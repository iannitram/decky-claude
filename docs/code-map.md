# Code map

How the code is laid out, who owns what, and where the 1.0 work goes. Existing files are upstream's; **new** marks the skeleton I added at Roadmap (stubs only, nothing wired in yet). Line counts are from 2026-10-30.

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

| Module | Owns | Talks to | Must |
|---|---|---|---|
| `main.py` (1545) | Decky backend `Plugin`: starts and stops the session, working-dir setup and cleanup, login (`get_auth`, `start_login`), session list, settings, update info | `deck_common`, `machine_profile`, `terminal_session` (new), `cli_install` (new) | M1, M2, M3, M8 |
| `mcp_server.py` (976) | MCP tools Claude calls: `steam_ui_eval`, `steam_snippet`, `screenshot`, input, `session_context`; the `SNIPPETS` table | Steam CEF `:8080`, gamescope, `deck_common`, `diagnose` (new) | M4, M5, M6 |
| `deck_common.py` (192) | Display env and xdotool/ydotool commands shared by backend and MCP | none | M4 |
| `machine_profile.py` (323) | Hardware, OS and Steam profile written into the session's CLAUDE.md block | none | M6 |
| `terminal_session.py` **new** | The tmux session: create, attach size, send keys/text, capture scrollback, stop | `tmux`, `main.py` | M2, M3 |
| `transcript.py` **new** | Turn the session's JSONL transcript into chat messages (user, assistant, tool use) for the chat view | `main.py` (session dir logic exists as `_session_dir`) | M2 |
| `cli_install.py` **new** | Find, install and update the `claude` CLI under the plugin's own directory | network, `main.py._find_claude` | M1 |
| `diagnose.py` **new** | Collect launch evidence for one game: Steam and Proton logs, compat tool, launch options, last exit | files under the Steam dir, `mcp_server.py` | M6 |
| `src/index.tsx` (777) | Panel: session, login, working dir, QR, quick keys | `main.py` callables | M1, M7 |
| `src/chat/ChatView.tsx` **new** | Chat view: messages, input, on-screen keyboard, focus | `main.py` callables, `transcript.py` events | M2, M4 |
| `src/terminal/TerminalTab.tsx` **new** | Terminal tab: rendered scrollback, touch scroll, key row | `main.py` callables | M3 |
| `src/errors.ts` **new** | One place that turns backend and CLI errors into plain sentences with the fix | all views | M7 |
| `src/sidebarTab.tsx` (225), `src/update.tsx` (195) | Optional sidebar icon; self-update | Decky | kept |
| `skills/steam-debugger` | The always-loaded debugging skill (submodule `vendor/skills`) | `mcp_server.py` | M5, M6 |
| `scripts/setup-input-tools.sh` | Installs input helper tools | none | M4 |

## Interlinks

- Panel to backend: `callable<...>` calls in `src/index.tsx` and `emit` events from `main.py` (`session_status` exists; `chat_message` and `terminal_output` are added by the skeleton's issues).
- Backend to session: `terminal_session` is the only code that touches tmux; `main.py` asks it, never shells out to tmux itself.
- Session to tools: `claude --mcp-config` starts `mcp_server.py`; its tools are the only way Claude touches Steam, the screen and input.
- `diagnose.py` is imported by `mcp_server.py` (tool `game_diagnose`) and is pure: reads files, takes paths as arguments, so tests feed it fixtures.
- Release packaging copies a fixed file list (`release.yml`, the `cp` line): every new root module must be added there or it never ships.

## Where new work goes

| Must | Change |
|---|---|
| M1 | `cli_install.py` plus a login-state panel in `src/index.tsx` (login itself exists) |
| M2 | `terminal_session.py` + `transcript.py` + `src/chat/ChatView.tsx` |
| M3 | `src/terminal/TerminalTab.tsx` + `terminal_session.py` capture |
| M4 | Exists upstream (`screenshot`); the chat must attach it: `ChatView.tsx` + one MCP hint |
| M5 | New MCP tool `steam_setting` (read, set) in `mcp_server.py`, entries in `SNIPPETS` |
| M6 | `diagnose.py` + MCP tool `game_diagnose`, text in the steam-debugger skill |
| M7 | `src/errors.ts`, then each backend `error` string |
| M8 | Extend `_cleanup_working_dir` and add its test |

## Platforms (R04)

Linux only at runtime: Decky Loader on SteamOS. The pure parts (`diagnose.py`, `transcript.py`, `deck_common` command builders, `src/errors.ts`) are plain Python and TypeScript and run their tests on any machine, so Mac and PC can build, typecheck and test; they cannot run the plugin. Nothing here targets Mac or Windows at runtime (Won't W5).

## Tests

`tests/` uses `unittest` (stdlib) for the Python modules; `pnpm typecheck` and `pnpm build` cover the panel. Hand tests in Gaming Mode are listed per Must in `SPEC.md`.
