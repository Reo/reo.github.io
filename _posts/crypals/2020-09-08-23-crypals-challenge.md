---
layout: post
title: Cryptopals Challenge 23
category: crypto
author: 'reo'
tags: python cryptopals
mathjax: 
---

The third challenge in the series of [cryptopals challenges](https://cryptopals.com/)
which asks us to use the MT19937 PRNG is one where we clone the state given only values
it output. This is more powerful than the [previous](/crypto/2020/09/03/22-crypals-challenge.html)
attack since it does not rely on
the PRNG being seeded in a predictable manner.

## Contents
{:.no_toc}

* Content
{:toc}

<br>

***

## Outline

***

In this example, we seed the PRNG with a recommended value from its [Wikipedia entry](https://en.wikipedia.org/wiki/Mersenne_Twister).

```python
import os
import random
import mt19937

mt19937.seed_mt(5489)
```

In order to clone the state, we want to obtain of of the values stored in its state array
which for our implementation is called `MT`. Once all the values of MT are found, we copy
them into a local implementation of the PRNG. Of special note is the constant `n=642`
the size of this array , this will be useful when cloning the array.

Examining the `extract_number()` method from our implementation:

```python
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

we notice that some operations (called tempering) are done to
the value pulled from `MT`, we will reverse the tempering to get back our values
from the array. In order to recover the entire array, we will need all `n` values
so we repeat this process `n` times.

<br>

***

## Untempering

***

Written in python, the *untempering* process looks like

```python
# save n=624 calls to the rng
# for each of these, untemper to get back
# the original state of the MT array
detempered = []
realOuts = []
for i in range(n):
    extracted = mt19937.extract_number()
    realOuts.append(extracted)
    detempered.append(untemper(extracted))
```

Using constants from the MT19937 algorithm, we can reverse the tempering process.

```python
def untemper(y):
    x = y ^ (y>>l)

    x = x ^ ((x << t) & c)

    z = ((x << s) & (0x3F80&b)) ^ x
    z = ((z << s) & (0x1FC000&b)) ^ z
    z = ((z << s) & (0xFE00000&b)) ^ z
    x = ((z << s) & (0xF0000000&b)) ^ z

    z = ((x >> u) & (0x1FFC00&d)) ^ x
    x = ((z >> u) & (0x3FF&d)) ^ z

    return x
```

To verify we successfully cloned, we generate more numbers to compare after
the array is updated.

```python
# produce more numbers to verify cloning
for i in range(2*n):
    extracted = mt19937.extract_number()
    realOuts.append(extracted)
```

Next, we simply clone the state to our own copy of `MT` which we have access to

```python
# we now clone the state
for i in range(n):
    MT[i] = detempered[i]
```

<br>

***

## Verify The Cloning

***

Finally, we compare the saved generated numbers with the ones produced with our
own cloned PRNG

```python
INDEX = 0

# verify output is identical
for i in range(3*n):
    real = realOuts[i]
    expected = extract_number()
    if (expected != real):
        print('wrong prediction! at ' + str(i))
        exit(1)
```

The full code then includes both the included PRNG which we assume we don't have access
to its internals and a local implementation of MT19937 which we can manipulate the
state array:

```python
import os
import random
import mt19937

mt19937.seed_mt(5489)

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


def untemper(y):
    x = y ^ (y>>l)

    x = x ^ ((x << t) & c)

    z = ((x << s) & (0x3F80&b)) ^ x
    z = ((z << s) & (0x1FC000&b)) ^ z
    z = ((z << s) & (0xFE00000&b)) ^ z
    x = ((z << s) & (0xF0000000&b)) ^ z

    z = ((x >> u) & (0x1FFC00&d)) ^ x
    x = ((z >> u) & (0x3FF&d)) ^ z

    return x

# save n=624 calls to the rng
# for each of these, untemper to get back
# the original state of the MT array
detempered = []
realOuts = []
for i in range(n):
    extracted = mt19937.extract_number()
    realOuts.append(extracted)
    detempered.append(untemper(extracted))

# produce more numbers to verify cloning
for i in range(2*n):
    extracted = mt19937.extract_number()
    realOuts.append(extracted)

# we now clone the state
for i in range(n):
    MT[i] = detempered[i]

INDEX = 0

# verify output is identical
for i in range(3*n):
    real = realOuts[i]
    expected = extract_number()
    if (expected != real):
        print('wrong prediction! at ' + str(i))
        exit(1)
```
