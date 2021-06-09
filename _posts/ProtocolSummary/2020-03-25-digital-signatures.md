---
layout: post
title: 'Summary of Digital Signature Schemes'
category: 'Cryptographic Protocols'
author: 'reo'
tags: 'Digital Signature'
mathjax: true
---

With the increasingly widespread use of digital document
formats, it quickly became obvious that physical signatures
needed a digital, mathematically secure equivalent.

## Contents
{:.no_toc}

* Content
{:toc}

<br>

* * *

## Goals

* * *

There are a few requirements which we expect signatures to
fulfil both in the traditional setting and digitally.

1. The signature cannot be forged
2. The signature must be authentic
3. The signature cannot be "moved" to a different document
4. The signed document cannot be altered
5. The signature cannot be repudiated

<br>

* * *

## Using Public-key Cryptography

* * *

Public-key cryptography (in particular RSA) gives a
straight-forward solution with some limitations.
The idea is that instead of "encrypting" with the
recipient's public key, Alice would encrypt with
her own secret key. Let's take a look at why this appears
to work.

<br>

### Forgery

This signature cannot be forged since the only person who
could have encrypted the message which corresponds to Alice's
public key must have Alice's secret key (which we assume is
only Alice otherwise we have much larger issues).

<br>

### Authentic

Bob can verify the signature is authentic using Alice's
public key.

<br>

### Reusable

Bob cannot "move" the signature since that would require
encrypting using Alice's secret key which he doesn't have.

<br>

### Cannot be Altered

Similar to moving the signature, altering the document would
require Bob to know Alice's secret key.

<br>

### Non-repudiation

Since we assume Alice is the only one in possession of her
secret key, she cannot reasonably deny having signed the document.

<br>

* * *

## Weakening the Assumptions

* * *

There is however one potentially fatal flaw to only using the
public-key approach. Consider the situation where Alice signs
a document where she authorizes Bob to perform something on
her behalf, perhaps move money. Bob can present this digital
signature as many times as he wants and as long as Alice has
the same public-private key pair, continues to have these
permissions.

This can be somewhat solved using timestamps (a combined
approach like this is similar to what Adobe uses for their
signature scheme).

Even with this proposed solution why stop there? We can have
stronger (or strictly weaker) requirements we want from a
digital signature.

<br>

* * *

## Non-transferable Signatures

* * *

In this case, Alice wants to sign a document so that
the only way to verify its authenticity is to participate
in an interactive protocol. This prevents Bob from obtaining
a signed document from Alice and later use it to blackmail
her since Alice can simply choose to not verify.

Here is a basic protocol which can help get the idea across

<br>

### Example

Suppose Alice has private key $$x$$, public key $$g^x\pmod{p}$$ and
signs $$m$$ which she sends to Bob as $$z=m^x\pmod{p}$$. Bob can
verify the signature as follows

1. Bob chooses $$a, b$$ random integers less than $$p$$ and sends Alice $$c=z^a(g^x)^b\pmod{p}$$
2. Alice computes $$t=x^{-1}\pmod{p-1}$$ and sends Bob $$d=c^t\pmod{p}$$
3. Bob confirms $$d\equiv m^ag^b\pmod{p}$$

Bob should be convinced that Alice has the corresponding private key
but cannot convince a third party of the signature using only the
transcript since there is no way to know if the numbers were actually
random or if Bob just "worked backwards" from the $$d$$ he was looking for.

There are more sophisticated protocols which also allow Alice to
explicitly disavow a false signature.

<br>

* * *

## Fail-Stop Signatures

* * *

In this scenario, Alice wants to protect herself in case a brute-force
attack manages to steal her secret key and starts signing documents on
her behalf.

This can be done by generating many secret keys which correspond to the
same public key. Here if Alice wants to dispute a signature, she would
show that the document with the forged signature and one with her real
signature are distinct and still correspond to the same public key.

Alice would need to generate sufficient secret keys to make the probability
of an attack finding the one she uses sufficiently small.
This doesn't have many practical uses but it is an interesting area of study.

<br>

* * *

## References

* * *

Applied Crypto 23.4

[1] https://helpx.adobe.com/acrobat/using/certificate-based-signatures.html

