from typing import Dict, List

""" 
// Module to interact with Gmail API // 

Purpose: 
1. Gets unread emails and extracts relevant info.
2. Handles emails: Find, Fetch, Parse, Normalise, Return list of dicts.
3. Create draft reply + threading.

PSEUDOCODE / PLAN: 

- define what email labels to use: INBOX, UNREAD not TRASH, SPAM, PROMOTIONS, SOCIAL 
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

"""

# output schema:
# message_id (Gmail internal ID)
# thread_id (Gmail internal thread ID)
# from_ (string) ( single email add / list of email addresses? )
# subject (string)
# snippet (sting)
# date (string)

# exclusions
# exclude TRASH, SPAM, PROMOTIONS, SOCIAL

EXCLUDE_LABELS = "-in:spam -category:promotions -category:social -in:trash"


def list_unread_message_ids(service, max_results: int = 10) -> List[Dict[str, str]]:
    """
    Returns a list of {"id": "...", "threadId": "..."} objects from Gmail.
    """
    resp = (
        service.users()
        .messages()
        .list(
            userId="me",
            labelIds=["INBOX", "UNREAD"],
            q=EXCLUDE_LABELS,
            maxResults=max_results,
        )
        .execute()
    )
    return resp.get("messages", [])
