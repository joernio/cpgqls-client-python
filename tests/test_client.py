import asyncio
from unittest.mock import Mock

import pytest

from cpgqls_client import CPGQLSClient


class MockCPGQLTransportConnection:
    def __init__(self, first_recv_msg, second_recv_msg):
        self._num_recv_msgs = 0
        self._first_recv_msg = first_recv_msg
        self._second_recv_msg = second_recv_msg

    def __await__(self):
        return self
        yield None # pylint: disable=unreachable

    async def recv(self):
        await asyncio.sleep(0)

        lock = asyncio.Lock()
        async with lock:
            msg = None
            if self._num_recv_msgs == 0:
                msg = self._first_recv_msg
            elif self._num_recv_msgs == 1:
                msg = self._second_recv_msg
            self._num_recv_msgs += 1
        return msg

    async def __aenter__(self):
        return await self

    async def __aexit__(self, exc_type, exc, transport):
        pass


class MockCPGQLSTransport:
    def __init__(self, conn, get_response, post_response):
        self._conn = conn
        self._get_response = get_response
        self._post_response = post_response

    def connect(self, *args, **kwargs):
        return self._conn

    def post(self, *args, **kwargs):
        return self._post_response

    def get(self, *args, **kwargs):
        return self._get_response


class ReturnParamsMockCPGQLSTransport:
    def __init__(self, conn):
        self._conn = conn
        self._last_post_response = None
        self._last_get_response = None

    def connect(self, *args, **kwargs):
        return self._conn

    def post(self, *args, **kwargs):
        other_params = {'json.return_value': {'uuid': 'one'}}
        self._last_post_response = Mock(status_code=200, kwargs=kwargs, **other_params)
        return self._last_post_response

    def get(self, *args, **kwargs):
        other_params = {'json.return_value': {'success': True}}
        self._last_get_response = Mock(status_code=200, kwargs=kwargs, **other_params)
        return self._last_get_response

    def last_get_response(self):
        return self._last_get_response

    def last_post_response(self):
        return self._last_post_response


def test_basic_execution():
    event_loop = asyncio.new_event_loop()
    conn = MockCPGQLTransportConnection("connected", "received")
    get_args = {'json.return_value':  {'uuid': 'one'}}
    get_response_mock = Mock(status_code=200, **get_args)
    post_args = {'json.return_value':  {'uuid': 'one'}}
    post_response_mock = Mock(status_code=200, **post_args)
    transport = MockCPGQLSTransport(conn, get_response_mock, post_response_mock)
    endpoint = "localhost:8080"
    client = CPGQLSClient(endpoint, event_loop=event_loop, transport=transport)
    result = client.execute("val a = 1")
    assert result == post_response_mock.json()


def test_get_response_not_200():
    event_loop = asyncio.new_event_loop()
    conn = MockCPGQLTransportConnection("connected", "received")
    get_args = {'json.return_value':  {'uuid': 'one'}}
    get_response_mock = Mock(status_code=400, **get_args)
    post_args = {'json.return_value':  {'uuid': 'one'}}
    post_response_mock = Mock(status_code=200, **post_args)
    transport = MockCPGQLSTransport(conn, get_response_mock, post_response_mock)
    endpoint = "localhost:8080"
    client = CPGQLSClient(endpoint, event_loop=event_loop, transport=transport)
    with pytest.raises(Exception):
        client.execute("val a = 1")


def test_basic_auth():
    event_loop = asyncio.new_event_loop()
    conn = MockCPGQLTransportConnection("connected", "received")
    transport = ReturnParamsMockCPGQLSTransport(conn)
    endpoint = "localhost:8080"
    auth_username = "username"
    auth_password = "password"
    client = CPGQLSClient(endpoint,
                          event_loop=event_loop,
                          transport=transport,
                          auth_credentials=(auth_username, auth_password))
    client.execute("val a = 1")

    # transport functions are called
    get_res = transport.last_get_response()
    post_res = transport.last_post_response()
    assert get_res is not None
    assert post_res is not None

    # correct auth args are set
    assert get_res.kwargs is not None
    assert post_res.kwargs is not None

    assert get_res.kwargs['auth'] is not None
    assert post_res.kwargs['auth'] is not None


    assert get_res.kwargs['auth'][0] is not None
    assert get_res.kwargs['auth'][1] is not None
    assert get_res.kwargs['auth'][0] is auth_username
    assert get_res.kwargs['auth'][1] is auth_password

    assert post_res.kwargs['auth'][0] is not None
    assert post_res.kwargs['auth'][1] is not None
    assert post_res.kwargs['auth'][0] is auth_username
    assert post_res.kwargs['auth'][1] is auth_password
