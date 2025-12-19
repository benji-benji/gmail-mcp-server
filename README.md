# gmail-mcp-server

# pre-requisities
- google workspace account (with gmail enabled)
- Python 3.12
- uv (install via https://github.com/astral-sh/uv)

# security 
This repo does not contain any Google credentials or tokens. 

Local only files (ignored by git)
- credentials.json OAuth client secret downloaded from Google Cloud
- token.json generated locally when authenticating for the first time

Make sure you do not commit these files. 

# google Oauth setup (gmail API)
1. Create a Google Cloud project (https://console.cloud.google.com/).
2. Enable the gmail API for your project 
3. Configure OAuth consent screen 
4. Create OAuth Client ID (Desktop App recommended for local dev)
5. Download the client JSON and save it as `credentials.json` in the project root directory.
6. Scopes used:
   - gmail.readonly
   - gmail.compose


PSEUDOCODE: 

gmail_client.py : 
- authenticate user via OAuth 
- store token locally 
- define what info to extract from emails: From, Subject, Date, Body, Message-Id 
- define user parameters ( eg. max results) 
- list_message_refs - get the message IDs
- get_message_metadata - get the info from one message 
- info_to_dict - convert the info to a dictionary 
- create_snippet - build object {snippet}
- normalise_message - build object {from , subject, date, snippet, message-id}
# Do I need Thread ID? 
- list_unread_emails - get the unread emails, normalise them, return as list of dicts
# to add: create_draft_reply + threading 