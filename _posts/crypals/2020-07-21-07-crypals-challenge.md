---
layout: post
title: Cryptopals Challenge 7
category: crypto
author: 'reo'
tags: python cryptopals
mathjax: 
---

Continuing the cryptopals challenges, challenge 7 has us get familiar with using AES ECB mode. We implement our solution in
python as we have been for previous solutions. This may be a useful component so we call this `ecb.py` to make
importing easier for future challenges.

The code is simple and makes use of python's built-in libraries

```python
from Crypto.Cipher import AES

def ecb_enc(p,k):
    cipher = AES.new(k, AES.MODE_ECB)
    c = cipher.encrypt(p)
    return c

def ecb_dec(c,k):
    cipher = AES.new(k, AES.MODE_ECB)
    p = cipher.decrypt(c)
    return p
```

we can decipher the given file then by doing

```python
CipherFile = open('7.txt','r')
ct = base64.b64decode(CipherFile.read().replace('\n',''))
CipherFile.close()
print(ecb_dec(ct, b'YELLOW SUBMARINE'))
```
