# Roadmap

The path to 1.0 in `SPEC.md`. Upstream's own roadmap (README, section Roadmap) is the base; this is my delta (R18). Code layout and where each piece goes: `docs/code-map.md`. Linux only (Decky Loader on SteamOS); the pure modules also build and test on Mac and PC (R04).

## Feature list (delta over upstream)

| Feature | Must | Upstream or fork | Status |
|---|---|---|---|
| Guided login in the panel | M1 | exists upstream (`start_login`, QR) | keep |
| Install and update the `claude` CLI | M1 | keep on our fork | new |
| Chat view with on-screen keyboard | M2 | keep on our fork | new |
| Terminal tab on the same session | M3 | keep on our fork | new |
| Screenshot attached to the chat | M4 | `screenshot` exists upstream | wire |
| Read and change Steam settings | M5 | send upstream | new |
| Launch diagnosis | M6 | send upstream | new |
| Plain-language errors | M7 | keep on our fork | new |
| No collateral files | M8 | exists upstream (`_cleanup_working_dir`) | test |
| Voice input, model selection, log watcher | W1, W6 | after-1.0 | later |

## Open-source candidates

License rules per R41: code only where the license allows it, with credit in the PR and the file.

| Peer | License | Take |
|---|---|---|
| `SpysyWeeb/decky-claude-terminal` | BSD-3-Clause | tmux panel, on-screen keyboard and touch scrolling: port into `terminal_session.py` and `TerminalTab.tsx` (credit) |
| `Alex4386/decky-terminal` | BSD-3-Clause | terminal focus and input handling: read, port if it fits |
| `tetractius/Decky-LLM` | BSD-3-Clause | screenshot-to-chat flow: port the idea, write fresh |
| `Forlarin/deck-doctor` | BSD-3-Clause | which Proton and Steam logs explain a launch failure: port into `diagnose.py` |
| `lbr88-labs/decky-chatgpt-community` | MIT | voice mode flow, after 1.0 |
| `mark-lacdao/decky-gemini-plugin`, `siteboon/claudecodeui`, `JoelBrace/DeckyClaude` | GPL-3.0, AGPL-3.0, none | ideas only |

## Dev stages

1. **Groundwork.** Ship the new modules (skeleton) in the zip: add them to the release `cp` line; run the CI workflow; wire `tests/`. Needs the release workflow's file list changed (fork delta, ask me before enabling Actions).
2. **Session core (M3, M8).** `terminal_session.py` on tmux, `main.py` starts the one session there, `_cleanup_working_dir` test.
3. **Chat (M2, M4).** `transcript.py`, `ChatView.tsx`, on-screen keyboard, controller focus, screenshot attach.
4. **Terminal tab (M3).** `TerminalTab.tsx`, scrollback and touch scrolling.
5. **Login and CLI (M1).** `cli_install.py`, login state in the panel.
6. **Settings and diagnosis (M5, M6).** `steam_setting` MCP tool, `diagnose.py`, `game_diagnose` tool, skill text.
7. **Errors (M7).** `src/errors.ts` and every backend error string.
8. **Design pass (R04, last).** `baoyu-design` over the running panel against the shared design system; `design-pass` issues.

Stage 1 comes first; 2 before 3 and 4; 5, 6 and 7 are independent of each other once 2 is done.

## Risks

- The release workflow publishes on every push to `main`; pushes of new root modules do nothing until stage 1 packages them. The pipeline-file pushes (`SPEC.md`, `ROADMAP.md`, `PIPELINE.md`) would also release unless added to its `paths-ignore`.
- Hardware tests in Gaming Mode cannot run in CI; each UI issue carries a hand-test step.
