# -*- coding: utf-8 -*-
# Copyright: (c) 2022, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


from random import SystemRandom
import time

rand_instance = SystemRandom()


def get_timestamp():
    return str(int(time.time()))


def get_nonce(timestamp: str):
    return str(rand_instance.getrandbits(64)) + timestamp


def combine_item(key, value):
    return f'{key}="{value}"'


def get_oauth_header(consumer_key, token_key, token_signature):
    timestamp = get_timestamp()
    nonce = get_nonce(timestamp)

    params = [
        ("oauth_nonce", nonce),
        ("oauth_timestamp", timestamp),
        ("oauth_version", "1.0"),
        ("oauth_signature_method", "PLAINTEXT"),
        ("oauth_consumer_key", consumer_key),
        ("oauth_token", token_key),
        ("oauth_signature", f"%26{token_signature}"),
    ]

    partial = ", ".join(combine_item(k, v) for k, v in params)
    return f"OAuth {partial}"
