# CI runners (R29)

A public repo uses GitHub-hosted runners (`ubuntu-latest`, `windows-latest`, `macos-latest`) and has no self-hosted runner registered to it. A private repo runs on our self-hosted runners with these `runs-on:` lines (one job per OS):

```yaml
runs-on: [self-hosted, linux]
runs-on: [self-hosted, windows]
runs-on: [self-hosted, macos]
```

Trigger on `push` to `main` plus `pull_request` (`on: { push: { branches: [main] }, pull_request: }`), not on every branch push, so a PR fires one run, not two. Add `concurrency: { group: "${{ github.workflow }}-${{ github.event.pull_request.number || github.ref }}", cancel-in-progress: true }` so a newer run of the same PR or branch cancels the older one (decided 2026-10-28 ruling: "One run per commit (Recommended)").

On Windows, guard `setup-php` and `setup-python` with `if: runner.os != 'Windows' || runner.environment == 'github-hosted'` (the runner uses the machine's own tools). On Linux, install packages with `SUDO=$(command -v sudo || true); $SUDO apt-get install -y --no-install-recommends ...` and `DEBIAN_FRONTEND: noninteractive`. Give `Swatinem/rust-cache` `cache-bin: false`. Use only the labels above.

Switch a repo to them only after its runners show online (`python3 tools/runners/register.py --status <repo>` in the pipeline repo); a job no online runner matches stays queued. A public repo never switches to them (R29); it sets "Require approval for all outside collaborators" instead. Steps: the pipeline repo's `reference/self-hosted-runners.md`.
