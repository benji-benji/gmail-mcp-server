import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def main():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("gmail", "v1", credentials=creds)

        results = (
            service.users()
            .messages()
            .list(userId="me", labelIds=["INBOX", "UNREAD"], maxResults=1)
            .execute()
        )

        messages = results.get("messages", [])

        if not messages:
            print("No messages found.")
            return

        msg_id = messages[0]["id"]
        print(f"Found 1 message. id={msg_id}")

        msg = (
            service.users()
            .messages()
            .get(
                userId="me",
                id=msg_id,
                format="metadata",
                metadataHeaders=["From", "Subject", "Date"],
            )
            .execute()
        )

        headers = {
            h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])
        }
        print("From:", headers.get("From", ""))
        print("Subject:", headers.get("Subject", ""))
        print("Date:", headers.get("Date", ""))
        print("Snippet:", msg.get("snippet", ""))
        print("Thread ID:", msg.get("threadId", ""))

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
