---
layout: post
title: 'Key Escrow'
category: 'Cryptographic Protocols'
author: 'reo'
tags: Protocols 'Key Escrow' Politics
mathjax: true
---

It's no secret that government agencies around the world
have attempted to, and in some cases succeeded, in passing
legislation which give them "backdoor" access to
cryptosystems. Often with the pretext that criminals may
use these to communicate. Key Escrow is one proposed
"solution" to this issue.

## Contents
{:.no_toc}

* Content
{:toc}

<br>

* * *

## Goals

* * *

The goal of Key Escrow is really straight-forward. Give
someone (usually the authorities) a way to obtain the
keys used for encrypted communication so that if messages
are ever needed --- say, for a criminal investigation ---
they can be easily decrypted by an authorized party.

Ideally, the privacy of regular users should remain
intact, nobody should be able to obscure messages from the
authorities.

<br>

* * *

## Assumptions

* * *

There's a few (arguable lofty) assumptions being made here

1. There is a trusted KDC/authority
2. There is a sufficiently large set of (trusted) trustees
3. The trustees are available and cooperative
4. Alice and communicate securely with each of the trustees and KDC
5. The escrowed keys are the only ones valid for encryption

Notice that we'll use KDC instead of "authority" for brevity.

<br>

* * *

## First Attempt (Fair Cryptosystems)

* * *

One of the earliest implementations is as follows

1. Alice generates public/secret key pair $$(p_k,s_k)$$ and splits $$s_k$$ into public and secret pieces
2. Alice sends a public and corresponding secret piece to each trustee and her public key to KDC
3. The trustees verify their public/secret pairs, store the secret part, and send KDC the public part
4. KDC verifies the public pieces against the public key, signs the public key, and sends it to Alice/posts it

If Alice's messages later need to be decrypted, the
authorities simply tell the trustees to forfeit their
secret pieces and reconstruct the secret.

<br>

* * *

### Cons of Fair Cryptosystems

* * *

The fact that we need all trustees to cooperate could
be an issue (may prefer to use a variation on secret
sharing instead).

We can establish some stronger and more concrete
goals after this first attempt

<br>

* * *

## Strengthening the Goals

* * *

1. Users should have enough control over the keys to be sure they are secure
2. The authority should be guaranteed the secret keys are in fact random (no bad keys)
3. User should be guaranteed that their secret key is revealed iff enough trustees release their shares to the authority
4. The authority should be able to obtain the secret key for a target by collecting keys from a certain number of trustees
5. The system should not be able to allow obscured communication when the keys are revealed

<br>

* * *

## Failsafe Key Escrow

* * *

This scheme shares some similarities with traditional Diffie-Hellman exchange.

Let $$p$$ be prime and $$g$$ a generator of $$\mathbb{Z}_p$$
(both public parameters).

1. The KDC chooses $$y \in [0,p-2]$$ randomly and commits $$y$$ using a commitment scheme
2. $$A$$ picks a random secret value $$x \in [0,p-2]$$ and sends the KDC $$g^x \pmod{p}$$
3. $$A$$ shares $$x$$ with the trustees using a Verifiable Secret Sharing scheme
4. KDC reveals $$y$$ to $$A$$
5. $$A$$ verifies the commitment and sets her public key $$P_A = (G^x)G^y \pmod{p}$$
6. $$A$$ sets her secret key to be $$S_A = x + y \pmod{p-1}$$

<br>

* * *

## Applications

* * *

This has applications in national security laws passed in nations such as
the United Kingdom (see
[RIPA 2000](https://en.wikipedia.org/wiki/Regulation_of_Investigatory_Powers_Act_2000)).
In these cases, government agencies want to be able to
decrypt communication given sufficient clearance.

Of course these don't come without their own set of
downsides, but there's enough there for an entirely
separate article.

<br>

* * *

## References

* * *

Applied Cryptography 4.14

