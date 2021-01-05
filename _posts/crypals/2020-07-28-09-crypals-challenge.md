---
layout: post
title: Cryptopals Challenge 9
category: crypto
author: 'reo'
tags: python cryptopals
mathjax: 
---

Challenge 9 is the first of the second set, it is relatively straight-forward involving only padding a string to
ensure the length is a multiple of a given blocksize. We will implement PKCS#7 padding where a pad of length `k`
is done by appending `k` bytes of that same value.

```python
AES_BLOCKSIZE=16
def pad(b, blocksize=AES_BLOCKSIZE):
    r = blocksize - (len(b) % blocksize)
    return b + (bytes([r])*r)
```

Testing it we see
```python
print(pad2size(b'YELLOW SUBMARINE', 20))
# > YELLOW SUBMARINE\x04\x04\x04\x04
```

as we expect. This may come in handy for later challenges so we call this file `pkcs7.py` for easy importing in the future.
Since we have worked with AES it's also be a good idea to have a way to interface without specifying the blocksize
and have it use the standard 16 byte size. That's why we set the default argument accordingly.
