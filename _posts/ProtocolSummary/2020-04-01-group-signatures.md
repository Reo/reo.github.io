---
layout: post
title: 'Group Signatures'
category: 'Cryptographic Protocols'
author: 'reo'
tags: Protocols 'Digital Signature'
mathjax: true
---

Digital signatures can be extended to include protocols
where we want to retain some level of anonymity while still
needing to verify that a user is in fact a part of a
privileged group.

## Contents
{:.no_toc}

* Content
{:toc}

<br>

* * *

## Goals

* * *

The high-level goals here are

1. Only members of the group can sign messages
2. The receiver can verify that the signature is valid
3. The receiver cannot determine precisely who signed the document

<br>

* * *

## First Attempt

* * *

A simple approach can involve a trusted third party we'll call
Trent and gives Trent the ability to "open" the identity of the
signer should it be necessary.

The protocol is as follows:

1. Trent generates many private-public key pairs and gives every member $$m$$ unique private keys
2. The master list of all public keys is revealed with Trent keeping which corresponds to whom for himself
3. When a group member sign a document, they choose one of the $$m4$ keys at random
4. To verify the signature, the receiver matches it with one of the public keys on the master list
5. If there are any issues, Trent can identify which member the signature belongs to since he has the original list

<br>

* * *

### Problems

* * *

There are a few problems with this protocol which make it impractical.
The first being that it can require a very large number of keys, and
second, a trusted third party like Trent is hard to maintain and may
not exist.

<br>

* * *

## Ring Signatures

* * *

In this case, the assumtions are weakened so Trent is not needed while
the assertions in our goals still hold. Precisely,

1. Only members of the group can sign messages
2. The receiver can verify that the signature is valid
3. The receiver cannot determine precisely who signed the document

Note that since there is no trusted arbitrator, anonymity cannot be
revoked in this case.

<br>

* * *

### Generating the Signature

* * *

To generate a signature, Alice does the following: (see [1] for details)

1. Computes a symmetric key as the hash of the message to be signed $$k=H(m)$$
2. Picks a random number $$v$$ called "glue"
3. Picks random numbers $$x_i$$ for every ring member except herself
4. Computes $$y_i=g(x_i)$$ where $$g$$ is a [trapdoor function](https://en.wikipedia.org/wiki/Trapdoor_function)
5. Plug $$y_i$$ and $$v$$ into the *ring equation* $$C_{k,v}(y_1,\ldots,y_r)$$ solving for her corresponding $$y_s$$ value
6. Use knowledge of the trapdoor to compute $$x_i = g_s^{-1}(y_s)$$
7. The signature is $$(P_1,\ldots,P_r;v;x_1,\ldots,x_r)$$ where $$P_i$$ is the $$i$$th public key

Verifying the signature is much simpler. Given $$(P_1,\ldots,P_r;v;x_1,\ldots,x_r)$$,
and $$m$$ Bob does the following:

1. Computes $$y_i=g_i(x_i)$$ for $$i=1,\ldots, r$$
2. Computes $$k = H(m)$$
3. Verifies the ring equation $$C_{k,v}(y_1,\ldots,y_r)=v$$

Note that this protocol has proven unconditional security for the signer
and there are publicly available implementations.

This has potential applications in identifying membership (eg. key cards)
and cryptocurrency to obfuscate transaction details.

<br>

* * *

## References

* * *

Applied Crypto

https://link.springer.com/content/pdf/10.1007%252F3-540-45682-1_32.pdf

