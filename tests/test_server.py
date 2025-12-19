import base64
from email import policy
from email.parser import BytesParser

from mcp_gmail_server.gmail_client import normalise_message, build_reply_raw


def test_normalise_message_maps_expected_fields():
    raw_message = {
        "id": "gmail_msg_123",
        "threadId": "gmail_thread_456",
        "snippet": "Hello there, this is a snippet.",
        "payload": {
            "headers": [
                {"name": "From", "value": "Alice Example <alice@example.com>"},
                {"name": "Subject", "value": "Test subject"},
                {"name": "Date", "value": "Fri, 19 Dec 2025 12:00:00 +0000"},
                {"name": "Message-ID", "value": "<abc123@example.com>"},
            ]
        },
    }

    out = normalise_message(raw_message)

    # required keys exist
    for k in [
        "message_id",
        "thread_id",
        "from_",
        "subject",
        "date",
        "snippet",
        "rfc_message_id",
    ]:
        assert k in out

    # values map correctly
    assert out["message_id"] == "gmail_msg_123"
    assert out["thread_id"] == "gmail_thread_456"
    assert out["from_"] == "Alice Example <alice@example.com>"
    assert out["subject"] == "Test subject"
    assert out["date"] == "Fri, 19 Dec 2025 12:00:00 +0000"
    assert out["snippet"] == "Hello there, this is a snippet."
    assert out["rfc_message_id"] == "<abc123@example.com>"


def test_build_reply_raw_contains_threading_headers_and_body():
    to_addr = "alice@example.com"
    subject = "Hello"
    in_reply_to = "<abc123@example.com>"
    body = "Thanks — drafting via MCP."

    raw_b64 = build_reply_raw(
        to_addr=to_addr,
        subject=subject,
        in_reply_to=in_reply_to,
        body=body,
    )

    # decode base64url -> bytes -> parse email
    msg_bytes = base64.urlsafe_b64decode(raw_b64.encode("utf-8"))
    msg = BytesParser(policy=policy.default).parsebytes(msg_bytes)

    assert msg["To"] == to_addr
    assert msg["Subject"].startswith("Re:")
    assert msg["Subject"] == f"Re: {subject}"
    assert msg["In-Reply-To"] == in_reply_to
    assert msg["References"] == in_reply_to

    # body content
    assert body in msg.get_content()
