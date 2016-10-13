#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms

from .. import ParamError


class BaseForm(forms.Form):
    """基础Form"""

    def clean(self):
        '''参数校验不通过，直接返回参数错误，并把校验不通过的信息写到message'''
        cleaned_data = super(BaseForm, self).clean()
        if self.errors:
            raise ParamError(msg=self.errors.as_json())

        return cleaned_data
