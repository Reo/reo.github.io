---
layout: post
title: Cryptopals Challenge 27
category: crypto
author: 'reo'
tags: python cryptopals
mathjax: true
---

[Cryptopals challenge](https://cryptopals.com/) 27. We recover the key used in a system
where the key and IV are the same value and used for AES CBC mode.

## Contents
{:.no_toc}

* Content
{:toc}

<br>

***

## System Setup

***

The system here is one where a pair of systems agree that they will communicate using AES CBC mode
with IV being the same as their key. If an error ocurrs due to one of tha characters not being ascii,
they raise an exception which includes the attempt at deciphering to plaintext. For this attack,
we need the plaintext to be at least 3 blocks (48 bytes) in length.

```python
import os
from cbc import cbc_enc, cbc_dec
from Crypto.Util.strxor import strxor

GKEY=os.urandom(16)
CBC_IV=GKEY

def dec_and_check(ct, key, iv):
    pt = cbc_dec(ct, GKEY, CBC_IV)
    # also takes care of depadding
    if not pt.isascii():
        return pt

s = b'value1=12345678&value2=2&value3=YELLOWxSUBMARINE'

# simulate the attacker intercepting the sent the message
ct = cbc_enc(s, GKEY, CBC_IV)
```

<br>

***

## Attacker's Approach

***

From here, the attacker manipulates the ciphertext in a way that the
plaintext it decrypts to leaks information, sends it to one of the
systems and saves the response.

```python
attack = ct[:16] + b'\x00'*16 + ct[:16]
response = dec_and_check(attack, GKEY, CBC_IV)
```

|![CBC diagram](https://upload.wikimedia.org/wikipedia/commons/2/2a/CBC_decryption.svg){:class="svg invert-color" width="1200px"}|
|:--:|
| *CTR mode decryption (courtesy of Wikipedia)* |

Label the original three ciphertext blocks $$C_1, C_2, C_3$$ respectively.
From the diagram we see the plaintext error response we are sent back is

$$D_{\text{GKEY}}(C_1)\oplus \text{CBC_IV} || C_1\oplus D_{\text{GKEY}}(0)||D_{\text{GKEY}}(C_1)$$

In particular, we know
$$D_{\text{GKEY}}(C_1)$$ and $$D_{\text{GKEY}}(C_1)\oplus \text{CBC_IV}$$.

Taking xor of both of these we get back `CBC_IV` which is what we want.

```python
leakedIV = strxor(response[:16], response[32:])
```

we can check this worked as follows:

```python
if __name__ == "__main__":
    assert CBC_IV == leakedIV
```

