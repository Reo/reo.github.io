---
layout: post
title: 'Steganography and Subliminal Channels'
category: 'Cryptographic Protocols'
author: 'reo'
tags: Protocols Steganography 'Subliminal Channel' 'Digital Signature' 'ElGamal'
mathjax: true
---

Defined as concealing a message within another (ie. in plain sight),
steganography on its own is actually not considered to be a cipher.
There are however techniques which should interest any security
professional since it allows disclosure of information.
We also go over a way to hide messages within signature schemes
(specifically ElGamal signatures) which are properly encrypted.

## Contents
{:.no_toc}

* Content
{:toc}

<br>

* * *

## Steganography

* * *

An easy example of steganography would be if you were to grab
a newspaper and puncture the space above the letters of a text
you wanted to share. Another example would be adding an extra
space in the beginning of words which have the desired letters.
This works since the rendered HTML does not preserve these
additional spaces but the intended recipient would know to check
the source where they can then retrieve the message.

<br>

* * *

## In Practice

* * *

One of the most popular software for steganography is
[QuickStego](http://quickcrypto.com/free-steganography-software.html)
which hides text in image files by making very minute changes
which are often undetectable to everyone except someone who knows
to look for the message.

<br>

* * *

## Subliminal Channels

* * *

Suppose Alice and Bob live in a country where exchange of
encrypted messages is outlawed. They cannot use traditional
encryption techniques and Walter is in charge of monitoring
their internet communications to ensure their messages
are in fact in plaintext.

It would be possible to use steganography such as the HTML
example given above but if Walter is clever enough these can
still be found out. Lucky for Alice and Bob however, signature
schemes are still permitted. Here is how Alice and Bob can
still privately exchange encrypted messages without Walter
knowing.

<br>

### Hiding Messages using elGamal Signatures

Suppose Alice
and Bob meet up and exchange a symmetric key $$r$$.

Alice initializes the basic ElGamal signature scheme by
choosing a prime $$p$$, having $$g,r$$ be random numbers
both less than
$$p$$, and computing $$K=g^r\pmod{p}$$.

Alice's public key is $$(K,g,p)$$.

To send a subliminal message $$M$$ using the inoffensive message
$$M'$$ we need $$M, M', p$$ pairwise prime and $$M,(p-1)$$ also
relatively prime.

<br>

### The Algorithm

1. Alice computes $$X = g^M mod p$$ and solves for $$Y$$ in $$M’ = rX + MY \pmod{p-1}$$ [Extended Euclidean]
2. Alice attaches her signature $$(X,Y)$$ as specified in the basic ElGamal scheme
3. Walter can verify the signature is legitimate by confirming $$K^XX^Y = g^{M’} \pmod{p}$$
4. Bob verifies $$(g^r)^XX^Y = g^{M’} \pmod{p}$$ to ensure the message is genuine and $$r$$ is valid
5. Bob recovers the hidden message by computing $$M = (Y^{-1}(M’-rX)) \pmod{p-1}$$

<br>

### Example

This example is courtesy of Schneier's Applied Cryptography:

Let $$p=11,g=2,r=8$$. This makes the publilc key (which Walter
can verify himself) $$2^8\pmod{11} = 3$$.

To send $$M$$ using innocent message $$M'=5$$, Alice confirms that
$$\{5, 9, 11\}$$ are pairwise prime as well as $$\{9, 10\}$$. Since
they are, she may continue to solve for $$X=6$$ and $$Y=3$$.

The signature is then the pair $$(X,Y) = (6,3)$$.
Bob can verify $$(2^8)^66^3\equiv 2^5\pmod{11}$$ and recovers $$M$$

$$
3^{-1}(5-8\times 6)\pmod{10} = 49\pmod{10} = 9 = M
$$

as expected. From Walter's point of view, Alice and Bob simply
exchanged signatures.

<br>

* * *

## Lessons Learned

* * *

This shows just how careful one must be if they plan on supervising
communications, for instance in protecting intellectual property.
Signature schemes which have protection against these subliminal
channels have been proposed though it's quite possible other
protocols also include similar unconventional methods of communicating.

<br>

* * *

## References

* * *

applied crypto 4.2, 23.3

https://link.springer.com/chapter/10.1007/978-3-642-21031-0_21

