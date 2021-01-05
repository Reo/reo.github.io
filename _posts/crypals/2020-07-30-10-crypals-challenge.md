---
layout: post
title: Cryptopals Challenge 10
category: crypto
author: 'reo'
tags: python cryptopals
mathjax: 
---

The next [cryptopals challenge](https://cryptopals.com/), the tenth of the series is to implement AES CBC mode.
It is convenient to use the code we wrote for AES ECB mode for the [previous challenge](/crypto/2020/07/28/09-crypals-challenge.html).

AES CBC mode is also a block cipher like ECB mode. The difference lies in the fact that while CBC mode is
completely deterministic for each 16-byte block, CBC mode chains together information from previous blocks
so that two blocks with the same information in the plaintext do not result in two identical blocks in the
ciphertext.

|![cbc-graphic](https://upload.wikimedia.org/wikipedia/commons/8/80/CBC_encryption.svg){:class="svg invert-color" width="1200px"}|
|:--:|
| *CBC mode encryption (courtesy of Wikipedia)* |

We use the standard 16 byte blocksize.

```python
from ecb import ecb_enc, ecb_dec
from pkcs7 import pad, AES_BLOCKSIZE
from Crypto.Util.strxor import strxor

def cbc_enc(p,k,iv,blocksize=AES_BLOCKSIZE):
    '''
    encrypt p using AES CBC mode under key k with IV iv
    blocksize can be set here but is 16 bytes by default
    '''
    # Since AES is a block cipher, we need to get the plaintext
    # to line up with the block size
    pt = pad(p, blocksize)
    curr = iv
    ct = b''
    # The ith block an encryption of the previous block xored with
    # the current plaintext block
    for i in range(int(len(pt)/blocksize)):
        curr = ecb_enc(strxor(curr, pt[i*blocksize:(i+1)*blocksize]), k)
        ct += curr
    return ct

def cbc_dec(c,k,iv,blocksize=AES_BLOCKSIZE):
    '''
    decrypt c using AES CBC mode under key k with IV iv
    blocksize can be set here but is 16 bytes by default
    '''
    pt = b''
    curr = iv
    # reverse operation of that done in encryption
    for i in range(int(len(c)/blocksize)):
        tmp = c[i*blocksize:(i+1)*blocksize]
        pt += strxor(curr, ecb_dec(tmp, k))
        curr = tmp
    return pt
```

We can now test that this works using the example given:

```python
import base64

CipherFile = open('10.txt','r')
ct = base64.b64decode(CipherFile.read().replace('\n',''))
CipherFile.close()

print(cbc_dec(ct, b'YELLOW SUBMARINE', bytes([0])*16))
```

we get back the decrypted text along with padding added to line it up to
our block size.
