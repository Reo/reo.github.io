---
layout: post
title: Cryptopals Challenge 17
category: crypto
author: 'reo'
tags: python cryptopals
mathjax: true
---

For the 17th [Cryptopals challenge](https://cryptopals.com/),
we implement the so-called best-known attack on modern block cipher cryptography.
The CBC padding oracle.

## Contents
{:.no_toc}

* Content
{:toc}

<br>

***

## System Set Up and Implementation

***

The required imports end up being
```python
import random
import os
import base64
from cbc import cbc_enc, cbc_dec
from pkcs7 import pad, unpad, AES_BLOCKSIZE
```

The system in this example uses one random 16 byte AES key and encrypts one of 10 strings
chosen randomly using AES CBC mode. It then provides the ciphertext and iv. This
can be implemented as follows

```python
GKEY=os.urandom(16)
hiddenlist = [
        base64.b64decode('MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc='),
        base64.b64decode('MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic='),
        base64.b64decode('MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw=='),
        base64.b64decode('MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg=='),
        base64.b64decode('MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl'),
        base64.b64decode('MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA=='),
        base64.b64decode('MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw=='),
        base64.b64decode('MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8='),
        base64.b64decode('MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g='),
        base64.b64decode('MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93')
        ]

def encrypt_and_generate_iv():
    currhidden = hiddenlist[random.randint(0,9)]
    iv = os.urandom(16)
    ct = cbc_enc(currhidden, GKEY, iv)
    return ct, iv
```

The user is then supposed to send back the ciphertext and iv to an oracle which checks the padding
upon decryption and returns true iff the padding is valid.

```python
def check_pad(b):
    r = b[-1]
    return (b[-r:] == bytes([r])*r)

def pad_oracle(ct, iv):
    pt = cbc_dec(ct, GKEY, iv)
    return check_pad(pt)
```

This simulates AES CBC as it's implemented server-side in web applications.
The second can be thought of as mocking an encrypted session token such as
a cookie.

<br>

***

## Overview of Attack

***

We will be breaking this implementation using a side-channel attack, the oracle
leaks more information than it should by revealing whether or not the pad is valid.
The idea is as follows:

First, obtain the ciphertext, iv pair.
For each block, we corrupt its last byte until we have a valid padding. If it is
modified and is valid, it is likely the case that $$m\oplus b=01_{16}$$
where $$m$$ is the modification made to the last byte $$b$$ and subscript denotes
the base, in this case hex.
Now that we know the last byte we continue similarly for subsequent bytes.

```python
ct, iv = encrypt_and_generate_iv()
pt = b''
# for each block
for blckIdx in range(int(len(ct)/AES_BLOCKSIZE)):
    ptblck = b''
    ctblck = ct[AES_BLOCKSIZE*blckIdx:AES_BLOCKSIZE*(blckIdx+1)]
    prevctblck = iv if (blckIdx == 0) else ct[AES_BLOCKSIZE*(blckIdx-1):AES_BLOCKSIZE*blckIdx]
```

We initialize variables we will use to store the plaintext as well as the previous and
current block we will crack. Notice that the first "previous" block is the iv
since it serves the same purpose for the first block.

We will need another loop inside which goes over every byte within the block which
is where we will be corrupting the current ciphertext block.

For the $$i$$th byte into the block
we need to corrupt the ciphertext in a way which will allow us to use the oracle.
We can traverse the block in reverse and corrupt the $$i-1$$ bytes which follow
(in the previous block) so that when xored, they have a value of $$i$$ and
the oracle tells us if the $$i$$th byte is also correct.

This is an inductive argument and assumes we have found the $$i-1$$ previous
bytes. The initial byte can be found with an empty "fake" padding manipulating
only the final byte of the previous block until it is accepted in which
case we can say (with high probability) that we have found the desired byte.

<br>

***

## Byte-by-Byte Cracking

***

```python
    for byteIdx in range(1, AES_BLOCKSIZE+1):
        fauxpad = construct_fauxpad(byteIdx, ptblck, prevctblck)
```

where `construct_fauxpad()` may be implemented as:

```python
def construct_fauxpad(bIdx, ptblck, ctblck):
    '''
    create an artificial pad using known bytes
    '''
    fpad = b''
    for i in range(1, bIdx):
        fpad += bytes([ptblck[i-1] ^ ctblck[AES_BLOCKSIZE-bIdx+i] ^ bIdx])
    return fpad
```

from here we want to find $$m$$ from the previous section which we will call `delta`.

```python
        delta = find_delta(byteIdx, ctblck, fauxpad)
```

an example implementation being

```python
def find_delta(bIdx, ctblck, fauxpad):
    '''
    Find the character which results in the desired ciphertext
    accepted by the oracle
    '''
    for i in range(1, 256):
        if (pad_oracle(ctblck, b'\xff'*(AES_BLOCKSIZE-bIdx) + bytes([i]) + fauxpad)):
            return i
    return 0
```

Notice that we skip 0 initially since it would trivially satisfy the oracle
(no modification). We also use the value `b'\xff'` so there are no clashes
with pad values.

We use the $$m\oplus b$$ formula to recover an additional byte of paintext

```python
        delta ^= byteIdx
        ptblck = bytes([delta ^ prevctblck[AES_BLOCKSIZE-byteIdx]]) + ptblck
```

<br>

***

## Bringing it Together

***

putting everything together, our main loop looks like

```python
for blckIdx in range(int(len(ct)/AES_BLOCKSIZE)):
    ptblck = b''
    ctblck = ct[AES_BLOCKSIZE*blckIdx:AES_BLOCKSIZE*(blckIdx+1)]
    prevctblck = iv if (blckIdx == 0) else ct[AES_BLOCKSIZE*(blckIdx-1):AES_BLOCKSIZE*blckIdx]
    # for each byte within the block
    for byteIdx in range(1, AES_BLOCKSIZE+1):
        fauxpad = construct_fauxpad(byteIdx, ptblck, prevctblck)
        delta = find_delta(byteIdx, ctblck, fauxpad)
        delta ^= byteIdx
        ptblck = bytes([delta ^ prevctblck[AES_BLOCKSIZE-byteIdx]]) + ptblck
    pt += ptblck
```

We can verify this works with

```python
print(unpad(pt))
```

and we see the plaintext we expect.
