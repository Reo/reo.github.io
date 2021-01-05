---
layout: post
title: Cryptopals Challenge 25
category: crypto
author: 'reo'
tags: python cryptopals
mathjax: 
---

In this challenge, we common cited and supposed benefit of AES CTR mode being that one can
easily seek into the ciphertext and decrypt just the byte/block which is needed.

## Contents
{:.no_toc}

* Content
{:toc}

<br>

***

## Random Access Decipher

***

We simulate such a function by generating a random key which encrypts some ciphertext
and leaving the ability to edit through an API which can be accessed by anyone.
First, we have the edit function. Note that in the diagram, we can decipher any
block without needing to decipher any of the previous blocks

|![CTRdiagram]{:class="svg invert-color" width="1200px"}|
|:--:|
| *CTR mode decryption (courtesy of Wikipedia)* |


```python
import base64
import os
from pkcs7 import unpad, AES_BLOCKSIZE
from ecb import ecb_dec
from ctr import ctr_enc, ctr_dec
from Crypto.Util.strxor import strxor

GKEY = os.urandom(16)
CTR_NONCE = os.urandom(8)

def edit(ct, offset, newbyte):
    '''
    offset is given in bytes
    newbyte is the byte which will replace the one at offset
    '''
    if (offset >= len(ct)):
        # or offset is negative
        print('invalid offset')
        exit(1)

    blck = offset//AES_BLOCKSIZE
    pos = offset % AES_BLOCKSIZE
    pt = ctr_dec(ct, GKEY, CTR_NONCE)
    pt = pt[0:offset] + newbyte + pt[offset+1:]
    return ctr_enc(pt, GKEY, CTR_NONCE)
```

We then encrypt the file we are given under CTR

```python
CipherFile = open('25.txt','r')
ct = base64.b64decode(CipherFile.read().replace('\n',''))
CipherFile.close()
secret = unpad(ecb_dec(ct, b'YELLOW SUBMARINE'))

newCt = ctr_enc(secret, GKEY, CTR_NONCE)
```

<br>

***

## Recovering the Plaintext

***

Now, in order to break this system and recover the plaintext we will create a list
of guesses for what any given byte can be

```python
freqs = [
    b'e', b't', b'a', b'o', b'i', b'n', b's', b'h', b'r', b'd', b'l', b' ', b'c', b'u', b'm', b'w', b'f', b'g', b'y', b'p', b'b', b'\'', b'v', b'k', b'j', b'x', b'q', b'z',
    B'E', B'T', B'A', B'O', B'I', B'N', B'S', B'H', B'R', B'D', B'L', B'C', B'U', B'M', B'W', B'F', B'G', B'Y', B'P', B'B', B'V', B'K', B'J', B'X', B'Q', B'Z', b'\n', b'.',
    b'-', b',', b'"', b'9', b'8', b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'0', b'/', b'?', b'!', b'\n'
]
```

if we wanted to be more sophisticated we could use a better guessing strategy where
we base our guesses on the state of the string decrypted so far similar to how a human would
guess. This is related to the [Entropy of Printed English](http://languagelog.ldc.upenn.edu/myl/Shannon1950.pdf)
but for simplicity we will assume the characters are independent.

Notice that if we use the edit function and get back the identical ciphertext, we can say with confidence that
we have found the correct byte so we try all of the bytes from our list until the edit function returns
with no changes to the ciphertext.

```python
# this will store the characters we extract as we go along
extracted = b''

for i in range(len(newCt)):
    candidate = b''
    idx = -1
    while (candidate != newCt):
        idx += 1
        candidate = edit(newCt, i, freqs[idx])
    extracted += freqs[idx]
```

<br>

***

## Verifying our Solution

***

we then check using

```python
if __name__ == "__main__":
    print(extracted)
```

and as expected we get back the plaintext:

```
b"I'm back and I'm ringin' the bell \nA rockin' on the mike while the fly girls yell \nIn ecstasy in the back of me \nWell that's my DJ Deshay cuttin' all them Z's \nHittin' hard and the girlies goin' crazy \nVanilla's on the mike, man I'm not lazy. \n\nI'm lettin' my drug kick in \nIt controls my mouth and I begin \nTo just let it flow, let my concepts go \nMy posse's to the side yellin', Go Vanilla Go! \n\nSmooth 'cause that's the way I will be \nAnd if you don't give a damn, then \nWhy you starin' at me \nSo get off 'cause I control the stage \nThere's no dissin' allowed \nI'm in my own phase \nThe girlies sa y they love me and that is ok \nAnd I can dance better than any kid n' play \n\nStage 2 -- Yea the one ya' wanna listen to \nIt's off my head so let the beat play through \nSo I can funk it up and make it sound good \n1-2-3 Yo -- Knock on some wood \nFor good luck, I like my rhymes atrocious \nSupercalafragilisticexpialidocious \nI'm an effect and that you can bet \nI can take a fly girl and make her wet. \n\nI'm like Samson -- Samson to Delilah \nThere's no denyin', You can try to hang \nBut you'll keep tryin' to get my style \nOver and over, practice makes perfect \nBut not if you're a loafer. \n\nYou'll get nowhere, no place, no time, no girls \nSoon -- Oh my God, homebody, you probably eat \nSpaghetti with a spoon! Come on and say it! \n\nVIP. Vanilla Ice yep, yep, I'm comin' hard like a rhino \nIntoxicating so you stagger like a wino \nSo punks stop trying and girl stop cryin' \nVanilla Ice is sellin' and you people are buyin' \n'Cause why the freaks are jockin' like Crazy Glue \nMovin' and groovin' trying to sing along \nAll through the ghetto groovin' this here song \nNow you're amazed by the VIP posse. \n\nSteppin' so hard like a German Nazi \nStartled by the bases hittin' ground \nThere's no trippin' on mine, I'm just gettin' down \nSparkamatic, I'm hangin' tight like a fanatic \nYou trapped me once and I thought that \nYou might have it \nSo step down and lend me your ear \n'89 in my time! You, '90 is my year. \n\nYou're weakenin' fast, YO! and I can tell it \nYour body's gettin' hot, so, so I can smell it \nSo don't be mad and don't be sad \n'Cause the lyrics belong to ICE, You can call me Dad \nYou're pitchin' a fit, so step back and endure \nLet the witch doctor, Ice, do the dance to cure \nSo come up close and don't be square \nYou wanna battle me -- Anytime, anywhere \n\nYou thought that I was weak, Boy, you're dead wrong \nSo come on, everybody and sing this song \n\nSay -- Play that funky music Say, go white boy, go white boy go \nplay that funky music Go white boy, go white boy, go \nLay down and boogie and play that funky music till you die. \n\nPlay that funky music Come on, Come on, let me hear \nPlay that funky music white boy you say it, say it \nPlay that funky music A little louder now \nPlay that funky music, white boy Come on, Come on, Come on \nPlay that funky music \n"
```

[CTRdiagram]: https://upload.wikimedia.org/wikipedia/commons/3/3c/CTR_decryption_2.svg
