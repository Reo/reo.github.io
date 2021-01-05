---
layout: post
title: Cryptopals Challenge 22
category: crypto
author: 'reo'
tags: python cryptopals
mathjax: 
---

The 22nd [cryptopals challenge](https://cryptopals.com/)
asks us to crack an MT19937 seed given the output it gives.
This is an example of why the distinction exists between cryptographically
secure RNG and more general-purpose RNG such as this one which
may be more efficient but is prone to this sort of attack.

we use `mt19937.py` we implemented [last time](/crypto/2020/09/01/21-crypals-challenge.html)
along with other common libraries

```python
import random
import time
import mt19937
```

The challenge here is essentially asking us to seed the RNG with a random timestamp
between 80 and 2000 seconds ago with respect to the time the crack is run.

There is no need for any clever trick, the number of possible seeds is so small
that a brute force would suffice. The idea is to try all possible times which
could have been used as a seed until the output matches the expected value,
this is implemented in the following code:

```python
# wait random number of seconds between 40 and 1000,
# seed RNG with current timestamp, wait random number of seconds again,
# save the generated number
a = random.randint(40,1000)
b = random.randint(40,1000)
time.sleep(a)
realSeed = int(time.time())
seed_mt(realSeed)
time.sleep(b)
out = extract_number()

# now guess all times from 38 to 1002 seconds
currTime = int(time.time())
guesses = set()
for i in range(38, 1010):
    seed_mt(currTime - i)
    if (extract_number() == out):
        guesses.add(i)
print(guesses)
```

sure enough this finds the original seed as desired.
