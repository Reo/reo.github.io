---
layout: post
title: Cryptopals Challenge 26
category: crypto
author: 'reo'
tags: python cryptopals
mathjax: 
---

We take on challenge 26 from the set provided on the [cryptopals website](https://cryptopals.com/).
This time we implement a bit flipping attack on AES CTR mode similar to the bitflipping attack
we did in an [earlier post](/crypto/2020/08/18/16-crypals-challenge.html) against AES CBC mode.

## Contents
{:.no_toc}

* Content
{:toc}

<br>

***

## System Setup

***

Just like the aforementioned bitflip attack, the goal is get the string
`;admin=true` to appear in our query string. We set up the system similarly

```python
import os
from ctr import ctr_enc, ctr_dec
from Crypto.Util.strxor import strxor

GKEY=os.urandom(16)
NONCE=os.urandom(8)

def oracle(userdata):
    # don't accept userdata with ; or = in the string
    if ((b';' in userdata) or (b'=' in userdata)):
        return ''
    prefix = b"comment1=cooking%20MCs;userdata="
    suffix = b";comment2=%20like%20a%20pound%20of%20bacon"
    s = prefix + userdata + suffix
    return ctr_enc(s, GKEY, NONCE)

def decrypt_and_check_for_admin(ct):
    arr = ctr_dec(ct, GKEY, NONCE).split(b';')
    if (b'admin=true' in arr):
        return True
    return False
```

<br>

***

## The Attack

***

This time it's a little different since instead of feeding into the next block, the
bitfliping takes place in the same block. Hence, we only need one block this time
around and get back our ciphertext from the server. We can also check that this
does not give us admin priveleges as expected:

```python
userdata = b'xxxxx9admin9true'
ct = oracle(userdata)
# test that system works as expected:
print(decrypt_and_check_for_admin(ct))
# > False
```

Great, now we use the same mask from the previous bit-flipping challenge to
alter the ciphertext in a way that decrypts to our target text.

```python
mask = b'\x00'*32 + b'\x00'*5 + b'\x02' + b'\x00'*5 + b'\x04' + b'\x00'*46
attack = strxor(ct, mask)
```

Finally, we can check this attack succeeded

```python
print(decrypt_and_check_for_admin(attack))
# > True
```
