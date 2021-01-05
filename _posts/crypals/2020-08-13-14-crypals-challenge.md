---
layout: post
title: Cryptopals Challenge 14
category: crypto
author: 'reo'
tags: python cryptopals
mathjax: 
---

Continuing our cryptopals challenges,
we now tackle another attack on AES ECB encryption similar
to the one from [challenge 12](/crypto/2020/08/06/12-crypals-challenge.html).
This time, a random prefix is present which complicates things
a little.

## Contents
{:.no_toc}

* Content
{:toc}

<br>

***

## Setting up the Oracle

***

The first thing which is different this time around is the fact we need to find out where
the random prefix ends in order to use the same strategy we did in challenge 12. The
oracle now looks like:

```python
def concat_ecb(pt):
    hidden = 'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg'
    hidden += 'aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq'
    hidden += 'dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK'
    hidden = base64.b64decode(hidden)
    text = pad(pt+hidden)
    return ecb_enc(text, GKEY)
```

<br>

***

## Discovering the Start of Our Chosen Plaintext

***

AES ECB mode encryption means we can take advantage of a vulnerability we've used
in previous challenges. We first find out what a block of all `'a'` looks like.
We can do this by sending 3 blocks worth of `'a'` to the oracle so the ciphertext
has at least two identical blocks which are the enciphered `'a'`-filled blocks.

```python
repIdx, repBlock = find_block_pairs(concat_ecb(b'A'*(blockLen*3)), blockLen)
# this means the random prefix ends exactly at, or before repIdx
```

This is implemented as

```python
def find_block_pairs(b, blocksize):
    numblocks = int(len(b) / blocksize)
    for i in range(numblocks - 1):
        blockA = b[i*blocksize:(i+1)*blocksize]
        for j in range(i+1, numblocks):
            blockB = b[j*blocksize:(j+1)*blocksize]
            if (blockA == blockB):
                return (i, blockA)
```

<br>

***

## Retrofitting to Previous Solution

***

With this information and the number of bytes we have appended, we can create a
"prebuffer" which is just a prefix to the buffer we used in our solution to
[challenge 12](/crypto/2020/08/06/12-crypals-challenge.html)..

```python
prebuff = b'A'*blockLen
while (concat_ecb(prebuff)[repIdx*blockLen:(repIdx+1)*blockLen] != repBlock):
    prebuff += b'A'
# we no longer need the extra block full of 'A' so just leave what is needed
# to make the prefix complete a block
prebuff = prebuff[blockLen:]

# compute the actual length of the plaintext
hiddenLen = hiddenLen - (blockLen * repIdx) + len(prebuff)
```

from here on, it's just a modified version of our previous solution

```python
# and find the plaintext one byte at a time
hiddenGuess = b''

for i in range(hiddenLen):
    currBlock = repIdx + int(i/blockLen)    # start the block after the random and prebuff
    bufflen = (blockLen - 1 - i) % blockLen # length of the buffer according to the algorithm
    buff = prebuff + b'x'*bufflen           # construct the whole buffer required
    hiddenGuess += find_byte_from_block(buff, currBlock, blockLen, hiddenGuess)
```

printing the output we get

```
b"Rollin' in my 5.0\nWith my rag-top down so my hair can blow\nThe girlies on standby waving just to say hi\nDid you stop? No, I just drove by\n"
```

which looks a whole lot like deciphered text.

The imports we needed here were:

```python
from ecb import ecb_enc, ecb_dec
from pkcs7 import pad, AES_BLOCKSIZE
import os
import base64
import random
```
