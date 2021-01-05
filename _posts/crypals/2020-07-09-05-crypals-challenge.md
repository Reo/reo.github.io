---
layout: post
title: Cryptopals Challenge 5
category: crypto
author: 'reo'
tags: python cryptopals
mathjax:
---

This [cryptopals challenge](https://cryptopals.com/) asks us to implement a cipher similar to the [Vignère cipher](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher),
repeating key XOR.

A simple implementation here is to simply encrypt the plaintext byte-by-byte by XORing against the key

```python
def xor_line(key, pt):
    # key and pt are bytes objects
    # apply key bytewise
    res = b''
    for i in range(len(pt)):
        res += bytes([key[i % len(key)] ^ pt[i]])
        return res
```

Encrypting and decrypting here are symmetric in the sense that both are done by applying the same operation,
here is an example of what encrypting would look like using the provided text and key:

```python
print(xor_line(b'ICE', b"Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal").hex())
# > 0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f
```
