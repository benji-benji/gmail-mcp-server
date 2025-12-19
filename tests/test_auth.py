import os

import pytest

from mcp_gmail_server.auth import SCOPES, get_credentials



def test_get_credentials_uses_existing_token():
    # Skip if you haven't generated token.json yet
    if not os.path.exists("token.json"):
        pytest.skip("token.json not found; run auth once to generate it")


    creds = get_credentials(SCOPES)

    assert creds is not None
    assert getattr(creds, "valid", True) is True
