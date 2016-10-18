#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
from optparse import make_option

from Crypto.PublicKey import RSA
from django.core.management.base import BaseCommand

from .....common.crypt import random_str


def gen_rsa_key():
    return RSA.generate(1024, os.urandom)


class Command(BaseCommand):
    help = 'A simple key generator.'

    option_list = (
        make_option('-t', '--type', action="store",
                    dest="type", help="Should be one of aes/channel/rsa"),
    ) + BaseCommand.option_list

    def handle(self, *args, **options):
        type_ = options['type']
        stdout = self.stdout
        if type_ == 'rsa':
            key = gen_rsa_key()
            stdout.write('\nPublic key:\n\n')
            stdout.write(repr(key.publickey().exportKey('PEM')))
            stdout.write('\nPrivate key:\n\n')
            stdout.write(repr(key.exportKey('PEM')))
        elif type_ == 'aes':
            stdout.write('\nNew aes key:\n\n')
            stdout.write(random_str(16))
        elif type_ == 'channel':
            stdout.write('\nNew channel key:\n\n')
            stdout.write(random_str(32))
        else:
            stdout.write(self.style.ERROR('Must specify a type!, append `-h` for more details.'))
        stdout.write('\n')
