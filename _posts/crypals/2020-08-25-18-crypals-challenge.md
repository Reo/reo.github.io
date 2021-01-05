---
layout: post
title: Cryptopals Challenge 18
category: crypto
author: 'reo'
tags: python cryptopals
mathjax: 
---

We implement AES CTR mode as specified in cryptopals challenge 18.

An intuitive idea for how CTR mode works can be gotten from
this diagram

|![CTRdiagram]{:class="svg invert-color" width="1200px"}|
|:--:|
| *CTR mode encryption (courtesy of Wikipedia)* |

We also notice from the example given on the challenge page that
the counter is in little endian. Notice that we are essentially generating
a stream we use to xor against our plaintext so we have no obligation
to stick with block boundaries and have no need for padding.

An implementation may then look something like

```python
import base64
from ecb import ecb_enc, ecb_dec
from pkcs7 import AES_BLOCKSIZE
from Crypto.Util.strxor import strxor

NONCE=b'\x00'*8

def ctr_enc(pt, key, nonce):
    ct = b''
    # only go for as many blocks as needed
    for blckIdx in range((len(pt)//16) + 1):
        curr = nonce + blckIdx.to_bytes(8,'little')
        enc = ecb_enc(curr, key)
        ptblck = pt[blckIdx*AES_BLOCKSIZE:(blckIdx+1)*AES_BLOCKSIZE]
        ctblck = strxor(ptblck, enc[:len(ptblck)])
        ct += ctblck
    return ct

def ctr_dec(ct, key, nonce):
    pt = b''
    # only go for as many blocks as needed
    for blckIdx in range((len(ct)//16) + 1):
        curr = nonce + blckIdx.to_bytes(8,'little')
        enc = ecb_enc(curr, key)
        ctblck = ct[blckIdx*AES_BLOCKSIZE:(blckIdx+1)*AES_BLOCKSIZE]
        ptblck = strxor(ctblck, enc[:len(ctblck)])
        pt += ptblck
    return pt
```

Here, we set NONCE to 0 for it to work with the example in the challenge but
in practice, the nonce is a random integer which should be difficult to guess.

We test this with the example given and a second test case.

```python
ct = base64.b64decode('L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==')
print(ctr_dec(ct, b'YELLOW SUBMARINE', NONCE))

import os
NONCE = os.urandom(8)
ciphertext = ctr_enc(b'this is some cool ciphertext with" quotes, /fslash, and uneven length', b'YELLOW SUBMARINE', NONCE)
print(ctr_dec(ciphertext, b'YELLOW SUBMARINE', NONCE))
```

which prints

```
b"Yo, VIP Let's kick it Ice, Ice, baby Ice, Ice, baby "
b'this is some cool ciphertext with" quotes, /fslash, and uneven length'
```

as expected.

[CTRdiagram]: https://upload.wikimedia.org/wikipedia/commons/4/4d/CTR_encryption_2.svg
