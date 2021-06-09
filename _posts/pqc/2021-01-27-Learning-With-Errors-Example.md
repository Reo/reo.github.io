---
layout: post
title: 'Learning with Errors: Example'
category: Crypto
author: 'reo'
tags: LWE Lattice
mathjax: true
---

We go over an example of encryption and decryption presented in the last post as well as
how to establish a shared securely similar to diffie-hellman.

## Contents
{:.no_toc}

* Content
{:toc}

<br>

***

## Key Generation

***

We first need to agree on a modulus. For this small example, say we take $$q=7$$.

Next, we generate a matrix $$A\in\mathbb{Z}^{n\times n}$$ which will be used by both parties with entries sampled uniformly.
Suppose we choose $$n=3$$, $$A$$ could look something like

$$
A=
\begin{bmatrix}
6 & 4 & 5\\
3 & 6 & 3\\
6 & 1 & 2
\end{bmatrix}
$$

we similarly sample $$\pmb{s}$$:

$$
\pmb{s} = 
\begin{bmatrix}
5\\
2\\
3
\end{bmatrix}
$$

and finally the error from a discrete distibution similar to Gaussian

$$
\pmb{e} =
\begin{bmatrix}
1\\
0\\
1
\end{bmatrix}
$$

Computing $$\pmb{b} = A\pmb{s} + \pmb{e}$$ we have

$$
\pmb{b} =
\begin{bmatrix}
5\\
1\\
4
\end{bmatrix}
$$

Alice's public key is then $$(A, \pmb{b})$$

<br>

***

## Encryption

***

Suppose Bob would like to send a message to Alice.
For demonstration purposes, he will be sending a single bit, $$m$$.

Bob first generates his own secret and two error terms

$$
\pmb{s}' = 
\begin{bmatrix}
1,
5,
2
\end{bmatrix},\qquad

\pmb{e}' = 
\begin{bmatrix}
0,
-1,
-1
\end{bmatrix},\qquad

\pmb{e}'' = -1
$$

and computes the terms he will send

$$
\pmb{b}' = \pmb{s}'A + \pmb{e}' =
\begin{bmatrix}
5, 0, 2
\end{bmatrix},\qquad

v' = \pmb{s}'\pmb{b} + \pmb{e}'' = 4 - 1 = 3,\qquad

c = v' + \left\lfloor\frac{7}{2}\right\rfloor m = 3 + 3m
$$

Bob finally sends $$(\pmb{b}', c)$$ to Alice.

<br>

***

## Decryption

***

Alice can decrypt the bit sent by Bob (with high probability) as follows:
She first computes $$v = \pmb{b}'s = 3$$ and uses it to compute something close to
$$\left\lfloor\frac{7}{2}\right\rfloor m$$:

$$m' = c - v = 3 + 3m - 3 = 3m$$

Decoding is done by setting the received message to $$0$$ if
$$m'\in[-\left\lfloor\frac{q}{4}\right\rfloor,\left\lfloor\frac{q}{4}\right\rfloor]$$
and $$1$$ otherwise.

In our case, we would decode correctly either way as desired.

<br>

***

## Shared Secret

***

Taking a look at the values we computed, notice that $$v \approx \pmb{s}'A\pmb{s}$$
and $$v' \approx \pmb{s}'A\pmb{s}$$ so $$v\approx v'$$. This can be used as a shared
secret after rounding.

In particular, notice this involves combining values chosen by both parties.

<br>

***

## Conclusion

***

A real implementation which uses LWE can be seen in [Frodo KEM](https://frodokem.org/).
Frodo includes a Key Encapsulation Mechanism (simplified key exchange) while
minimizing error rate for LWE.

