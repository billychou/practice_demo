#!/usr/bin/env python
# -*- coding: UTF-8 -*-


class FakeUser(object):

    is_staff = False
    is_active = True
    is_superuser = False

    def __init__(self, id, username='username', nickname='nickname'):
        self.id = self.pk = id
        self.username = username
        self.nickname = nickname

    def __str__(self):
        return 'FakeUser'

    def save(self):
        pass

    def set_password(self, new_password):
        pass

    def is_authenticated(self):
        return True
