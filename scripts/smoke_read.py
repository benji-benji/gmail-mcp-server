from googleapiclient.discovery import build

from mcp_gmail_server.auth import SCOPES, get_credentials
from mcp_gmail_server.gmail_client import list_unread_message_ids, get_message_metadata, info_to_dict, normalise_message

def main():
    creds = get_credentials(SCOPES)
    service = build("gmail", "v1", credentials=creds)

    refs = list_unread_message_ids(service, max_results=1)
    print("refs:", refs)

    if not refs:
        print("No unread inbox messages.")
        return

    msg_id = refs[0]["id"]
    msg = get_message_metadata(service, msg_id)

    print("id:", msg.get("id"))
    print("threadId:", msg.get("threadId"))
    print("snippet:", msg.get("snippet", "")[:120])
    print("headers:", msg.get("payload", {}).get("headers", []))
    # check header to list is working
    headers_list = msg.get("payload", {}).get("headers", [])
    headers_dict = info_to_dict(headers_list)

    print("From:", headers_dict.get("From", ""))
    print("Subject:", headers_dict.get("Subject", ""))
    
    email = normalise_message(msg)
    print(email["from_"])
    print(email["subject"])
    print(email["snippet"][:120])
    print(email["message_id"], email["thread_id"])


if __name__ == "__main__":
    main()
