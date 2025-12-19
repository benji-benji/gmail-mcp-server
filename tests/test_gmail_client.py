from mcp_gmail_server.gmail_client import list_unread_message_ids


class _ExecuteStub:
    def __init__(self, payload):
        self._payload = payload

    def execute(self):
        return self._payload


class _ListCallStub:
    def __init__(self, payload, capture):
        self._payload = payload
        self._capture = capture

    def list(self, **kwargs):
        # capture the args passed to Gmail API call
        self._capture.update(kwargs)
        return _ExecuteStub(self._payload)


class _MessagesStub:
    def __init__(self, payload, capture):
        self._payload = payload
        self._capture = capture

    def messages(self):
        return _ListCallStub(self._payload, self._capture)


class _UsersStub:
    def __init__(self, payload, capture):
        self._payload = payload
        self._capture = capture

    def users(self):
        return _MessagesStub(self._payload, self._capture)


def test_list_unread_message_ids_returns_messages_and_uses_expected_filters():
    capture = {}

    fake_payload = {
        "messages": [{"id": "abc", "threadId": "t1"}, {"id": "def", "threadId": "t2"}]
    }
    service = _UsersStub(fake_payload, capture)

    out = list_unread_message_ids(service, max_results=2)

    assert out == fake_payload["messages"]

    # Check we passed the important filters
    assert capture["userId"] == "me"
    assert capture["labelIds"] == ["INBOX", "UNREAD"]
    assert capture["maxResults"] == 2
    assert "q" in capture  # your exclusion query
