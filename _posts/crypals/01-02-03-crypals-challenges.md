---
layout: post
date: 30-06-2020
title: Cryptopals Challenges 1-3
category: crypto
author: 'reo'
tags: python cryptopals
---

Solving challenges 1, 2, and 3 of [the cryptopals challenges](https://cryptopals.com/) using Python.

## Contents
{:.no_toc}

* Content
{:toc}

<br>

***

## Challenge 1

***

The first challenge is simply converting hex to base64. Python has a library to do just this
making the first challenge quite easy: we have `hex2base64.py`

```python
import base64

def hex_to_base64(hex):
    '''
    takes in a string with hex digits and
    returns it as a base64 encoded string
    '''
    return base64.b64encode(bytes.fromhex(hexstr))
```

<br>

***

## Challenge 2

***

The next challenge wants us to take two equal length hex buffers and return their XOR. We again take
advantage of a useful library so `xorstr.py` is

```python
import base64
from Crypto.Util.strxor import strxor

def xor_hexstr(hexstr1, hexstr2):
    '''
    takes in two hex strings and returns their xor
    '''
    bytes1 = bytes.fromhex(hexstr1)
    bytes2 = bytes.fromhex(hexstr2)
    return strxor(bytes1, bytes2).hex()
```

<br>

***

## Challenge 3

***

Finally, challenge 3 asks us break a cipher which uses the XOR technique we implemented in the last challenge.
Since we are dealing directly with bytes, there is no need to import the previous file.

The detail here is that since we are xoring against only a single byte, there are only 256 possible
keys from `0x00` to `0xff`. The crack is a simple brute force which checks all possible keys and prints
the key and words where the first position when split appears as a word in the dictionary.

```python
from Crypto.Util.strxor import strxor

# linux dictionary is used to check for valid words
words = set(line.strip() for line in open('/usr/share/dict/words'))

c = bytes.fromhex('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')

# for each possible key
for i in range (256):
    # res is the attempted decipher
    res = strxor(bytes([i])*len(c), c)
    if res.isascii():
        candidates = res.decode().split()
        # we check that there is at least one nontrivial word as a result
        for candidate in candidates:
            if (len(candidate) > 1) and (candidate.lower() in words):
                print(res)
                print(i)
                break
```

sure enough this works and we find the the ciphertext was originally

`Cooking MC's like a pound of bacon`

with corresponding key: `88`.
