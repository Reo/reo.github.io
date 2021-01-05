---
layout: post
title: Cryptopals Challenge 8
category: crypto
author: 'reo'
tags: python cryptopals
mathjax: 
---

The goal of this challenge is to detect which of a list of ciphertexts used AES ECB mode.

An easy way to do this is simply counting the number of blocks which are the same.
This works because there is no randomness involved in AES ECB mode in the sense that
the same 16 bytes of plaintext always encrypts to the same 16 bytes of ciphertext.

```python
from Crypto.Util.strxor import strxor
from operator import itemgetter

ECB_CHUNK_SIZE=16

def count_repeats(b, n, keylen):
    total = 0
    # count how many times a chunk of keylen bytes repeats
    for i in range(n-1):
        for j in range(i+1, n):
            if (b[i*keylen:(i+1)*keylen] == b[j*keylen:(j+1)*keylen]):
                total += 1

    return total
```

This next bit is to sort the ciphertexts with the one which has most repeats at the top
which are also the ones most likely to be encrypted in AES ECB.

```python
CipherFile = open('8.txt', 'r')
ciphertexts = CipherFile.read().splitlines()
CipherFile.close()

ct_guesses = list()

for i, ciphertext in enumerate(ciphertexts):
    c = bytes.fromhex(ciphertext)
    hamdepth = int(len(c)/ECB_CHUNK_SIZE)
    repeatCount = count_repeats(c, hamdepth, ECB_CHUNK_SIZE)
    ct_guesses.append((i, repeatCount))

ct_candidates = sorted(ct_guesses,key=itemgetter(1), reverse=True)

for i in range(12):
    print(str(i) + ': ' + str(ct_candidates[i]))
```

The output for the file given is

```
0: (132, 6)
1: (0, 0)
2: (1, 0)
3: (2, 0)
4: (3, 0)
5: (4, 0)
6: (5, 0)
7: (6, 0)
8: (7, 0)
9: (8, 0)
10: (9, 0)
11: (10, 0)
```

so the 132nd line is the one with most repeats with 6 repeats and is hence most likely the one
encrypted using AES ECB. No other line has any repeats.
