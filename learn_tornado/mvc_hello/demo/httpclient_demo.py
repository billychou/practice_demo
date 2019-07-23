#!/usr/bin/env python
#-*-coding: utf-8-*-
__author__ = "songchuan.zhou"
__email__ = "zsc1528@gmail.com"
from tornado.httpclient import HTTPClient
from tornado.concurrent import Future
from tornado.httpclient import AsyncHTTPClient


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
    fetch_future = http_client.fetch(url)
    fetch_future.add_done_callback(
        lambda f: my_future.set_result(f.result())
    )
    return my_future.result()


def mycallback(a):
    print(a)


if __name__ == "__main__":
    #result = synchronous_fetch("http://m5.amap.com/ws/valueadded/deepinfo/search/?poiid=B0FFFYPI2X&sign=631DC142633197660026CB0A11F29547&output=json&version=2.12&channel=mo_openapi&mode=255&cms_ver=6&deepcount=1&sourcefrom=loadrunner_test")
    #print(result)
    result = async_fetch_future("http://m5.amap.com/ws/valueadded/deepinfo/search/?poiid=B0FFFYPI2X&sign=631C142633197660026CB0A11F29547&output=json&version=2.12&channel=mo_openapi&mode=255&cms_ver=6&deepcount=1&sourcefrom=loadrunner_test")
    print(result)