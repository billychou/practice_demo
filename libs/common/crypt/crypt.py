#!/usr/bin/env python
# -*- coding: utf-8  -*-

'''
加密、解密类库
'''

from Crypto import Random
from base64 import b64encode, b64decode, b32encode, b32decode, encodestring, decodestring
import string
from Crypto.Random import random
from Crypto.Cipher import AES
from Crypto.Cipher import DES
from Crypto.Cipher import Blowfish
from .xxtea import (decrypt as xxt_decrypt,
                    encrypt as xxt_encrypt)


def random_str(length=8):
    '''生成可打印的 [0-9a-zA-Z] 随机字符串.'''
    seeds = string.letters + string.digits
    random_str = ''
    for x in xrange(length):
        random_str += random.choice(seeds)
    return random_str


def cryptString(secret, plain):
    '''只有CM在使用，以后不要再使用'''
    obj = Blowfish.new(secret, Blowfish.MODE_ECB)
    randstring = str.join(
        '', random.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890', 12))
    split = random.randrange(10) + 1
    s = randstring[:split] + ':valid:' + plain + ':valid:' + randstring[split:]
    length = len(s)

    l = length + 8 - (length % 8)
    padded = s + " " * (8 - length % 8)

    ciph = obj.encrypt(padded[:l])
    try:
        return b32encode(ciph)
    except NameError:
        return encodestring(ciph)


def decryptString(secret, cipher):
    '''只有CM在使用，以后不要再使用'''
    obj = Blowfish.new(secret, Blowfish.MODE_ECB)
    try:
        ciph = b32decode(cipher)
    except NameError:
        ciph = decodestring(cipher)
    except TypeError:
        return None

    plaintext = obj.decrypt(ciph)
    try:
        (c1, plain, c2) = plaintext.split(":valid:")
    except ValueError:
        return None
    return plain


def aes_encrypt(plaintext, key, iv=None, flag="raw"):
    """ AES-128bit/MODE_CBC/PKCS7Padding

    @ plaintext -- 明文
    @ key -- 密钥
    @ iv -- None时随机，[a-zA-Z0-9]

    returns:
        (cipher, iv)
    """
    def pad(s):
        x = AES.block_size - len(s) % AES.block_size
        return s + (chr(x) * x)

    try:
        padded_plaintext = pad(plaintext)

        if iv is None:
            iv = random_str(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)

        encrypted, iv_ = cipher.encrypt(padded_plaintext), iv

        if "base64" == flag:
            encrypted = b64encode(encrypted)

        return encrypted, iv_
    except Exception:
        return None, ''


def aes_decrypt(ciphertext, key, iv, flag="raw"):
    """ AES-128bit/MODE_CBC/PKCS7Padding

    @ plaintext -- 密文
    @ key -- 密钥
    @ iv -- iv
    returns:
        plaintext
    """
    def unpad(s):
        return s[:-ord(s[-1])]

    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        if "base64" == flag:
            ciphertext = b64decode(ciphertext)
        plaintext = unpad(cipher.decrypt(ciphertext))
        return plaintext
    except Exception:
        return None


def aes_encrypt_base64(plaintext, key, iv=None):
    return aes_encrypt(plaintext, key, iv, flag='base64')


def aes_decrypt_base64(ciphertext, key, iv):
    return aes_decrypt(ciphertext, key, iv, flag='base64')


def aes_cbc_encrypt_base64(plaintext, key):
    '''iv嵌入到密文头部，再做base64编码的aes-cbc加密'''
    try:
        iv = Random.new().read(AES.block_size)
        ciphertext = aes_encrypt(plaintext, key, iv)[0]
        return b64encode(iv + ciphertext)
    except Exception:
        return None


def aes_cbc_decrypt_base64(ciphertext, key):
    '''iv嵌入到密文头部，再做base64编码的aes-cbc解密'''
    try:
        decoded = b64decode(ciphertext)
        iv, ciphertext = decoded[:AES.block_size], decoded[AES.block_size:]
        return aes_decrypt(ciphertext, key, iv)
    except Exception:
        return None


def des_encrypt(plaintext, key, flag="raw"):
    def pad(s):
        x = DES.block_size - len(s) % DES.block_size
        return s + (chr(x) * x)

    padded_plaintext = pad(plaintext)
    cipher = DES.new(key)
    encrypted = cipher.encrypt(padded_plaintext)
    if "base64" == flag:
        encrypted = b64encode(encrypted)

    return encrypted


def des_decrypt(ciphertext, key, flag="raw"):
    def unpad(s):
        return s[:-ord(s[-1])]

    if "base64" == flag:
        ciphertext = b64decode(ciphertext)
    cipher = DES.new(key)
    plaintext = unpad(cipher.decrypt(ciphertext))

    return plaintext


def xxtea_encrypt(plaintext, key, flag="base64", is_bin=False):
    try:
        if is_bin:
            pass
        else:
            cipher = xxt_encrypt(plaintext, key)
        if flag == "base64":
            cipher = b64encode(cipher)
        return cipher
    except Exception:
        return None


def xxtea_decrypt(cipher, key, flag="base64", is_bin=False):
    try:
        if flag == "base64":
            cipher = b64decode(cipher)
            byte_list = xxt_decrypt(cipher, key)
            if is_bin:
                return bytes(bytearray(byte_list))
            else:
                return bytes(bytearray(byte_list[:-1]))  # 去掉末位的 \0
    except Exception:
        return None
