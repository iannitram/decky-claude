# Roadmap

The path to 1.0 in `SPEC.md`. Upstream's own roadmap (README, section Roadmap) is the base; this file is my delta only (R18): issues and the code map cover what upstream will not do. Code layout and where each piece goes: `docs/code-map.md`. Decisions: `docs/adr/`.

Updated: 2026-11-11

features:
- release: Our release zip ships every module, from this fork
- session-core: One Claude Code session in tmux, started and stopped by the backend (ADR 0001)
- chat: Chat view of the session in the Quick Access Menu, on-screen keyboard, controller focus (M2)
- game-context: Claude sees the running game through a screenshot asked for in the chat (M4)
- terminal-tab: Terminal tab on the same session with touch scrolling (M3)
- login: Install and update the claude CLI and log in from the panel with a controller (M1)
- steam-settings: Check and change Steam and Deck settings through the Steam UI debugger (M5)
- launch-diagnosis: Explain why a game will not launch, with a fix to approve (M6)
- plain-errors: Every failure shown in the panel as a plain sentence with the fix (M7)
- cleanup: Stopping the session leaves the working directory as it was (M8)
- design-pass: The pre-1.0 design pass over the running panel (R04)
- voice: Voice input with local whisper.cpp, after 1.0 (W1)
- upstream-planned: Upstream's planned items, merged from upstream after 1.0 (W6)

Every issue carries exactly one `feature:<id>` label from this block and one milestone: `1.0` for everything above except `voice` and `upstream-planned`, which are `After 1.0` (`after-1.0`, not sized).

## Features against the spec

| Feature | Must | Upstream or fork | What exists today |
|---|---|---|---|
| release | 1.0 line ("from a release zip") | keep on our fork | release workflow and self-updater exist upstream; the new modules are not in the zip's file list, and the updater reads upstream's releases |
| session-core | M2, M3 | keep on our fork | the session runs on a private pty; tmux is ADR 0001 |
| chat | M2 | keep on our fork | `ChatView.tsx` and `transcript.py` stubs |
| game-context | M4 | exists upstream (`screenshot`) | the chat must lead Claude to it |
| terminal-tab | M3 | keep on our fork | `TerminalTab.tsx` stub |
| login | M1 | login exists upstream (`start_login`, QR); CLI install keep on our fork | `cli_install.py` stub |
| steam-settings | M5 | send upstream | `steam_ui_eval` and `steam_snippet` exist; no settings tool |
| launch-diagnosis | M6 | send upstream | `diagnose.py` stub |
| plain-errors | M7 | keep on our fork | `src/errors.ts` stub; backend errors are partly plain |
| cleanup | M8 | send upstream | `_cleanup_working_dir` exists but leaves a `.claude/` folder and reformats files it touched |
| design-pass | R04 | keep on our fork | runs last |
| voice | W1 | keep on our fork | after 1.0 |
| upstream-planned | W6 | upstream's (TuxLux40/decky-claude #5, #6, #7, #9) | after 1.0; merged when upstream ships them |

## Upstream

Upstream (TuxLux40/decky-claude) moved 4 commits after the spec (2026-10-31: held keys for synthetic input, the steam-debugger learning loop, README). They were merged into our `main` on 2026-11-02; on 2026-11-11 upstream `main` has nothing we lack. Upstream's branch `fix/input-follows-focused-display` (1 commit, 2026-10-27) is not on its `main`; the same fix is already on our `main` (`deck_common.focused_x_display`).

## Dev stages

1. **Groundwork (release).** The zip ships the new modules; pipeline docs no longer trigger a release. The self-updater's source and whether this fork publishes at all wait on my ruling (Risks).
2. **Session core (session-core, cleanup).** `terminal_session.py` on tmux, then `main.py` runs the one session there; cleanup restores the working directory byte for byte, and stopping removes the session's own files.
3. **Chat (chat, game-context).** `transcript.py`, backend chat events, `ChatView.tsx`, the Chat / Terminal tab switch with the on-screen keyboard and controller focus; then "what is on screen?" through the screenshot tool.
4. **Terminal tab (terminal-tab).** Screen capture, keys and resize in the backend; `TerminalTab.tsx` with touch scrolling and a key row.
5. **Login and CLI (login).** `find_installed` and `is_newer`, then install and update into the plugin's data directory, the backend using that copy, and the login states in the panel.
6. **Settings and diagnosis (steam-settings, launch-diagnosis).** The `steam_setting` tool and its checked settings table; `parse_vdf`, `summarize`, `collect`, the `game_diagnose` tool and the one-tap fix in the chat.
7. **Errors (plain-errors).** The `plainError` table with its CI test, then every backend failure as a plain sentence with the fix.
8. **Design pass (design-pass, last before 1.0, R04).** `baoyu-design` over the running panel in Gaming Mode against the design system shared by all our apps; its findings are filed as `design-pass` issues and built before Prototype / Beta.

Order: stage 1 first. The pure pieces (`transcript`, `cli_install.find_installed`/`is_newer`, `parse_vdf`, `summarize`, `plainError`, the `steam_setting` plumbing, the cleanup restore) need nothing and can start at once. Stage 2 comes before the chat and terminal backends; stages 5, 6 and 7 are independent of each other; the design pass waits for everything else. The `Blocked by` lines on the issues are the exact order.

## Mac, PC and Linux (R04)

This is a Decky Loader plugin for Steam's Gaming Mode on SteamOS, so it runs only on Linux (Won't W5).

- **Linux (SteamOS):** the only place the plugin runs. Backend under Decky as root, panel in Steam's Quick Access Menu, the session as the desktop user. tmux 3.x and xdotool ship in the SteamOS base image. The CLI download is Linux x64 (SteamOS handhelds are x64). Every UI issue carries a hand test on a SteamOS handheld (`platform:linux`).
- **Mac:** no build and no runtime: there is no Decky Loader or Gaming Mode. A Mac can work on the pure modules and their tests, and run `pnpm typecheck` and `pnpm build`.
- **PC (Windows):** the same as Mac: no build and no runtime; pure modules, tests, typecheck and build only. Nothing in the code may assume Windows paths.
- CI is `ubuntu-latest` only, which matches the one runtime.

## Open-source candidates

License rules per R41: code only where the license allows it, with credit in the PR and the file.

| Peer | License | Take | Where |
|---|---|---|---|
| `SpysyWeeb/decky-claude-terminal` | BSD-3-Clause | tmux panel, on-screen keyboard and touch scrolling: port (credit) | `terminal_session.py`, `TerminalTab.tsx` |
| `Alex4386/decky-terminal` | BSD-3-Clause | terminal focus and input handling in Gaming Mode: read, port if it fits | `TerminalTab.tsx` |
| `tetractius/Decky-LLM` | BSD-3-Clause | screenshot-to-chat flow: port the idea, write fresh | game-context |
| `Forlarin/deck-doctor` | BSD-3-Clause | which Proton and Steam logs explain a launch failure; one-tap fixes | `diagnose.py`, the one-tap fix |
| `lbr88-labs/decky-chatgpt-community` | MIT | voice mode flow | voice, after 1.0 |
| `TuxLux40/decky-ollama` | MIT | local model in Gaming Mode | ideas only (Won't W2) |
| `mark-lacdao/decky-gemini-plugin`, `siteboon/claudecodeui`, `JoelBrace/DeckyClaude` | GPL-3.0, AGPL-3.0, none | chat UI ideas | ideas only |

Libraries: none added. Python stays stdlib only; the panel keeps upstream's dependencies (`@decky/ui`, `@decky/api`). A VDF reader is written fresh (`parse_vdf`, about 50 lines) rather than adding a dependency the release zip would have to vendor.

## Risks

- **The release workflow is on in this fork and has published v1.0.13 (2026-10-30) and v1.0.14 (2026-11-02)**, though the spec says it stays off until I say so. Pushes that touch `SPEC.md`, `ROADMAP.md`, `PIPELINE.md` or `CHANGELOG.md` also release, because only `README.md`, `CLAUDE.md`, `docs/**`, `assets/**`, `scripts/prototypes/**` and `.github/**` are ignored (the release issue fixes the list).
- **The self-updater reads upstream's releases** (`_UPDATE_REPO = "TuxLux40/decky-claude"`). An install of our zip offers upstream's newer version (v1.0.15 today) and would replace our delta with upstream's build. Held for my ruling: point it at this fork with versions above upstream's, or keep auto-update off in our builds.
- Hardware tests in Gaming Mode cannot run in CI; each UI issue carries a hand-test step on a SteamOS handheld.
- Steam's internal UI API (`steam_setting`) changes between client versions; each settings entry records the client version it was checked on.
