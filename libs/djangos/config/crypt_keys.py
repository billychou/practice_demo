#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''各种密钥'''

from ...common.config import ConfigBase


class AmapClientKeys(ConfigBase):
    BASE = 0
    AMAP7 = BASE + 1  # amap7 android/ios请求使用AES加密

    DATA = [
        {
            "id": AMAP7,
            "aes_key": "LXlvWaosMcJCJwVn",
            "xxtea_key": "LXlvWaosMcJCJwVn",
        },
    ]
