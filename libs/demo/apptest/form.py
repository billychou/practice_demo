#!/usr/bin/env python
# -*- coding: utf-8  -*-
from django_dist import borm


class _FormValidator(object):
    def validate_name(self, model, value, field_obj):
        if not value:
            raise borm.ValidateError('param:name must be given.')

    def validate_id(self, model, value, field_obj):
        if not value:
            raise borm.ValidateError('param:id must be given.')


class Base(borm.BOModel):
    channel = borm.StringField(required=True)


class TestApi(Base):
    __validator__ = _FormValidator()

    name = borm.StringField(required=True)
    id = borm.IntegerField()
