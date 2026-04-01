from django.db import migrations

# Rename the 'hastexo' tables to 'stackamole' to access labs created
# prior to the project rename.

OLD_APP_LABEL = 'hastexo'
NEW_APP_LABEL = 'stackamole'


def migrate_tables(apps, schema_editor):
    connection = schema_editor.connection
    existing_tables = connection.introspection.table_names()

    if 'hastexo_stack' in existing_tables:
        with connection.cursor() as cursor:
            # stackamole_* tables were created just now and contain no data,
            # confirm empty and drop
            cursor.execute("SELECT COUNT(*) FROM stackamole_stack")
            if cursor.fetchone()[0] > 0:
                raise Exception(
                    "'hastexo_stack' exists & 'stackamole_stack' contains "
                    "data; this scenario is out of scope for automated "
                    "migration.")
            cursor.execute("DROP TABLE stackamole_stacklog")
            cursor.execute("DROP TABLE stackamole_stack")
            # rename hastexo_* tables to stackamole_*
            cursor.execute(
                "ALTER TABLE hastexo_stacklog RENAME TO stackamole_stacklog")
            cursor.execute(
                "ALTER TABLE hastexo_stack RENAME TO stackamole_stack")


def migrate_contenttypes(apps, schema_editor):
    ContentType = apps.get_model('contenttypes', 'ContentType')
    db = schema_editor.connection.alias
    if ContentType.objects.using(db).filter(app_label=OLD_APP_LABEL).exists():
        # remove the stackamole content types that were just auto-created
        ContentType.objects.using(db).filter(app_label=NEW_APP_LABEL).delete()
        # rename 'hastexo' content types to 'stackamole'
        ContentType.objects.using(db).filter(app_label=OLD_APP_LABEL).update(
            app_label=NEW_APP_LABEL)


def migrate_migration_records(apps, schema_editor):
    # delete now orphaned 'hastexo' migration records
    schema_editor.connection.cursor().execute(
        "DELETE FROM django_migrations WHERE app = 'hastexo'"
    )


class Migration(migrations.Migration):

    dependencies = [
        ('stackamole', '0012_add_suspend_by'),
    ]

    # One way migration only from 'hastexo' to 'stackamole'
    operations = [
        migrations.RunPython(
            migrate_tables,
            migrations.RunPython.noop,
        ),
        migrations.RunPython(
            migrate_contenttypes,
            migrations.RunPython.noop,
        ),
        migrations.RunPython(
            migrate_migration_records,
            migrations.RunPython.noop,
        ),
    ]
