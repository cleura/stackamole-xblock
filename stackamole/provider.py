import time
import base64
import logging
import paramiko
import random
import string
from cryptography.hazmat.primitives import serialization, asymmetric

try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO

from heatclient.exc import HTTPException, HTTPNotFound
from keystoneauth1.exceptions.http import HttpError
from novaclient.exceptions import ClientException, NotFound

from .common import (
    b,
    get_xblock_settings,
    IN_PROGRESS,
    FAILED,
    DELETE_COMPLETE,
    DELETE_IN_PROGRESS,
    RESUME_COMPLETE,
    RESUME_IN_PROGRESS,
    SUSPEND_COMPLETE,
    SUSPEND_IN_PROGRESS
)
from .openstack import HeatWrapper, NovaWrapper


class ProviderException(Exception):
    pass


class Provider(object):
    """
    Base class for provider drivers.

    """
    default_credentials = None
    credentials = None
    name = None
    capacity = None
    template = None
    environment = None
    sleep_seconds = None

    @staticmethod
    def init(name):
        settings = get_xblock_settings()
        sleep_seconds = settings.get("sleep_timeout", 10)
        providers = settings.get("providers")
        config = providers.get(name)
        if config and isinstance(config, dict):
            provider_type = config.get("type")
            if provider_type == "openstack" or not provider_type:
                return OpenstackProvider(name, config, sleep_seconds)
            else:
                raise ProviderException(
                    f"Unsupported provider type: {provider_type} "
                    f"for provider: {name}.")
        else:
            raise ProviderException(
                f"Configuration missing for provider: {name}")

    def __init__(self, name, config, sleep):
        self.name = name
        self.sleep_seconds = sleep
        self.reset_logger()

        # Get credentials
        if config and isinstance(config, dict):
            credentials = {}
            for key, default in self.default_credentials.items():
                credentials[key] = config.get(key, default)
            self.credentials = credentials
        else:
            error_msg = ("No configuration provided for provider %s" %
                         self.name)
            raise ProviderException(error_msg)

    def set_logger(self, logger):
        """Set a logger other than the standard one.

        This is meant to be used from Celery tasks, which usually
        would want to use their task logger for logging.
        """
        self.logger = logger

    def reset_logger(self):
        """Reset the logger back to the standard one."""
        self.logger = logging.getLogger(__name__)

    def set_capacity(self, capacity):
        if capacity in (None, "None"):
            capacity = -1
        else:
            try:
                capacity = int(capacity)
            except (TypeError, ValueError):
                # Invalid capacity: disable the provider
                capacity = 0

        self.capacity = capacity

    def set_template(self, template):
        if not template:
            error_msg = ("No template provided for provider %s" % self.name)
            raise ProviderException(error_msg)

        self.template = template

    def set_environment(self, environment):
        if not environment:
            error_msg = ("No environment provided for provider %s" % self.name)
            raise ProviderException(error_msg)

        self.environment = environment

    def sleep(self):
        time.sleep(self.sleep_seconds)

    def generate_key_pair(self, encodeb64=False, key_type="rsa"):
        keypair = {}

        if key_type == "ed25519":
            # use cryptography to generate Ed25519Key until paramiko adds
            # support for the key generation as well.
            ed25519key = asymmetric.ed25519.Ed25519PrivateKey.generate()

            public_key = ed25519key.public_key().public_bytes(
                encoding=serialization.Encoding.OpenSSH,
                format=serialization.PublicFormat.OpenSSH).decode()
            keypair["public_key"] = public_key

            private_key = ed25519key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.OpenSSH,
                encryption_algorithm=serialization.NoEncryption()).decode()

        else:
            pkey = paramiko.RSAKey.generate(4096)
            keypair["public_key"] = f'{pkey.get_name()} {pkey.get_base64()}'
            s = StringIO()
            pkey.write_private_key(s)
            private_key = s.getvalue()
            s.close()

        if encodeb64:
            private_key = base64.b64encode(b(private_key))

        keypair["private_key"] = private_key

        return keypair

    def generate_random_password(self, length):
        abc = string.ascii_lowercase
        return "".join(random.choice(abc) for i in range(length))

    def get_stacks(self):
        raise NotImplementedError()

    def get_stack(self):
        raise NotImplementedError()

    def create_stack(self):
        raise NotImplementedError()

    def delete_stack(self):
        raise NotImplementedError()

    def suspend_stack(self):
        raise NotImplementedError()

    def resume_stack(self):
        raise NotImplementedError()


class OpenstackProvider(Provider):
    """
    OpenStack provider driver.

    """
    default_credentials = {
        "os_auth_url": "",
        "os_auth_token": "",
        "os_username": "",
        "os_password": "",
        "os_user_id": "",
        "os_user_domain_id": "",
        "os_user_domain_name": "",
        "os_project_id": "",
        "os_project_name": "",
        "os_project_domain_id": "",
        "os_project_domain_name": "",
        "os_region_name": ""
    }
    heat_c = None
    nova_c = None

    def __init__(self, provider, config, sleep):
        super(OpenstackProvider, self).__init__(provider, config, sleep)

        self.heat_c = self._get_heat_client()
        self.nova_c = self._get_nova_client()

    def _get_heat_client(self):
        return HeatWrapper(**self.credentials).get_client()

    def _get_nova_client(self):
        return NovaWrapper(**self.credentials).get_client()

    def _get_stack_outputs(self, heat_stack):
        outputs = {}
        for o in getattr(heat_stack, 'outputs', []):
            output_key = o["output_key"]
            output_value = o["output_value"]
            outputs[output_key] = output_value

        return outputs

    def get_stacks(self):
        stacks = []
        try:
            heat_stacks = self.heat_c.stacks.list()
        except HTTPNotFound:
            return stacks
        except (HTTPException, HttpError) as e:
            raise ProviderException(e)

        if heat_stacks:
            for heat_stack in heat_stacks:
                stack = {
                    "name": heat_stack.stack_name,
                    "status": heat_stack.stack_status
                }
                stacks.append(stack)

        return stacks

    def get_stack(self, name):
        try:
            self.logger.debug('Fetching information on '
                              'OpenStack Heat stack [%s]' % name)
            heat_stack = self.heat_c.stacks.get(stack_id=name)
        except HTTPNotFound:
            status = DELETE_COMPLETE
            outputs = {}
        except (HTTPException, HttpError) as e:
            raise ProviderException(e)
        else:
            status = heat_stack.stack_status
            outputs = self._get_stack_outputs(heat_stack)

        return {"status": status,
                "outputs": outputs}

    def create_stack(self, name, run, key_type=""):
        if not self.template:
            raise ProviderException("Template not set for provider %s." %
                                    self.name)
        keypair = {}
        if key_type:
            keypair = self.generate_key_pair(key_type=key_type)
            try:
                self.nova_c.keypairs.create(
                    name=name,
                    public_key=keypair["public_key"],
                    key_type='ssh'
                )
                self.logger.info("Created a key with type [%s]" % key_type)
            except ClientException as e:
                raise ProviderException(e)

        try:
            self.logger.info('Creating OpenStack Heat stack [%s]' % name)
            res = self.heat_c.stacks.create(
                stack_name=name,
                template=self.template,
                environment=self.environment,
                parameters={'run': run}
            )
        except (HTTPException, HttpError) as e:
            raise ProviderException(e)

        stack_id = res['stack']['id']

        # Sleep to avoid throttling.
        self.sleep()

        try:
            heat_stack = self.heat_c.stacks.get(stack_id=stack_id)
        except (HTTPException, HttpError) as e:
            raise ProviderException(e)

        status = heat_stack.stack_status

        # Wait for stack creation
        while IN_PROGRESS in status:
            self.sleep()

            try:
                heat_stack = self.heat_c.stacks.get(stack_id=heat_stack.id)
            except HTTPNotFound:
                raise ProviderException("OpenStack Heat stack "
                                        "disappeared during creation.")
            except (HTTPException, HttpError) as e:
                raise ProviderException(e)

            status = heat_stack.stack_status

        if FAILED in status:
            raise ProviderException("Failure creating OpenStack Heat stack.")

        res = {"status": status,
               "outputs": self._get_stack_outputs(heat_stack)}
        if keypair:
            res["private_key"] = keypair["private_key"]

        return res

    def resume_stack(self, name):
        try:
            self.logger.info('Resuming OpenStack Heat stack [%s]' % name)
            self.heat_c.actions.resume(stack_id=name)
        except (HTTPException, HttpError) as e:
            raise ProviderException(e)

        status = RESUME_IN_PROGRESS

        # Wait until resume finishes.
        while (FAILED not in status and
               status != RESUME_COMPLETE):
            self.sleep()

            try:
                heat_stack = self.heat_c.stacks.get(
                    stack_id=name)
            except HTTPNotFound:
                raise ProviderException("OpenStack Heat stack "
                                        "disappeared during resume.")
            except (HTTPException, HttpError) as e:
                raise ProviderException(e)
            else:
                status = heat_stack.stack_status

        if FAILED in status:
            raise ProviderException("Failure resuming OpenStack Heat stack")

        outputs = self._get_stack_outputs(heat_stack)

        # Reboot servers, if requested
        reboot_on_resume = outputs.get("reboot_on_resume")
        if (reboot_on_resume is not None and
                isinstance(reboot_on_resume, list)):
            for server in reboot_on_resume:
                try:
                    self.logger.info("Rebooting OpenStack Nova "
                                     "instance %s" % server)
                    self.nova_c.servers.reboot(server, 'HARD')
                except ClientException as e:
                    raise ProviderException(e)

        return {"status": status,
                "outputs": outputs}

    def suspend_stack(self, name, wait=True):
        try:
            self.logger.info("Suspending OpenStack Heat stack [%s]" % name)
            self.heat_c.actions.suspend(stack_id=name)
        except (HTTPException, HttpError) as e:
            raise ProviderException(e)

        status = SUSPEND_IN_PROGRESS

        # Wait until suspend finishes.
        if wait:
            while (FAILED not in status and
                   status != DELETE_COMPLETE and
                   status != SUSPEND_COMPLETE):
                self.sleep()

                try:
                    heat_stack = self.heat_c.stacks.get(
                        stack_id=name)
                except HTTPNotFound:
                    status = DELETE_COMPLETE
                except (HTTPException, HttpError) as e:
                    raise ProviderException(e)
                else:
                    status = heat_stack.stack_status

            if FAILED in status:
                raise ProviderException("Failure suspending "
                                        "OpenStack Heat stack.")

        return {"status": status}

    def delete_stack(self, name, wait=True):
        try:
            self.logger.info("Deleting Nova Keypair [%s]" % name)
            self.nova_c.keypairs.delete(name)
        except NotFound:
            self.logger.info(
                "Keypair not found for deletion for stack [%s]" % name)

        try:
            self.logger.info("Deleting OpenStack Heat stack [%s]" % name)
            self.heat_c.stacks.delete(stack_id=name)
        except (HTTPException, HttpError) as e:
            raise ProviderException(e)

        status = DELETE_IN_PROGRESS

        # Wait until delete finishes.
        if wait:
            while (FAILED not in status and
                   status != DELETE_COMPLETE):
                self.sleep()

                try:
                    heat_stack = self.heat_c.stacks.get(
                        stack_id=name)
                except HTTPNotFound:
                    status = DELETE_COMPLETE
                except (HTTPException, HttpError) as e:
                    raise ProviderException(e)
                else:
                    status = heat_stack.stack_status

            if FAILED in status:
                raise ProviderException("Failure deleting "
                                        "OpenStack Heat stack.")

        return {"status": status}
