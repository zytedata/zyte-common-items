import base64

import pytest

from zyte_common_items import Header, Request


def test_request_no_kwargs():
    req = Request("http://example.com")
    assert req.url == "http://example.com"
    assert req.method == "GET"
    assert req.body is None
    assert req.body_bytes is None
    assert req.headers is None


def test_request_body_bytes():
    body = base64.b64encode(b"request body").decode()
    req = Request("http://example.com", body=body, method="POST")
    assert req.method == "POST"
    assert req.body == body
    assert req.body_bytes == b"request body"


def test_request_to_scrapy_basic():
    scrapy = pytest.importorskip("scrapy")
    req = Request("http://example.com")
    scrapy_req = req.to_scrapy(None)

    assert isinstance(scrapy_req, scrapy.Request)
    assert scrapy_req.url == "http://example.com"
    assert scrapy_req.method == "GET"
    assert scrapy_req.callback is None


def test_request_to_scrapy_complex():
    scrapy = pytest.importorskip("scrapy")

    def callback():
        pass

    body = base64.b64encode(b"request body").decode()
    headers = [Header(name="Header", value="Value")]

    req = Request(
        "http://example.com",
        headers=headers,
        body=body,
        method="POST",
        name="link name",
    )

    scrapy_req = req.to_scrapy(callback=callback, meta={"foo": "bar"}, priority=5)

    assert isinstance(scrapy_req, scrapy.Request)
    assert scrapy_req.url == "http://example.com"
    assert scrapy_req.meta == {"foo": "bar"}
    assert scrapy_req.method == "POST"
    assert scrapy_req.callback is callback
    assert scrapy_req.body == b"request body"
    assert scrapy_req.headers["Header"] == b"Value"
    assert scrapy_req.priority == 5


def test_request_to_scrapy_headers_with_the_same_name():
    pytest.importorskip("scrapy")

    headers = [Header(name="name", value="value1"), Header(name="name", value="value2")]

    req = Request("http://example.com", headers=headers)
    scrapy_req = req.to_scrapy(callback=None)
    assert scrapy_req.headers.getlist("name") == [b"value1", b"value2"]
