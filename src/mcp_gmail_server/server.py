from typing import Any, Dict, List

from googleapiclient.discovery import build
from mcp.server.fastmcp import FastMCP

from mcp_gmail_server.auth import SCOPES, get_credentials
from mcp_gmail_server.gmail_client import (
    list_unread_emails,
    create_draft_reply as gmail_create_draft_reply,
)

"""

Module to make MCP server

Purpose: 
Create an MCP server (FastMCP)
Register tools so Claude can call them
For each tool call:
- (auth → Gmail API → use gmail_client functions)
- return JSON-serializable results (list/dict)
"""

# make server first
mcp = FastMCP(name="Gmail MCP Server", json_response=True)


@mcp.tool()
def get_unread_emails(max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Return unread emails from the user's Gmail inbox, excluding spam, promotions, and social categories.

    Args:
        max_results (int): Maximum number of unread emails to fetch. Default is 5.
    """
    creds = get_credentials(SCOPES)
    service = build("gmail", "v1", credentials=creds)

    return list_unread_emails(service, max_results=max_results)

@mcp.tool()
def create_draft_reply(
    thread_id: str,
    rfc_message_id: str,
    to_addr: str,
    subject: str,
    reply_body: str,
    draft_id: str | None = None
) -> Dict[str, Any]:
    
    """
    Create a correctly-threaded draft reply in Gmail.

    Args:
    thread_id: Gmail thread ID from get_unread_emails
    rfc_message_id: Message-ID header from get_unread_emails (used for In-Reply-To/References)
    to_addr: recipient email address (use sender email)
    subject: original subject (tool will use it as-is; include 'Re:' if desired)
    reply_body: plain-text body for the reply
    """
    creds = get_credentials(SCOPES)
    service = build("gmail", "v1", credentials=creds)
    return gmail_create_draft_reply(service, thread_id, rfc_message_id, to_addr, subject, reply_body)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
