#!/usr/bin/env python
# -*- coding: utf-8  -*-

from xml.parsers import expat
import xmltodict


def parse(xml_input, encoding=None, expat=expat, process_namespaces=False,
          namespace_separator=':', **kwargs):
    ill_encodes = ['gbk', ]
    if isinstance(xml_input, str):
        for encode in ill_encodes:
            header = '<?xml version="1.0" encoding="%s"' % encode
            if xml_input.startswith(header):
                xml_input = xml_input.decode(encode).encode('utf-8')
                xml_input = xml_input.replace(header, '<?xml version="1.0" encoding="utf-8"', 1)

    return xmltodict.parse(xml_input, encoding=encoding, expat=expat, process_namespaces=process_namespaces,
                           namespace_separator=namespace_separator, **kwargs)
