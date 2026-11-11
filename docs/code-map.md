# Code map

How the code is laid out, who owns what, and where the 1.0 work goes. Existing files are upstream's; the skeleton I added at Roadmap is stubs only, nothing wired in yet. Line counts are from 2026-11-11.

## Processes

```
Steam UI (CEF, React)  <--callable/events-->  main.py (Decky backend, root)
                                                 |  starts, supervises
                                                 v
                                      tmux session "claude" (one Claude Code session)
                                         ^                 |
              chat view reads/sends -----+                 +-- claude spawns mcp_server.py (stdio MCP, child process)
              terminal tab attaches -----+                                   |
                                                       Steam CEF :8080, gamescope, xdotool/ydotool, logs
```

One Claude Code session, two views of it (ADR 0001). Python is stdlib only. The release zip is the install layout (see `CLAUDE.md`).

## Modules

Status: **present** = the code does this job today (upstream's code, or ours once merged); **planned** = a skeleton stub, filled in by the issues of its feature. An issue that fills a module moves its status to present in the same PR. Feature ids are the `features:` block in `ROADMAP.md` and the `feature:<id>` labels.

| Module | Owns | Talks to | Must | Feature | Status |
|---|---|---|---|---|---|
| `main.py` (1564) | Decky backend `Plugin`: starts and stops the session, working-dir setup and cleanup (also the trust and MCP entry it writes into the user's Claude Code config file, the skills link and the learning-loop hook), login (`get_auth`, `start_login`), session list, settings, update info; later the chat, terminal and CLI callables | `deck_common`, `machine_profile`, `terminal_session`, `transcript`, `cli_install` | M1, M2, M3, M7, M8 | session-core, chat, terminal-tab, login, plain-errors, cleanup | present (pty session; moves to tmux in session-core) |
| `mcp_server.py` (990) | MCP tools Claude calls: `steam_ui_eval`, `steam_snippet`, `screenshot`, input, `session_context`; the `SNIPPETS` table; later `steam_setting` (with its `SETTINGS` table) and `game_diagnose` | Steam CEF `:8080`, gamescope, `deck_common`, `diagnose` | M4, M5, M6 | game-context, steam-settings, launch-diagnosis | present (`steam_setting`, `game_diagnose` planned) |
| `deck_common.py` (216) | Display env and xdotool/ydotool commands shared by backend and MCP | none | M4 | (upstream) | present |
| `machine_profile.py` (323) | Hardware, OS and Steam profile written into the session's CLAUDE.md block | none | M6 | (upstream) | present |
| `terminal_session.py` | The tmux session: create, attach size, send keys/text, capture scrollback, stop; the only code that runs tmux | `tmux`, `main.py` | M2, M3 | session-core | planned |
| `transcript.py` | Turn the session's JSONL transcript into chat messages (user, assistant, tool use) for the chat view | `main.py` (session dir logic exists as `_session_dir`) | M2 | chat | planned |
| `cli_install.py` | Find, install and update the `claude` CLI under the plugin's own data directory (`find_installed`, `is_newer`, `install`, `update_available`) | network, `main.py._find_claude` | M1 | login | planned |
| `diagnose.py` | Collect launch evidence for one game (`parse_vdf`, `collect`, `summarize`): Steam and Proton logs, compat tool, launch options | files under the Steam dir, `mcp_server.py` | M6 | launch-diagnosis | planned |
| `src/index.tsx` (777) | Panel: session, login, working dir, QR, quick keys; later the Chat / Terminal tab switch and the login states | `main.py` callables | M1, M2, M7 | chat, login, plain-errors | present |
| `src/chat/ChatView.tsx` | Chat view: messages, input, on-screen keyboard, focus, Approve / Not now for a fix | `main.py` callables, `chat_message` events | M2, M4, M6 | chat, launch-diagnosis | planned |
| `src/terminal/TerminalTab.tsx` | Terminal tab: rendered scrollback, touch scroll, key row | `main.py` callables, `terminal_output` events | M3 | terminal-tab | planned |
| `src/errors.ts` | One place that turns backend and CLI errors into plain sentences with the fix | all views | M7 | plain-errors | planned |
| `src/sidebarTab.tsx` (225), `src/update.tsx` (195) | Optional sidebar icon; self-update (reads the release repo named in `main.py` `_UPDATE_REPO`: upstream's today, this fork's after the updater issue) | Decky, GitHub releases | kept | release | present (repo and version 1.1.0 planned) |
| `.github/workflows/release.yml` | Builds the release zip from a fixed file list; publishes on push to `main` when the workflow is enabled | GitHub | 1.0 line | release | present (new modules not in its list yet; disabled in the repo's Actions settings since 2026-11-11, turned back on by the last `release` issue) |
| `skills/steam-debugger` | The always-loaded debugging skill (submodule `vendor/skills`, upstream's) | `mcp_server.py` | M5, M6 | (upstream) | present |
| `scripts/setup-input-tools.sh` | Installs input helper tools | none | M4 | (upstream) | present |

## Interlinks

- Panel to backend: `callable<...>` calls in `src/index.tsx` and `emit` events from `main.py` (`session_status` exists; `chat_message` and `terminal_output` are added by the chat and terminal-tab issues).
- Backend to session: `terminal_session` is the only code that touches tmux; `main.py` asks it, never shells out to tmux itself.
- Session to tools: `claude --mcp-config` starts `mcp_server.py`; its tools are the only way Claude touches Steam, the screen and input.
- `diagnose.py` is imported by `mcp_server.py` (tool `game_diagnose`) and is pure: reads files, takes paths as arguments, so tests feed it fixtures.
- Release packaging copies a fixed file list (`release.yml`, the `cp` line): every new root module must be added there or it never ships.
- Outside writes: besides the working directory, the backend writes the trust and MCP entry (`_trust_working_dir`) into the user's Claude Code config file, and the skill's learning-loop hook (wired by `_learning_loop_settings`) writes a learnings file in the user's data folder. Both are undone by the `cleanup` issues (M8, my ruling of 2026-11-11).

## Where new work goes

| Must | Change |
|---|---|
| M1 | `cli_install.py` plus a login-state panel in `src/index.tsx` (login itself exists) |
| M2 | `terminal_session.py` + `transcript.py` + `src/chat/ChatView.tsx` |
| M3 | `src/terminal/TerminalTab.tsx` + `terminal_session.py` capture |
| M4 | Exists upstream (`screenshot`); the chat must attach it: `ChatView.tsx` + one MCP hint |
| M5 | New MCP tool `steam_setting` (read, set) in `mcp_server.py`, entries in its own `SETTINGS` allow-list table |
| M6 | `diagnose.py` + MCP tool `game_diagnose`, one line in the session's CLAUDE.md block (the steam-debugger skill is upstream's submodule: changes to it are sent upstream), Approve / Not now in `ChatView.tsx` |
| M7 | `src/errors.ts`, then each backend `error` string |
| M8 | `_setup_working_dir` records what existed; `_cleanup_working_dir` restores it byte for byte; `stop_session` removes the tmux socket and output log; `_trust_working_dir` records which of the two flags it added to the user's Claude Code config file and cleanup takes those out again; the learning-loop file goes back to what it was before the session, with the session's learnings kept in the plugin's data directory |

## Platforms (R04)

- **Linux (SteamOS):** the only runtime. Decky Loader runs the backend as root and the panel inside Steam's Gaming Mode UI. tmux 3.x and xdotool are in the SteamOS base image. Hand tests run on a SteamOS handheld.
- **Mac and PC:** no runtime and no build of the plugin (Won't W5): there is no Decky Loader or Gaming Mode there. They can still work on the code: the pure modules (`transcript.py`, `diagnose.py`, `cli_install.find_installed` and `is_newer`, `deck_common` command builders, `src/errors.ts`) run their tests anywhere Python 3.11+ and Node 20 run, and `pnpm typecheck` and `pnpm build` work on all three. Windows paths never appear in the code: the backend is Linux only.
- CI runs on `ubuntu-latest` only; no Mac or Windows job is needed for a Linux-only plugin.

## Tests

`tests/` uses `unittest` (stdlib) for the Python modules; `tests/test_skeleton.py` holds one skipped placeholder per Must with Python code (M1, M2, M3, M6, M8); each issue adds its own test file (the Easy issues carry theirs, locked, in the issue) and removes the placeholder it covers; `pnpm typecheck` and `pnpm build` cover the panel. Hand tests in Gaming Mode are listed per Must in `SPEC.md`.
