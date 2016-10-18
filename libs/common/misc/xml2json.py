#!/usr/bin/env python
# -*- coding: utf-8  -*-

__author__ = 'qingyun.meng'

"""
Created by qingyun.meng on 202014/9/15.
Modify by: qingyun.meng
Description: 
"""

import xml.etree.cElementTree as ET
import json

def elem_to_internal(elem,strip=1):
    """Convert an Element into an internal dictionary (not JSON!)."""
    d = {}
    for key, value in elem.attrib.items():
        d['@'+key] = value

    # loop over subelements to merge them
    for subelem in elem:
        v = elem_to_internal(subelem,strip=strip)
        tag = subelem.tag
        value = v[tag]
        try:
            # add to existing list for this tag
            d[tag].append(value)
        except AttributeError:
            # turn existing entry into a list
            d[tag] = [d[tag], value]
        except KeyError:
            # add a new non-list entry
            d[tag] = value
    text = elem.text
    tail = elem.tail
    if strip:
        # ignore leading and trailing whitespace
        if text: text = text.strip()
        if tail: tail = tail.strip()

    if tail:
        d['#tail'] = tail

    if d:
        # use #text element if other attributes exist
        if text: d["#text"] = text
    else:
        # text is the value if no attributes
        #d = text or None
        d = text or ""  #2012-07-04 Change None to ""
    return {elem.tag: d}

def internal_to_elem(pfsh, factory=ET.Element):
    """Convert an internal dictionary (not JSON!) into an Element.

    Whatever Element implementation we could import will be
    used by default; if you want to use something else, pass the
    Element class as the factory parameter.
    """
    attribs = {}
    text = None
    tail = None
    sublist = []
    tag = pfsh.keys()
    if len(tag) != 1:
        raise ValueError("Illegal structure with multiple tags: %s" % tag)
    tag = tag[0]
    value = pfsh[tag]
    if isinstance(value,dict):
        for k, v in value.items():
            if k[:1] == "@":
                attribs[k[1:]] = v
            elif k == "#text":
                text = v
            elif k == "#tail":
                tail = v
            elif isinstance(v, list):
                for v2 in v:
                    sublist.append(internal_to_elem({k:v2},factory=factory))
            else:
                sublist.append(internal_to_elem({k:v},factory=factory))
    else:
        text = value
    e = factory(tag, attribs)
    for sub in sublist:
        e.append(sub)
    e.text = text
    e.tail = tail
    return e

def elem2json(elem, strip=1):
    """Convert an ElementTree or Element into a JSON string."""
    if hasattr(elem, 'getroot'):
        elem = elem.getroot()
    return json.dumps(elem_to_internal(elem,strip=strip))

def json2elem(json, factory=ET.Element):
    """Convert a JSON string into an Element.

    Whatever Element implementation we could import will be used by
    default; if you want to use something else, pass the Element class
    as the factory parameter.
    """
    return internal_to_elem(json.loads(json), factory)


def xml2json(xmlstring,strip=1):
    """Convert an XML string into a JSON string."""
    elem = ET.fromstring(xmlstring.encode("utf-8"))
    return elem2json(elem,strip=strip)

def json2xml(json, factory=ET.Element):
    """Convert a JSON string into an XML string.

    Whatever Element implementation we could import will be used by
    default; if you want to use something else, pass the Element class
    as the factory parameter.
    """
    elem = internal_to_elem(json.loads(json), factory)
    return ET.tostring(elem)

# sample:
# >>> Xml2Json('<doc><tag><subtag>data</subtag><t>data1</t><t>data2</t></tag></doc>').result
# {u'doc': {u'tag': {u'subtag': u'data', u't': [u'data1', u'data2']}}}
# >>> xml2json('<doc><tag><subtag>data</subtag><t>data1</t><t>data2</t></tag></doc>', strip = 0)
