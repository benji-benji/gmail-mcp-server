# gmail-mcp-server

A small MCP server that connects **Claude Desktop** to **Gmail** so Claude can:

- read unread emails from Inbox (excluding spam/promotions/social/trash)
- create *threaded* draft replies (and update an existing draft if you pass `draft_id`)

---

## What it does

### Tool 1: `get_unread_emails(max_results=5)`

Returns unread inbox emails with:

- `from_`, `subject`, `snippet`
- `message_id`, `thread_id`, `rfc_message_id`

Claude calling the tool:

![Claude tool request](assets/I'll%20check%20unread%20emails%201%20-%20claude.png)

Example output:

![Claude tool output](assets/I'll%20check%20unread%20emails%202%20-%20claude.png)

---

### Tool 2: `create_draft_reply(...)`

Creates a Gmail draft reply in the correct thread.

If you pass `draft_id`, it **updates** the existing draft instead of creating multiple drafts in the same thread.

Claude calling `create_draft_reply`:

![Claude create_draft_reply](assets/do%20it%20again%20%20tfl%20-%20claude.png)

Claude creating drafts for multiple emails:

![Claude create drafts](assets/I'll%20create%20draft%20replies%20-%20claude.png)

Drafts showing up in Gmail:

![Gmail Hackney Empire draft](assets/hackney%20empire%20-%20gmail.png)

![Gmail Hetzner draft](assets/hetzner%20reply%20-%20gmail.png)

![Gmail TfL draft](assets/transport%20for%20london%20reply%20-%20gmail.png)

---

## Prerequisites

- Python 3.12+
- `uv`
- Claude Desktop
- Gmail account

---

## Security

This repo does **not** include secrets.

Local-only (gitignored):

- `credentials.json` (downloaded from Google Cloud)
- `token.json` (generated locally after first auth)

---

## Google OAuth (Gmail API) setup

1. Create Google Cloud project
2. Enable **Gmail API**
3. Create OAuth Client ID (**Desktop app**)
4. Download client JSON → save as `credentials.json` in repo root
5. Scopes used:
   - `https://www.googleapis.com/auth/gmail.readonly`
   - `https://www.googleapis.com/auth/gmail.compose`

## First Auth

Generates `token.json`:
```bash
uv run python scripts/smoke_read.py
```

## Install + Run

### Install Dependencies
```bash
uv sync
```

### Run Server Manually

Useful for debugging:
```bash
uv run python -m mcp_gmail_server.server
```

## Claude Desktop Config

My Claude config uses the full uv path plus `--directory` so Claude starts the server from the repo root reliably.

![Claude desktop config](assets/claude%20desktop%20config%20json.png)

**Note:** After editing config, quit Claude fully (Cmd+Q) and reopen.

## Example Prompts

- "Call get_unread_emails with max_results=3 and show sender + subject."
- "Using the first email, call create_draft_reply with a polite reply body and return draft_id."
- "Revise the draft to be shorter and warmer (pass the same draft_id to update it)."

## Tests
```bash
uv run pytest -q
```

## Next Steps / Stretch Goals

If I had more time, I'd add:

- Simple importance scoring / prioritisation for unread emails
- Style guide + templates (Google Doc / Notion / local markdown)
- Better recipient handling (Reply-To, multiple recipients)
- Nicer reply formatting / quoting original message
- Support for multiple senders / "reply all"