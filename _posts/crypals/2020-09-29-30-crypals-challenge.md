---
layout: post
title: Cryptopals Challenge 30
category: crypto
author: 'reo'
tags: python cryptopals
mathjax: 
---

This challenge is again similar to the last one. This hash length extension is on md4.
The md4 implementation can be found [at this repo](https://gist.github.com/BenWiederhake/eb6dfc2c31d3dc8c34508f4fd091cea9).

There are no major changes and details on what's going on can be found in the [previous post](/crypto/2020/09/24/28-crypals-challenge.html).
The biggest difference is perhaps the `md4_pad()` method which is taken from the implementation itself.

```python
import random
import os
import md4
import struct

GKEY=os.urandom(random.randint(110,220))

def md4_pad(mlength):
    # suppose we're dealing with bytes
    # in particular, mlength is the length of the message in bytes
    # note SHA1 uses 64 byte blocks
    ret = b'\x80' + b'\x00' * ((55 - mlength) % 64) + struct.pack("<Q", mlength * 8)
    return ret

def make_hmac(message):
    mmd = md4.MD4()
    mmd.add(GKEY + message)
    return mmd.finish()

def verify_hmac(message, hmac):
    return make_hmac(message) == hmac

def to_int(b):
    return int.from_bytes(b,'little')

m = b"comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"
mlen = len(m)
prefix_bytes = make_hmac(m)

start_state = [to_int(prefix_bytes[:4]), to_int(prefix_bytes[4:8]), to_int(prefix_bytes[8:12]), to_int(prefix_bytes[12:])]
md = md4.MD4()

for i in range(999):
    totallen = mlen + i
    md.h = start_state.copy()
    md.remainder = b";admin=true"
    md.count = (totallen//64) + 1

    new_message = m + md4_pad(totallen) + b';admin=true'
    new_hmac = md.finish()
    if (verify_hmac(new_message, new_hmac)):
        print('success!')
        exit(0)
```
