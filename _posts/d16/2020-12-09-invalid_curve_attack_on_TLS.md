---
layout: post
title: Invalid Curve Attacks on Elliptic Curve Diffie Hellman
category: 
author: 
tags: 
mathjax: true
---

Here we go over an intuitive idea for what an attack on ECDH which uses invalid curves would look like.
Some of the details were simplified which make the system insecure beyond our attack but in a future post
we go over a similar attack which was a real vulnerability in TLS libraries which implemented ECDH
such as [Bouncy Castle](https://www.bouncycastle.org/).

## Contents
{:.no_toc}

* Content
{:toc}

<br>

***

## Intro

***

As its name suggests, ECDH (Elliptic Curve Diffie Hellman) is a variation of the
[Diffie-Hellman protocol](https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange)
which uses Elliptic Curve Cryptography (ECC) to accomplish its goal of establishing a
shared secret over an insecure channel. It forms a large part in the security of
exchanging messages finding uses in TLS as well as messaging apps such as WhatsApp,
Facebook Messenger, and LINE.

<br>

***

## Notation

***

Since we're using Elliptice Curves for our asymmetric encryption, Bob is using
a set of standard domain parameters, perhaps a set recommended by NIST.
For simplicity, suppose we are working with curves in standard Weierstrass form over the field
$$\text{GF}(p)$$ where $$p$$ is prime.

$$E:= y^2\equiv x^3 +ax + b\pmod{p}$$

Denote the public and private keys of a user Bob as $$Q_B$$ and $$d_B$$ respectively.
If Alice and Bob use Diffie Hellman, the shared secret is then taken to be the
x coordinate of $$d_BQ_A = d_AQ_B$$

<br>

***

## Attack

***

We define $$E^*$$ is an *invalid curve with respect to* $$E$$ exactly when $$E$$
and $$E^*$$ differ only in their constant term $$b$$.

Let $$H(c)$$ be a cryptographic hash function and for a point
$$P=(P_x,P_y)$$ define the function $$x(P) = P_x$$.

Say we have a system where if Alice wishes to
connect with Bob, she sends her public key to Bob who responds with
$$H(x(d_BQ_A))$$. This way, Alice can verify that the secret was correctly
established by verifying

$$
H(x(d_AQ_B)) = H(x(d_BQ_A))
$$

There are two parts to this attack, an offline part followed by an online part.

<br>

***

### Offline Portion

***

Mallory computes some values with knowledge of terms such as
$$n=$$ number of points on the subgroup Bob is using. This part of NIST's
publicly available Domain parameters for instance.

let $$p_1,\ldots p_m$$ be small primes with $$m$$ chosen such that

$$
\prod_{i=1}^m p_i = B > n^2
$$

for convenience we denote $$B_i = B/p_i$$. Mallory computes $$m$$ points on invalid curves
with respect to the curve Bob is using such that the order of points
$$R_1,\ldots, R_m$$ correspond exactly with $$p_1,\ldots, p_m$$. Note that
we have

$$d^2_B < n^2 < B$$

<!--comment-->

<br>

***

### Online Portion

***

1. Mallory sends Bob $$R_1$$
2. Bob responds with $$H(x(d_BR_1))$$
3. Mallory computes $$H(x(R_1)),\ldots$$ until for some $$t_1$$ she has
$$H(x(t_1R_1)) = H(d_BR_1)$$

Mallory now knows $$t_1\equiv \pm d_B\pmod{p_1}$$ and further

$$
r_1\equiv t_1^2\equiv d_B^2\pmod{p_1}
$$

Repeating this for the remaining $$R_i$$ we have a system of congruences where the
Chinese Remainder Theorem may be used to solve for $$d^2_B$$. Mallory then simply
needs to compute the square root to find $$d_B$$.

Note that since the orders are chosen to be small primes, Mallory needs to compute
at most $$p_i$$ hashes in step 2. so the expected number of hash computations is
$$p_i/2$$.

<br>

***

## Example

***

Suppose Bob uses $$p=31$$ with a private key $$d_B=22$$ and curve

$$
E:= y^2\equiv x^3 + 10x + 26\pmod{31}
$$

Per our algorithm, Mallory precomputes points on invalid curves with respect to $$E$$:

$$
E^*_1:= y^2\equiv x^3 + 10x + 4\pmod{31}
$$

contains the point $$R_1=(23,30)$$ with order 5 and $$R_2=(6,30)$$ with order 7.

$$
E^*_2:= y^2\equiv x^3 + 10x + 23\pmod{31}
$$

contains $$R_3=(2,12)$$ with order 11 and

$$
E^*_3:= y^2\equiv x^3 + 10x + 7\pmod{31}
$$

has the point $$R_4=(1,24)$$ of order 13.
Mallory then does the online portion of our attack

1. Mallory starts a connection with Bob posting $$R_1$$ as her public key
2. Bob computes $$d_BR_1 = (18,23)$$ and following protocol, sends Mallory $$H(x(18,23))=H(18)$$
3. Mallory computes $$H(x(R_1)), H(x(2R_1))$$ finding that $$H(18)=H(x(2R_1))$$
4. Mallory now knows that $$d_B^2\equiv 2^2\equiv 5\equiv r_1\pmod{5}$$
5. Mallory repeats from step 1 using $$R_2,R_3,$$ and $$R_4$$

After these computations, Mallory has the following system of congruences:

$$
\begin{align}
d_B^2\equiv r_1 &\equiv 4 \pmod{5}\\
d_B^2\equiv r_2 &\equiv 1 \pmod{7}\\
d_B^2\equiv r_3 &\equiv 0 \pmod{11}\\
d_B^2\equiv r_4 &\equiv 3 \pmod{13}\\
\end{align}
$$

In order to use CRT we let $$x_i$$ be the solution to $$B_ix_i\equiv 1\pmod{p_i}$$ and
use it to compute the smallest positive solution which we are interested in.

$$
d_B^2 = \sum_{i=1}^4 r_i x_i\pmod{B}
$$

expanding we get $$d_B^2 = 484$$ hence $$d_B=22$$ as expected.
Notice that in this example, $$B=5\times 7\times 11\times 13=5005$$ so with these few steps
we can find private keys for any curve with fewer than $$\sqrt{5005}$$ points.
In fact, if we had also included primes 2 and 3 we would be able to determine
$$d_B$$ for all $$n$$ smaller than $$\sqrt{30030}$$. This is significantly faster
than a brute force approach.

<br>

***

## Preventing the attack

***

This attack relies on the fact that Bob computes point addition of points which may not even lie
on his curve. Since the algorithm for point addition in the group of points on Elliptic curves
does not depend on the constant term, Bob unwittingly leaks information on his private key
by correctly computing the result on small subgroups.

The easiest way to prevent this type of attack is to verify that the points being given in
fact lie on your curve. The recommended solution is to verify the point is a member of the
subgroup you are using before doing any processing involving the private key.

These posts are based on the works of Jager et. al and Antipa et. al:

T.  Jager,  J.  Schwenk,  and  J.  Somorovsky,  “Practical  invalid  curve  attacks  on  tls-ecdh,”  inEuropean Symposium on research in computer security, pp. 407–425, Springer, 2015.

A.  Antipa,  D.  Brown,  A.  Menezes,  R.  Struik,  and  S.  Vanstone,  “Validation  of  elliptic  curvepublic keys,”  inInternational Workshop on Public Key Cryptography,  pp. 211–223,  Springer,2003.

and the NIST recommendations

L. Chen, D. Moody, A. Regenscheid, and K. Randall, “Recommendations for discrete logarithm-based cryptography:  Elliptic curve domain parameters,” tech. rep., National Institute of Stan-dards and Technology, 2019.
