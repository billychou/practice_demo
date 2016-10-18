#!/usr/bin/env python
# -*- coding: utf-8  -*-

"""
aos channel
"""

from ...common.config import CHANNELS
from . import ConfigBase


class ChannelConf(ConfigBase):
    CONF_MANAGER = None  # CONF_MANAGER为None时使用配置文件

    DATA = {channel.get('channel'): channel for channel in CHANNELS}
