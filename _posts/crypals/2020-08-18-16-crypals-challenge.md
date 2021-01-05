---
layout: post
title: Cryptopals Challenge 16
category: crypto
author: 'reo'
tags: python cryptopals
mathjax: 
---

The final challenge for set 2 of the [cryptopals challenges](https://cryptopals.com/).
We completed challenge 15 [in a previous post](/crypto/2020/08/13/14-crypals-challenge.html) so we continue with 16
which asks us to implement a CBC bit flipping attack.

## Contents
{:.no_toc}

* Content
{:toc}

<br>

***

## System Set Up and Implementation

***

The system here is one which allows the user to choose some data to send to the server.
It then prepends the data with the string `"comment1=cooking%20MCs;userdata="`
and appends the string `";comment2=%20like%20a%20pound%20of%20bacon"`.

Similar to the cut and paste attack
we did earlier, when parsing it checks for and rejects any `userdata` which
contains meta characters `;` or `=`.
It then encrypts the result using AES CBC under a random key and iv.
In python it could look something like this:

```python
import os
from Crypto.Util.strxor import strxor
from cbc import cbc_enc, cbc_dec
from pkcs7 import pad, AES_BLOCKSIZE

GKEY=os.urandom(16)
iv=os.urandom(16)

def oracle(userdata):
    if ((b';' in userdata) or (b'=' in userdata)):
        return ''
    prefix = b"comment1=cooking%20MCs;userdata="
    suffix = b";comment2=%20like%20a%20pound%20of%20bacon"
    s = prefix + userdata + suffix
    return cbc_enc(s, GKEY, iv)
```

The server then verifies whether a user is admin by taking back in the ciphertext
and checking if `admin=true` is present between the `;`-separated string:

```python
def decrypt_and_check_for_admin(ct):
    arr = cbc_dec(ct, GKEY, iv).split(b';')
    if (b'admin=true' in arr):
        return True
    return False
```

<br>

***

## Strategic Bit Flips

***

In order to break this, we rely on the fact that due to the description of CBC mode,
a 1-bit change in the ciphertext propagates and affects the upcoming blocks.
In particular, the ciphertext from the previous block is xored against the upcoming block.

|![cbc-flip-diagram](https://i.stack.imgur.com/bOu8Q.png){:class="invert-color" width="1200px"}|
|:--:|
| *Modifying the cyan bit allows us to xor the corresponding plaintext (courtesy of Wikipedia)* |

The string `xxxxxxxxxxxxxxxxxxxxx9admin9true` has none of the meta charaters and will
therefore be accepted. Our plaintext would be divided into the following blocks:

```
||  comment1=cooking  ||
||  %20MCs;userdata=  ||
||  xxxxxxxxxxxxxxxx  ||
||  xxxxx9admin9true  ||
||  ;comment2=%20lik  ||
||  e%20a%20pound%20  ||
||  of%20bacon[pad-]  ||
```

notice that the xor of the numerical representation of `9` in ascii and `0x02` gives us `0x3b`
which is the numerical representation of `;` character in ascii. Similarly, xor of `0x39`
(numerical representation of `9` in ascii) with `0x04` gives `0x3d` which decodes to `=`.
We can try to use the bit propagation property mentioned earlier to alter the ciphertext
without knowing the key and have it decrypt to our target of `;admin=true`.

<br>

***

## Implementing the Attack

***

First, we get the corresponding ciphertext

```python
userdata = b'x'*21 + b'9admin9true'
ct = oracle(userdata)
```

Next, we construct and apply the mask using the values discussed earlier:

```python
mask = b'\x00'*32 + b'\x00'*5 + b'\x02' + b'\x00'*5 + b'\x04' + b'\x00'*52 + b'\x00'*16
attack = strxor(ct, mask)
```

and finally, we confirm this gives us our expected result

```python
print(decrypt_and_check_for_admin(attack))
# > True
```

which means we have gotten admin priveleges as desired.
