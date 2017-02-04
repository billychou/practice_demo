#!/usr/bin/env python

from tornado.httpclient import HTTPClient
from tornado.httpclient import AsyncHTTPClient
from tornado.concurrent import Future
from tornado import gen

def synchronous_fetch(url):
    http_client = HTTPClient()
    response = http_client.fetch(url)
    return response.body


def asynchronous_fetch(url, callback):
    http_client = AsyncHTTPClient()

    def handle_response(response):
        callback(response.body)
    http_client.fetch(url, callback=handle_response)


def async_fetch_future(url):
    http_client = AsyncHTTPClient()
    my_future = Future()
    http_client = AsyncHTTPClient()
    my_future = Future()





if __name__ == "__main__":
    synchronous_fetch("http://www.bestyikao.com")
