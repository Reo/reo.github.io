---
layout: post
title: Cryptopals Challenge 12
category: crypto
author: 'reo'
tags: python cryptopals
mathjax: 
---

This next cryptopals challenge involves finding out information
on the cipher used (in this case, blocksize and AES mode).
Upon discovering ECB mode is being used, an attack is mounted where
decryption can be done without knowledge of the key one byte at a time.

## Contents
{:.no_toc}

* Content
{:toc}

<br>

***

## Discovering the Blocksize

***

The first step is to find out the block size of the cipher
being used. This can be done by simply trying different size
plaintext until the encryption needs to use a new block.
The blocksize is then the difference in size between the previous and
new ciphertext:

```python
# length of the ciphertext before any appends
ctLen = len(concat_ecb(b''))
hiddenLen = -1 # length of hidden text
blockLen = -1  # length of a block in this cipher
diff = 0       # difference in length beween two ciphertexts
i = 1          # keep track of how many bytes needed to append
while (diff == 0):
    diff = len(concat_ecb(b'a'*i)) - ctLen
    i += 1
blockLen = diff
hiddenLen = ctLen - i
```

<br>

***

## Discovering the Mode of Encryption

***

Now that we have the blocksize, we check if ECB mode is being used.
If this is not the case, this attack cannot be used so we exit.
To check, we use the same strategy [from last time](/crypto/2020/08/04/11-crypals-challenge.html).

```python
# check if the function is using ECB.
ct = concat_ecb(b'a'*(2*blockLen))
if (not(ct[:blockLen] == ct[blockLen:2*blockLen])):
    # Since the chosen plaintext is the prefix,
    # the condition holds iff using ECB mode
    exit(1)
```

<br>

***

## Byte-at-a-Time Cracking

***

Now that we know both the blocksize and that we're using ECB mode,
we can discover the hidden text one byte at a time as follows:

1. create a buffer which leaves only one byte of unknown hidden text at the end
2. find the ciphertext of that block and call it `blockA`
3. try ASCII values (or more generally `0x00` to `0xff`) as the last byte call it `blockB`
4. when `blockA == blockB` we have found the last byte
5. repeat this for every byte of the hidden text

we implement this with a nested loop which iterates over every byte of
the hidden text which we found the length of above and called `hiddenLen`.
The inner loop is the one which guesses every possible byte until a match is found;
it makes sense to make this a helper.

The main loop then looks like

```python
for i in range(hiddenLen):
    blockIdx = int(i/blocksize)
    bufflen = (blocksize - 1 - i) % blocksize
    buff = b'x'*bufflen
    hiddenGuess += find_byte_from_block(buff, blockIdx, blocksize, hiddenGuess)
```

while `find_byte_from_block()` is implemented as follows:

```python
def find_byte_from_block(buff, blockIdx, blocksize, reconstructed):
    l = blocksize*blockIdx     # lower index
    u = blocksize*(blockIdx+1) # upper index
    blockA = concat_ecb(buff)[l:u]
    # guess every possible byte
    for i in range(0, 256):
        blockB = concat_ecb(buff + reconstructed + bytes([i]))[l:u]
        if (blockA == blockB):
            return bytes([i])
```

<br>

***

## Conclusion

***

When the algorithm terminates, the hidden text is then stored in `hiddenGuess` and may be printed:

```python
print(hiddenGuess)
# > b"Rollin' in my 5.0\nWith my rag-top down so my hair can blow\nThe girlies on standby waving just to say hi\nDid you stop? No, I just drove by"
```

To complete the code, the imports we ended up needing were:
```python
from ecb import ecb_enc, ecb_dec
from pkcs7 import pad, AES_BLOCKSIZE
import os
import base64
```
