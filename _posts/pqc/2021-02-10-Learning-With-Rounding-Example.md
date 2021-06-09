---
layout: post
title: 'Learning with Rounding Example'
category: Crypto
author: 'reo'
tags: LWR Lattice
mathjax: true
---

A small example of Learning with Rounding key agreement and Encryption/Decryption
for better understanding the procedure.

## Contents
{:.no_toc}

* Content
{:toc}

<br>

***

## Parameter choices

***

Using the same notation as the introductory article, we may choose
$$\epsilon_q = 13, \epsilon_p = 10, \epsilon_t = 3$$ and $$l=3$$.

For high correctness, we choose a moderatiely small variance for our gaussian: $$\sigma = 2^6$$ but higher security purposes may want to choose
higher variance for more security. (the distribution is also truncated at $$\pm \sigma/2$$).

As always, these values were simply chosen for example's sake, the dimension $$l=3$$ in particular is too small
for security applications.

<br>

* * *

## Key Agreement Example

* * *

As a technical note, 
the numbers here were generated in python using `randint(0,q-1)` from the `random` package for uniform distributions and
a rounded `truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)` from `scipy.stats` package
for those sampled from a Gaussian distribution.

Following our algorithm from the previous post, Alice generates

$$
A=
\begin{bmatrix}
4768 &
7514 &
2031 \\
331 &
6544 &
2947 \\
7512 &
4568 &
4028
\end{bmatrix}
,\qquad
\pmb{s} = 
\begin{bmatrix}
22\\
-17\\
10
\end{bmatrix}
$$

and computes

$$
As\bmod q =
\begin{bmatrix}
5660\\
7424\\
5008
\end{bmatrix}
$$

bit shifting right by $$\epsilon_q - \epsilon_p = 3$$ we get

$$
b=
\begin{bmatrix}
707\\
928\\
626
\end{bmatrix}
$$

Bob now generates his own secret key

$$
\pmb{s}' = 
\begin{bmatrix}
-9\\
16\\
-27
\end{bmatrix}
$$

notice in our case $$s = s\bmod p$$ and also $$s' = s'\bmod p$$. This is convenient for computation.

$$
A^Ts'\bmod q =
\begin{bmatrix}
5320\\
3854\\
2037
\end{bmatrix}
$$

bit shifting right by $$\epsilon_q - \epsilon_p = 3$$ and $$\epsilon_p - \epsilon_t = 7$$
respectively we get

$$
b'=
\begin{bmatrix}
665\\
481\\
254
\end{bmatrix}
,\quad
v' = -8417 \bmod p = 799
,\quad
c = 4
,\quad
k' = msb(799) = 1
$$

Finally, Alice completes the process using $$r = 2^{\epsilon_p - \epsilon_t - 1}c = 64 * 4 = 256$$

$$
v = 8993\bmod p = 801
k = msb(v - r) = msb(801 - 256) = msb(545) = 1
$$

as expected.

<br>

***

## Asymmetric Encryption Example

***

Recall that for asymmetric encryption, instead of computing $$c$$,
you compute $$c_m=(v' + 2^{\epsilon_p-1}m\bmod p)\gg (\epsilon_p - \epsilon_t - 1)\in\mathbb{Z}_{2t}$$.

To decrypt, Alice would compute $$msb(m')$$ where $$m' = (v - 2^{\epsilon_p - \epsilon_t - 1}c_m)$$.

Using the same values from our earlier example and $$m = 1$$ we have

$$c_m = (799 + 2^9\bmod p)\gg (10 - 3 - 1) = 287 \gg 6  = 4$$

$$msb(m') = msb(801 - 2^{6}4) = msb(545) = 1$$

if instead $$m=0$$ then $$c_m = 12$$ and $$msb(m') = msb(801 - 2^6\cdot12) = msb(801-768) = msb(33) = 0$$ as expected.

