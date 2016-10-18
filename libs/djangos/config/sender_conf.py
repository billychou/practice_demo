#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''短信、邮箱相关配置'''

from ...common.config import ConfigBase


# 淘宝消息中心(MC) WebServices

class TaobaoSMSTemplateConfig(ConfigBase):
    VERIFYCODE = 1
    TAXIVERIFY = 2
    REGISTER = 3
    MYPOSITION = 4
    BUSLINE = 5
    ROUTE_FOOT = 6
    ROUTE_BUS = 7
    ROUTE_AUTO = 8
    POI_POS = 9
    MAP_CLICK = 10

    DATA = [
        {
            "id": VERIFYCODE,  # 手机号码验证
            "source_id": "aos-sns*verifycode",
            "message_type_id": "260456294",
            "template_id": "730818448",
            "keywords": ['code'],
            "template_content": u"验证码：{code}，如非本人操作，请忽略本短信。",  # 仅供展示，不使用
        },
        {
            "id": TAXIVERIFY,  # 打车手机号码验证
            "source_id": "aos-sns*taxiverify",
            "message_type_id": "520415310",
            "template_id": "720745859",
            "keywords": ['code'],
            "template_content": u"验证码：{code}，您正在使用叫车服务，如非本人操作，请忽略本短信。",  # 仅供展示，不使用
        },
        {
            "id": REGISTER,  # 手机号快速创建账号
            "source_id": "aos-sns*register",
            "message_type_id": "770273899",
            "template_id": "520117650",
            "keywords": ['phone', 'code'],
            "template_content": u"您已成功创建高德账号，登录账号为您的手机号：{phone}，密码为：{code}",  # 仅供展示，不使用
        },
        {
            "id": MYPOSITION,  # 我的位置分享
            "source_id": "aos-sns*myposition",
            "message_type_id": "330652805",
            "template_id": "260973338",
            "keywords": ['name', 'shortaddress'],
            "value_limit": {'name': 23, 'shortaddress': 25},
            "template_content": u"【我的位置】：{name}，详情请见：{shortaddress}",
        },
        {
            "id": BUSLINE,  # 公交线路信息分享
            "source_id": "aos-sns*busline",
            "message_type_id": "620397010",
            "template_id": "350717911",
            "keywords": ['busnumber', 'description', 'shortaddress'],
            "value_limit": {'description': 23, 'shortaddress': 25},
            "template_content": u"{busnumber}，{description}，详细请见：{shortaddress}",
        },
        {
            "id": ROUTE_FOOT,  # 步行线路分享
            "source_id": "aos-sns*route_foot",
            "message_type_id": "480153386",
            "template_id": "370123737",
            "keywords": ['description', 'shortaddress'],
            "value_limit": {'description': 23, 'shortaddress': 25},
            "template_content": u"步行线路：{description}，详细请见：{shortaddress}",
        },
        {
            "id": ROUTE_BUS,  # 公交换乘方案分享
            "source_id": "aos-sns*route_bus",
            "message_type_id": "750881625",
            "template_id": "700145259",
            "keywords": ['description', 'shortaddress'],
            "value_limit": {'description': 23, 'shortaddress': 25},
            "template_content": u"公交线路：{description}，详细请见：{shortaddress}",
        },
        {
            "id": ROUTE_AUTO,  # 驾车换乘方案分享
            "source_id": "aos-sns*route_auto",
            "message_type_id": "480183017",
            "template_id": "520165363",
            "keywords": ['description', 'shortaddress'],
            "value_limit": {'description': 23, 'shortaddress': 25},
            "template_content": u"驾车线路：{description}，详细请见：{shortaddress}",
        },
        {
            "id": POI_POS,  # poi位置分享
            "source_id": "aos-sns*poi_pos",
            "message_type_id": "340120590",
            "template_id": "450903705",
            "keywords": ['name', 'address', 'shortaddress'],
            "value_limit": {'name': 15, 'address': 14, 'shortaddress': 25},  # address 留一位给，

            "template_content": u"【{name}】：{address}详情请见：{shortaddress}",
        },
        {
            "id": MAP_CLICK,  # 地图选点位置分享
            "source_id": "aos-sns*map_click",
            "message_type_id": "340607214",
            "template_id": "370554145",
            "keywords": ['name', 'address', 'shortaddress'],
            "value_limit": {'name': 15, 'address': 14, 'shortaddress': 25},  # address 留一位给，
            "template_content": u"【{name}】：{address}详情请见：{shortaddress}",
        }
    ]

# EMAIL  SMTP SETTINGS -- 完全兼容Django settings配置