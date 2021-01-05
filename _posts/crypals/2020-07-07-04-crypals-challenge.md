---
layout: post
title: Cryptopals Challenge 4
category: crypto
author: 'reo'
tags: python cryptopals
mathjax:
---

In challenge 4 of the [cryptopals challenges](https://cryptopals.com/)
we detect and break single-byte XOR which has been used to encrypt a
string. We do not know which.

We can use
the same strategy we used for [Challenge 3](/crypto/2020/06/30/crypals-challenges.html#challenge-3).
There are no more than $$60\times 255$$ checks in a brute force which is still very feasible.

```python
from Crypto.Util.strxor import strxor

# read in the dictionary file
words = set(line.strip() for line in open('/usr/share/dict/words'))
ciphertexts = [line.strip() for line in open('4.txt','r')]

for ciphertext in ciphertexts:
    c = bytes.fromhex(ciphertext)
    for i in range (256):
        res = strxor(bytes([i])*len(c), c)
        if res.isascii():
            candidates = res.decode().split()
            for candidate in candidates:
                if (len(candidate) > 1) and (candidate.lower() in words):
                    print(res)
                    print(i)
                    break
```

The only difference in this challenge is iterating through the candidates.

