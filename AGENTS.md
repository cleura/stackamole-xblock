# AGENTS.md — terse agent index (routing + gotchas)

Agents: explore the repo directly; this file routes, it does not teach.

See [HACKING.md](HACKING.md) for contributor information, style guide, and tests.

**Session memory:** Write plans, notes, and ephemeral files to `.ai/` (gitignored).
Prefer `.ai/tmp/` over the system temp directory.

**When planning**, read these to understand dependencies and tooling:

* `pyproject.toml`
* `tox.ini`
* `requirements.txt`
* `requirements/test.txt`

## Tooling

### Tests
Entry point is **`tox`**.

### Hooks
Git hooks are stored in `.githooks`:

- `pre-commit` (lint only)
- `pre-push` (functional test)

### Review
Series are always **unsquashed**; each commit must be independently testable and correct.

### Git

- Read-only operations (`git log`, `git diff`, `git status`) are fine.
- Any mutating git operation (add, commit, reset, checkout, push, stash, merge, branch, etc.) requires explicit user approval.
- All modifications require a topic branch.
  Do not, under any circumstances, allow commits to the `master` or `main` branch.
- Refactoring tasks must always create a *new* topic branch.
- **Never** bypass Git hooks.
- **Never**, under any circumstances, invoke `git` with the `--no-verify` option.
- **Always** declare the AI tool and the employed model, by including `Assisted-By: <tool>/<model>` in the commit message.
- **Never** include emoji in commit messages.

## Changelog

- Proposed changes to the [Changelog.md](Changelog.md) file must be under the `Unreleased` heading.
- Do not retroactively change information about previously released versions.
