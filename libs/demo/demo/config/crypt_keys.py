#!/usr/bin/env python
# -*- coding: utf-8  -*-

from djangos.config import ConfigBase


class AmapClientKeys(ConfigBase):
    BASE = 0
    AMAP7 = BASE + 1

    DICT = [
        {
            "id": AMAP7,
            "aes_key": "LXlvWaosMcJCJwVn",
            "xxtea_key": "LXlvWaosMcJCJwVn",
        },
    ]
