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
REQUIRED_LABELS = ["INBOX", "UNREAD"]
METADATA_HEADERS = ["From", "Subject", "Date", "Message-ID"]

def list_unread_message_ids(service, max_results: int = 10) -> List[Dict[str, str]]:
    """
    Returns a list of {"id": "...", "threadId": "..."} objects from Gmail.
    """
    resp = (
        service.users()
        .messages()
        .list(
            userId="me",
            labelIds=REQUIRED_LABELS,
            q=EXCLUDE_LABELS,
            maxResults=max_results,
        )
        .execute()
    )
    return resp.get("messages", [])

def get_message_metadata(service, message_id: str) -> Dict:
    """
    Fetches metadata for a single message by ID.
    """
    message = (
        service.users()
        .messages()
        .get(userId="me", id=message_id, format="metadata", metadataHeaders=METADATA_HEADERS)
        .execute()
    )
    return message

def info_to_dict(headers_list: List[Dict[str, str]]) -> Dict[str, str]:
    """
    Converts a list of header dicts to a single dict.
    """
    return {header["name"]: header["value"] for header in headers_list}

def normalise_message(message: Dict) -> Dict:
    """
    Normalises a raw Gmail message into our schema.
    """
    payload = message.get("payload", {})
    headers_list = payload.get("headers", [])
    header_dict = info_to_dict(headers_list)    
    
    
    from_ = header_dict.get("From", "")
    subject = header_dict.get("Subject", "")
    date = header_dict.get("Date", "")
    message_id = header_dict.get("Message-ID", "")

    snippet = message.get("snippet", "")

    return {
        "message_id": message.get("id", ""),
        "thread_id": message.get("threadId", ""),
        "from_": from_,
        "subject": subject,
        "date": date,
        "snippet": snippet,
        "rfc_message_id": message_id,
    }
    
def list_unread_emails(service, max_results: int = 10) -> List[Dict]:
    """
    Lists unread emails, normalises them, and returns as a list of dicts.
    """
    message_refs = list_unread_message_ids(service, max_results=max_results)
    emails = []

    for ref in message_refs:
        msg_id = ref.get("id")
        if not msg_id:
            continue

        raw_message = get_message_metadata(service, msg_id)
        normalised = normalise_message(raw_message)
        emails.append(normalised)

    return emails

