---
layout: post
title: Cryptopals Challenge 21
category: crypto
author: 'reo'
tags: python cryptopals
mathjax: 
---

The next cryptopals challenge asks us to implement MT19937 aka [Mersenne Twister](https://en.wikipedia.org/wiki/Mersenne_Twister),
the most widely-used PRNG for general purposes but --- as we will learn in the next few challenges,
is not cryptographically secure.

The implementation can be found on [Wikipedia](https://en.wikipedia.org/wiki/Mersenne_Twister).
We implement the 32 bit version using the pseudocode and constants from that same Wiki page.

```python
import os
import random

# This implements MT19937
# constants and pseudocode courtesy of Wikipedia

w, n, m, r = 32, 624, 397, 31
a = 0x9908B0DF
u, d = 11, 0xFFFFFFFF
s, b = 7, 0x9D2C5680
t, c = 15, 0xEFC60000
l = 18
f = 1812433253

LOW_W_MASK = (2**w)-1

MT = [None] * n
INDEX = n+1
LOWER_MASK = (1 << r) - 1 # the number of r 1's
UPPER_MASK = LOW_W_MASK & ~l

'''
initialize using a seed
'''
def seed_mt(seed):
    global INDEX
    INDEX = n
    MT[0] = LOW_W_MASK & seed
    for i in range (1,n):
        MT[i] = LOW_W_MASK & (f*(MT[i-1]^(MT[i-1]>>(w-2))))

def twist():
    global INDEX
    for i in range(n):
        x = (MT[i] & UPPER_MASK) + (MT[(i+1)%n] & LOWER_MASK)
        xA = x >> 1
        if ((x % 2) != 0):
            xA = xA ^ a
        MT[i] = MT[(i+m) % n] ^ xA
    INDEX = 0

# extract value based on MT[INDEX]
# calling twist() every n numbers
def extract_number():
    global INDEX
    if (INDEX >= n):
        if (INDEX > n):
            print('Generator never seeded')
            # may automatically seed with 5489 in this case
            exit(1)
        twist()

    y = MT[INDEX]
    y = y ^ ((y >> u)&d)
    y = y ^ ((y << s)&b)
    y = y ^ ((y << t)&c)
    y = y ^ (y >> l)

    INDEX += 1
    return LOW_W_MASK & y
```

For future use we call this file `mt19937.py`.
