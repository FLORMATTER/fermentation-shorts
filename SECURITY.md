# Security Policy

## Scope

This repository contains **no server, no user data and no credentials**. It is
a static collection of HTML/SVG animations plus local Python and Node helper
scripts that run on the author's own machine. There is therefore no runtime
attack surface to report in the usual sense.

## What is still worth reporting

Please open an issue (or contact the owner privately for anything sensitive) if
you find:

- **A leaked secret** — an API key, token or password accidentally committed in
  any file, including the `_arquivo/` folder or a manual backup.
- **A script that does something destructive** without a dry-run — for example
  deleting or overwriting files outside the project directory.
- **A path-traversal or command-injection flaw** in a helper script that reads
  a filename from the command line and passes it to a shell.

## How the scripts are meant to behave

- Destructive operations are **dry-run by default** and require an explicit
  `--apply` flag (see `_consertar-transform.py`).
- Scripts write only inside the project directory.
- `_gerar-mp4.js` launches a local Chrome install headlessly and writes the
  resulting `.mp4` next to the source `.html`.

If a script deviates from the above, that is a bug worth reporting.

## Supported versions

Only the current `main` branch is maintained.
