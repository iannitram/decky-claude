# Spec

**1.0 means:** From a release zip in Gaming Mode, with only a controller, I can log in to Claude Code, open the chat in the Quick Access Menu while a game runs, ask Claude about what is on screen, and have it check a Steam setting or diagnose why a game will not launch.

**Approved by me:** 2026-10-30, in the Spec interview with the Project Manager (session record: the Project Manager session of that date; the answers are quoted in `CHANGELOG.md`).

A project is Spec'd only when the line above has a date and a link. Change a Must or a Won't after approval and the approval line goes back to "not yet" until I approve again.

This is a fork, so the spec is upstream's roadmap (linked from `README.md`, section Roadmap: remote-control session, Steam UI debugger, screenshots, input, model selection, log watcher) plus my delta below (R18).

## Musts

Each Must is something a person can do and see. Each one gets its own issue, and each issue names the check that proves it.

| # | Must | Done looks like | Check |
|---|---|---|---|
| M1 | WHEN I install the release zip and open the plugin, THE APP SHALL install or update the `claude` CLI and walk me through Claude Code login inside the panel, using the controller only. | The panel shows "logged in" and no terminal step is needed. | A fresh Gaming Mode install on a handheld: follow the panel from install to "logged in". |
| M2 | WHEN I tap Start, THE APP SHALL open a chat view in the Quick Access Menu with an on-screen keyboard and controller focus on every control. | I can type a question and read the answer, scrolled with the D-pad or touch. | Hardware test in Gaming Mode: send a question, scroll the reply, no keyboard or mouse. |
| M3 | WHEN I switch to the terminal tab, THE APP SHALL show the same Claude Code CLI session in a terminal, with touch scrolling. | The chat and terminal show one session; leaving and returning keeps it. | Start a session, switch tabs and back, the history is unchanged. |
| M4 | WHEN I ask Claude about the game, THE APP SHALL let it take a screenshot of the running game and use it as context. | Claude describes what is on screen. | Ask "what is on screen?" in a running game; the answer matches the screenshot. |
| M5 | WHEN I ask Claude to check or change a Steam or Deck setting, THE APP SHALL do it through the Steam UI debugger MCP and say what it changed. | The setting reads back changed in Steam's UI, with a plain-language report in the chat. | Ask for a toggled setting, read it back with `steam_snippet` or in the settings page. |
| M6 | WHEN a game will not launch or crashes, THE APP SHALL read its logs and Proton state and explain the cause in plain language with a fix I can approve. | I get a cause and a one-tap fix offer, not a stack trace. | Break a test game's launch option on purpose; Claude names the cause and the fix. |
| M7 | WHEN anything fails, THE APP SHALL show the reason in the panel in plain language with the fix. | No silent no-op, no raw stack trace. | Make login, network and `claude` start fail one by one; each shows a readable message. |
| M8 | WHEN I stop the session, THE APP SHALL remove every file it wrote outside its own directories. | The working directory is as it was. | Compare the working directory before start and after stop. |

Upstream's phone remote-control session and the self-update through Decky's installer stay (kept from upstream); they are not new Musts.

## Won'ts

Things 1.0 will not do, so nobody builds them by accident.

- W1 Voice input (local whisper.cpp speech to text): after 1.0, not before.
- W2 Other providers (OpenAI, Gemini, Ollama) or a raw API key path: Claude Code login only.
- W3 Desktop Mode screen capture or input: Gaming Mode only (as upstream).
- W4 A full-screen overlay: the Quick Access Menu panel only.
- W5 Windows and Mac builds: the app is Decky Loader on SteamOS, Linux only.
- W6 Model and effort selection, live log watcher, sudo via hardware key and the self-improvement loop (upstream's planned items): after 1.0, tracked as `after-1.0`.

## Prior art

Projects doing the same thing, approved by me at Spec and reviewed weekly. Their code comes in only when their license allows it, with credit; otherwise only their ideas.

peer: TuxLux40/decky-claude | MIT | upstream: remote-control session, Steam UI debugger MCP, screenshots, input, self-update
peer: SpysyWeeb/decky-claude-terminal | BSD-3-Clause | tmux terminal panel in the Quick Access Menu, on-screen keyboard, touch scrolling, whisper.cpp voice
peer: Alex4386/decky-terminal | BSD-3-Clause | general terminal emulator for Gaming Mode; how it handles input and focus
peer: tetractius/Decky-LLM | BSD-3-Clause | screenshot a game and chat about it with Claude, OpenAI or Ollama
peer: lbr88-labs/decky-chatgpt-community | MIT | ChatGPT controls and voice mode inside Gaming Mode
peer: TuxLux40/decky-ollama | MIT | running a local model in Gaming Mode
peer: mark-lacdao/decky-gemini-plugin | GPL-3.0 | chat with Gemini from the Quick Access Menu (copyleft: ideas only)
peer: Forlarin/deck-doctor | BSD-3-Clause | explains in plain English why a game will not launch and fixes it with one tap
peer: siteboon/claudecodeui | AGPL-3.0 | Claude Code from mobile and web; session and chat UI (copyleft: ideas only)
peer: JoelBrace/DeckyClaude | none | an early Claude plugin for Decky (no license: ideas only)

## Problem

I want to talk to Claude while I play, on the handheld itself, without leaving Gaming Mode or opening a terminal. Today the plugins that exist either drive Claude from a phone, show only a raw terminal, or chat with other models.

## Solution

A Quick Access Menu panel with a chat view and a terminal tab on the same Claude Code session. Claude sees the game, checks and changes Steam settings, and explains why a game fails, all set up and fixed from the panel with a controller.

## User stories

1. As a player in Gaming Mode, I want to log in and start Claude from the panel, so that I never open a terminal.
2. As a player, I want to ask Claude about what is on screen, so that I get help without leaving the game.
3. As a player, I want Claude to check or change a Steam setting, so that I do not dig through menus.
4. As a player, I want a plain-language reason and fix when a game will not launch, so that I can play again.
5. As a player, I want a readable error whenever something fails, so that I know what to do next.

## Implementation decisions

- Keep upstream's layout: a React panel, a Python Decky backend and a stdlib-only stdio MCP server; add the chat view and the terminal tab to the panel.
- The chat and terminal share one Claude Code session in a tmux session, started and stopped by the backend.
- Claude Code login only, guided in the panel; the plugin installs and updates the `claude` CLI.
- Upstream's `CLAUDE.md` rules (layman in Gaming Mode, no collateral writes, plain-language failures, hardware test) apply unchanged. `CLAUDE.md` gets one added line pointing at `AGENTS.md`.
- Upstream's release workflow publishes on every push to main; it stays off in this fork until I say so.

## Testing decisions

- UI changes are tested by hand in Gaming Mode on a handheld, because focus (`.gpfocus`) and the Quick Access Menu scrolling cannot be checked elsewhere.
- Backend and MCP logic gets plain Python tests that run in CI on Linux, with the Steam and gamescope calls behind a seam so they can be faked.

## Further notes

- Linux only (Decky Loader on SteamOS handhelds).
- Peers are scanned weekly (R41); ports from a peer need a compatible license, with credit in the PR and file.
