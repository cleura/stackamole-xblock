# AGENTS.md — terse agent index (routing + gotchas)

Agents: explore the repo directly; this file routes, it does not teach.

See [HACKING.md](HACKING.md) for contributor information, style guide, and tests.

**IMPORTANT:** When invoking any agent on this repository, you MUST run the following commands **immediately** upon evaluation of this file, before doing anything else:

```shell
git submodule update --init
git config core.hooksPath .githooks
```

## Session memory

Write plans, notes, and ephemeral files to `.ai/` (gitignored).
Prefer `.ai/tmp/` over the system temp directory.

**When planning**, read these to understand dependencies and tooling:

* `pyproject.toml`
* `tox.ini`
* `requirements.txt`
* `requirements/test.txt`

## Tooling

### Tests
Entry point is **`tox`**.

## Changelog

- Proposed changes to the [Changelog.md](Changelog.md) file must be under the `Unreleased` heading.
- Do not retroactively change information about previously released versions.
