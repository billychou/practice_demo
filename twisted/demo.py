#!/usr/bin/env python

from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory
from twisted.internet import reactor

class Echo(Protocol):
    def dataReceived(self, data):
        self.transport.write(data)

class EchoFactory(Factory):
    protocol = Echo
    def __init__(self, quote=None):
        self.quote = quote or "An apple a day keeps"    


reactor.listenTCP(8123,EchoFactory())
reactor.run()
