from googleapiclient.discovery import build

from mcp_gmail_server.auth import SCOPES, get_credentials
from mcp_gmail_server.gmail_client import list_unread_emails



def main():
    creds = get_credentials(SCOPES)
    service = build("gmail", "v1", credentials=creds)

    emails = list_unread_emails(service, max_results=3)

    print(f"Found {len(emails)} unread inbox emails (excluding spam/promotions/social).")

    if not emails:
        return

    for i, e in enumerate(emails, start=1):
        print(f"\n[{i}] {e.get('from_', '')}")
        print(f"Subject: {e.get('subject', '')}")
        print(f"Snippet: {e.get('snippet', '')[:120]}")
        print(f"IDs: message_id={e.get('message_id', '')} thread_id={e.get('thread_id', '')}")


if __name__ == "__main__":
    main()  
