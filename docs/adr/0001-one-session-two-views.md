# 0001 One Claude Code session, two views

**Decided 2026-10-30.** The chat view and the terminal tab show the same Claude Code session, running in one tmux session started by the backend.

**Why.** Two sessions would split history and cost twice; the terminal gives the full CLI (permission prompts, slash commands), the chat gives a controller-friendly view. The chat reads the session's JSONL transcript for messages and sends text through tmux, so it needs no second protocol.

**Ruled out.** A chat built on `claude -p` stream-json (separate session, loses the CLI's prompts); a terminal-only panel (hard with a controller); a full-screen overlay (Won't W4).
