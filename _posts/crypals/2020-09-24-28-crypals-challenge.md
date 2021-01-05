---
layout: post
title: Cryptopals Challenges 28-29
category: crypto
author: 'reo'
tags: python cryptopals
mathjax: 
---

We combine challenges 28 and 29 in this post which deals executing a hash-length extension attack
on SHA-1. It is one example of various ways to do hash-length extension which is featured as a
challenge on
the [cryptopals website](https://cryptopals.com/)

## Contents
{:.no_toc}

* Content
{:toc}

<br>

***

## System Setup

***

Challenge 28 first asks us to write a function to authenticate a message under a secret key
by using a simple prefix MAC. What we want looks like `SHA1(key || message)` and can be implemented
as:

```python
import os
import sha1
import random
import struct

GKEY=os.urandom(random.randint(110,220))

def make_hmac(message):
    return sha1.sha1(GKEY + message)

def verify_hmac(message, hmac):
    return make_hmac(message) == hmac
```

the sha1 implementation we use here can be found at [this repository](https://github.com/ajalt/python-sha1/blob/master/sha1.py).

The system here is one which takes a query string and a corresponding hmac to verify whether
the hmac was made using the secret key and hence the query string is valid.

<br>

***

## Attack Overview

***

As mentioned earlier, we will
be executing a [hash-length extension](https://en.wikipedia.org/wiki/Length_extension_attack)
so we will need to forge a message which looks like

```
SHA1(key || original-message || glue-padding || new-message)
```

where `glue-padding` is how the hash function computes padding to line up messages with block size and
`new-message` is `;admin=true` in our case.

<br>

***

## Attack Implementation

***

We set up our original message, corresponding valid hmac

```python
m = b"comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"
prefix_bytes = make_hmac(m)
```

now, similar to the Mersenne Twister we implemented in a previous post,
sha1 has state variable to keep track of its current state and implements the
[Merkle–Damgård construction](https://en.wikipedia.org/wiki/Merkle%E2%80%93Damg%C3%A5rd_construction).
We can take advantage of this to set our own implementation of sha1 to the same state

```python
start_state = (int(prefix_bytes[:8],16), int(prefix_bytes[8:16],16), int(prefix_bytes[16:24],16), int(prefix_bytes[24:32],16), int(prefix_bytes[32:],16))
hash_inst = sha1.Sha1Hash()
```

Note that since we will be extending an already-created hash we also need to compute the
padding which would have been created for the hmac for the original message `m`. We
can simply take this from the actual implementation of sha1 we are using

```python
def sha1_pad(mlength):
    '''
    mlength is the length of the message in bytes
    note SHA1 uses 64 byte blocks
    '''
    ret = b'\x80'
    ret += b'\x00' * ((56 - (mlength + 1) % 64) % 64)
    m_bitlength = mlength * 8
    ret += struct.pack(b'>Q', m_bitlength)
    return ret
```

Finally, we guess key lengths, say from 0 to 999 resetting the state at each time
and creating the appropriate padding until the server accepts the forged message.

```python
# guess key lengths between 1 and 999
for i in range(1000):
    # rebuild state
    totallen = len(m) + i
    curr_state = start_state
    hash_inst._h = start_state
    hash_inst._unprocessed = b";admin=true"
    hash_inst._message_byte_length = ((-totallen)%64) + totallen # length of the forged message up to appended block

    new_message = m + sha1_pad(totallen) + b';admin=true'
    new_hmac = hash_inst.hexdigest()
    if (verify_hmac(new_message, new_hmac)):
        print('success!')
        exit(0)
```

and as expected this prints `success!`.

