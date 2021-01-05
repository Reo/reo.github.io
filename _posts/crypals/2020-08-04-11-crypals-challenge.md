---
layout: post
title: Cryptopals Challenge 11
category: crypto
author: 'reo'
tags: python cryptopals
mathjax: 
---

In the 11th [cryptopals challenge](https://cryptopals.com/), our goal
is to use an oracle which encrypts using AES ECB half the time and
AES CBC the other half in order to tell which mode is being used reliably.

## Contents
{:.no_toc}

* Content
{:toc}

<br>

***

## Intro

***

Similar to the [previous challenge](/crypto/2020/07/23/08-crypals-challenge.html), we will be
taking advantage of the fact that AES ECB
always encrypts to identical plaintext blocks to identical ciphertext blocks.

First, we write the oracle which randomly encrypts either ECB or
CBC:

```python
from ecb import ecb_enc, ecb_dec
from cbc import cbc_enc, cbc_dec
from pkcs7 import pad, AES_BLOCKSIZE
from Crypto.Util.strxor import strxor
import random
import os

def ecb_cbc_oracle(pt):
    '''
    returns a bytestring of pt encrypted under
    AES ECB half the time and CBC the other half
    using a different key and, if necessary, iv
    each time.
    Additionally, between 5 and 10 random bytes are
    prepended and appended to the plaintext at each
    call.
    '''
    prefixlen = random.randint(5, 10)
    prefix = os.urandom(prefixlen)
    suffixlen = random.randint(5, 10)
    suffix = os.urandom(suffixlen)
    pt = prefix + pt + suffix

    key = os.urandom(16)
    mode = random.randint(1,2)
    if mode == 1:
        pt = pad(pt)
        ct = ecb_enc(pt, key)
    else:
        iv = os.urandom(16)
        ct = cbc_enc(pt, key, iv, 16)
    return ct
```

<br>

***

## Chosen plaintext

***

To find out which was used, we simply pass in a chosen plaintext which
takes up various blocks so regardless of any prefix or suffix we are guaranteed
to have at least two blocks of plaintext which are identical.

```python
if __name__ == "__main__":
    payload = b'a'*64
    for i in range(20):
        ct = ecb_cbc_oracle(payload)
        if (ct[16:32] == ct[32:48]):
            print('ecb')
        else:
            print('cbc')
```

Though 64 is overkill for this example it works for our blocksize of 16 bytes since
we would need at least 32 for two blocks of identical input plus at least 22 more to
fill the blocks with the added prefix and suffix.

recall that CBC uses the prvious ciphertext so two consecutive blocks of `a`
would encrypt to different ciphertext blocks while in ECB mode two consecutive blocks
of `a` would encrypt to the same two blocks of ciphertext. That is what we're checking
for when determining what mode was used here.
