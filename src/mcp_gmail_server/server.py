from typing import Any, Dict, List

from googleapiclient.discovery import build
from mcp.server.fastmcp import FastMCP

from mcp_gmail_server.auth import SCOPES, get_credentials
from mcp_gmail_server.gmail_client import list_unread_emails

'''

// Module to nake MCP server // 

Purpose: 
Create an MCP server (FastMCP)
Register tools so Claude can call them
For each tool call:
- (auth → Gmail API → use gmail_client functions)
- return JSON-serializable results (list/dict)
'''

# make server first 
mcp = FastMCP(
    name="Gmail MCP Server", json_response=True) 

@mcp.tool()
def get_unread_inbox_emails(max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Return unread emails from the user's Gmail inbox, excluding spam, promotions, and social categories.

    Args:
        max_results (int): Maximum number of unread emails to fetch. Default is 5.
    """
    creds = get_credentials(SCOPES)
    service = build("gmail", "v1", credentials=creds)

    return list_unread_emails(service, max_results=max_results)

def main():
    mcp.run()

if __name__ == "__main__":
    main()