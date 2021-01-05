---
layout: post
title: Cryptopals Challenge 24
category: crypto
author: 'reo'
tags: python cryptopals
mathjax: true
---

This [cryptopals challenge](https://cryptopals.com/)
asks us break a cipher which uses MT19937 as a keystream with a known plaintext.
The keysize here 2 bytes so there are only $$2^{16}=65536$$ possible keys, this is small enough
to be feasibly brute forced. We will use known plaintext here to confirm which of the guessed
keys is the correct one.

## Contents
{:.no_toc}

* Content
{:toc}

<br>

***

## Implementing the Cipher

***

```python
def mt_encrypt(pt, k):
    ct = b''
    seed_mt(int.from_bytes(k, 'little'))
    for i in range(len(pt)):
        curr = bytes([extract_number()&0xFF])
        ct += strxor(pt[i:i+1], curr[0:1])
    return ct

def mt_decrypt(ct, k):
    pt = b''
    seed_mt(int.from_bytes(k, 'little'))
    for i in range(len(ct)):
        curr = bytes([extract_number()&0xFF])
        pt += strxor(ct[i:i+1], curr[0:1])
    return pt
```

create a random plaintext with a known suffix and run it under the cipher

```python
prefixLen = random.randint(5,50)
prefix = os.urandom(prefixLen)
pt = prefix + b'A'*14
# next, run it under the created cipher
ct = mt_encrypt(pt, GKEY)
```

<br>

***

## Breaking the Cipher

***

And finally, we guess all possible keys looking for our stimulus of 14 consecutive `'A'` characters
at the end.

```python
guesses = set()
for i in range(2**16):
    candidate = mt_decrypt(ct, bytes([(i>>8), i&0xFF]))
    if ((candidate[-14:]) == (b'A'*14)):
        guesses.add(bytes([(i>>8), i&0xFF]))
```

We can verify this succeeded by checking the key against the
set of guesses

```python
# use this to verify we guessed correctly
if __name__ == "__main__":
    print(guesses)
    assert(GKEY in guesses)
```

and sure enough we have the size of guesses should be very small, often containing just the one element
guaranteed to be present which is GKEY as desired.
