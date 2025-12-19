import base64
from email.message import EmailMessage

from googleapiclient.discovery import build

from mcp_gmail_server.auth import SCOPES, get_credentials
from mcp_gmail_server.gmail_client import list_unread_emails


def b64url_encode(message_bytes: bytes) -> str:
    return base64.urlsafe_b64encode(message_bytes).decode("utf-8")


def build_reply_raw(to_addr: str, subject: str, in_reply_to: str, body: str) -> str:
    msg = EmailMessage()
    msg["To"] = to_addr
    msg["Subject"] = subject if subject.lower().startswith("re:") else f"Re: {subject}"
    msg["In-Reply-To"] = in_reply_to
    msg["References"] = in_reply_to
    msg.set_content(body)

    return b64url_encode(msg.as_bytes())


def main():
    creds = get_credentials(SCOPES)  # make sure SCOPES includes gmail.compose now
    service = build("gmail", "v1", credentials=creds)

    emails = list_unread_emails(service, max_results=1)
    if not emails:
        print("No unread emails to draft against.")
        return

    e = emails[0]
    raw = build_reply_raw(
        to_addr=e["from_"],                     # MVP: use From as To (we’ll refine)
        subject=e["subject"],
        in_reply_to=e["rfc_message_id"],
        body="Hi — quick reply draft from my MCP server.\n\nThanks,\nBenji",
    )

    draft = (
        service.users()
        .drafts()
        .create(
            userId="me",
            body={"message": {"raw": raw, "threadId": e["thread_id"]}},
        )
        .execute()
    )

    print("Draft created!")
    print("draftId:", draft.get("id"))
    print("threadId:", draft.get("message", {}).get("threadId"))


if __name__ == "__main__":
    main()
