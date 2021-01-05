---
layout: post
title: Cryptopals Challenge 13
category: crypto
author: 'reo'
tags: python cryptopals
mathjax: 
---

This Cut and Paste attack is a continuation of the [cryptopals challenges](https://cryptopals.com/)
we have been solving and are now halfway into the second set. We manipulate the ciphertext
to send the server a query string which would not be allowed under normal circumstances.

## Contents
{:.no_toc}

* Content
{:toc}

<br>

***

## System Set Up

***

In order to make a valid response, we need to implement the reverse operation
to our padding in `pkcs7.py` which we wrote in a [previous post](/crypto/2020/07/28/09-crypals-challenge.html)

The pad we created intentionally to make unpadding easy, we simply
remove the last `k` bytes where `k` is the numerical value of the final byte.

```python
def unpad(b, blocksize=AES_BLOCKSIZE):
    r = b[-1]
    return b[:-r]
```

Assume we have a system where a user can make an account with their email using a function
that encodes a the profile in a query-string-format. For instance, given
a string `name@mail.com` it produces

`email=name@mail.com&uid=10&role=user`

This function refuses to encode anything with metacharacters `&` or `=` so
as to prevent attackers from sending a string like
`mallory@hacker.com&role=admin`.

The system sends an ecb-encrypted version of the string it produces back to the user.

To verify, the user would send the same ciphertext again which the server
deciphers and creates a JSON object out of the deciphered string.
Using our first example again, the server would create

```
{
  email: 'name@mail.com',
  uid: 10,
  role: 'user'
}
```

and assign permissions etc. accordingly.

<br>

***

## System Implementation

***

We first implement this fictitious service starting with creating a
profile given an email. For simplicity, we hard-code user id as 10.

```python
GKEY = urandom(16)

def profile_for(email):
    # don't allow '&' or '=' as part of an email
    if (('&' in email) or ('=' in email)):
        return None
    s = 'email='+email+'&uid=10&role=user'
    data = pad(s.encode())
    return ecb_enc(data, GKEY)
```

Next, we need to be able to retrieve the profile from ciphertext
and parse the query string:

```python
def profile_from_ciphertext(encoded_ct):
    pt = unpad(ecb_dec(encoded_ct,GKEY)).decode()
    return parse_q(pt)
```

`parse_q()` simply parses the querystring and returns the object. Recall this
would be done server-side:

```python
def parse_q(q):
    ret = dict()
    items = q.split('&')
    for pair in items:
        keyval = pair.split('=')
        ret[keyval[0]] = keyval[1]
    return(ret)
```

<br>

***

## Manipulating the Ciphertext

***

Our goal is to take advantage of the fact that ECB mode does not
rely on previous blocks to create a ciphertext which has us on an admin role
despite creating an account as a regular user.

The idea here is to 'cut and paste' blocks from the ciphertext changing only the order
they appear when decrypted. This is facilitated by hte fact that we know how the
`profile_for()` function manipulates its input.

we could choose
```python
malstr = 'xyzw@mail.admin' + (bytes([11])*11).decode() + 'com'
malct = profile_for(malstr)
```

The ciphertext in terms of blocks is now
```
email=xyzw@mail.  ||  admin<0x0b*11>  ||  com&uid=10&role=  ||  user<padding>
```

notice that manipulating these blocks by switching the second and third and omitting
the last we get

```
email=xyzw@mail.  ||  com&uid=10&role=  ||  admin<0x0b*11>
```

so we add

```python
malct = malct[:16] + malct[32:48] + malct[16:32]
```

this is exactly what we want and this can be verified by printing

```python
print(profile_from_ciphertext(malct))
# > {'email': 'xyzw@mail.com', 'uid': '10', 'role': 'admin'}
```

