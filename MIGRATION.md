# Migrating from the Hastexo XBlock to the Stackamole XBlock

This project was renamed to Stackamole XBlock in May 2026.
From version `9` forward, it includes a one-way migration script to rename the data tables.
To migrate your project, using Tutor, do the following:
1. Install and enable `git+https://github.com/cleura/tutor-contrib-stackamole@v3.0.0` (`v3.0.0` or higher) in your Tutor environment.
2. In the Tutor `config.yml` file, add `stackamole-xblock>=9.0.0` to the `OPENEDX_EXTRA_PIP_REQUIREMENTS` list.
3. Rename all your `HASTEXO_*` settings in `config.yml` to `STACKAMOLE_*`.
4. Update the `terminal_url` in your `STACKAMOLE_XBLOCK_SETTINGS` to `/stackamole-xblock/`.
5. Run `tutor config save`.
6. Rebuild the `openedx` and `stackamole` images.
7. Run `tutor local/k8s launch`.
   This includes running the migration script to rename the data tables.
8. (Optional) Depending on your deployment setup, you might need to delete the `hastexo` deployments once all other steps are completed.
   For example, in a `k8s` environment, run:
   ```bash
    kubectl -n <namespace> delete deployment hastexo-xblock
    kubectl -n <namespace> delete deployment hastexo-xblock-reaper
    kubectl -n <namespace> delete deployment hastexo-xblock-suspender
   ```

## Migrating courses

Your courses should now use the `stackamole` module instead of `hastexo`, however a `hastexo` entrypoint will remain in the XBlock for backward compatibility, until further notice.
This means that all courses using the `hastexo` module will run normally, and importing such a course will also remain possible.

### Export/import cycle

The easiest way to migrate your courses, is to export and re-import them, as the XBlock will now automatically export the course to use the `stackamole` module.

### Manual modifications

If you need to manually migrate your course XML:
* rename all `<hastexo>` tags to `<stackamole>`,
* rename the `hastexo` directory to `stackamole`,
* update the the `advanced_modules` list in your `policy.json` to include `stackamole` instead of `hastexo`.
