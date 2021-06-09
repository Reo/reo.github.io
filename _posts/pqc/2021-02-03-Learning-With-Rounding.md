---
layout: post
title: 'Post-Quantum Cryptography: Learning with Rounding'
category: Crypto
author: 'reo'
tags: LWR Lattice
featured: 1
mathjax: true
---

A brief introduction to Learning with Rounding (LWR) based on papers by
Banerjee et al. and Alwen et al.


## Contents
{:.no_toc}

* Content
{:toc}

<br>

***

## The Idea

***

In LWE, we sampled an error vector from a Gaussian distribution to fuzz the solution to a set of linear equations.
This sampling may be a source of slowdown for the algorithm if, for instance, rejection sampling is used.

In LWR, we generate the analog to errors deterministically by rounding an element in $$\mathbb{Z}_q$$ to
one in a more spare set such as $$\mathbb{Z}_p$$ where $$p < q$$.
<!---->
We can then formalize our rounding procedure by defining
$$\left\lfloor x\right \rceil_p = \left\lfloor \frac{p}{q}x\right \rceil \pmod{p}$$
where $$\left\lfloor x\right \rceil$$ denotes the nearest integer to $$x$$.

We can simplify this further by choosing $$q$$ and $$p$$ to be powers of $$2$$, say,

$$q = 2^{\epsilon_q},\quad p = 2^{\epsilon_p}$$

where $$\epsilon_q, \epsilon_p$$ are positive integers such that $$\epsilon_q > \epsilon_p$$.
This simplifies our rounding operation since now $$p/q = 2^{\epsilon_p - \epsilon_q}$$ which is equivalent to shifting
$$\epsilon_q - \epsilon_p$$ bits to the right; the mod $$p$$ is implicit in this operation.

The modulus operations are also more efficient to implement since taking mod $$q$$ is equivalent to saying
keep the $$q$$ least significant bits (and similarly for mod $$p$$).

<br>

***

## Hardness and Relation to LWE

***

Notice that if $$s = \epsilon_q - \epsilon_p$$ is small then the rounding operation is actually equivalent to
adding a small error which makes the lower $$s$$ bits $$0$$. This similarity is convenient because it hints
towards LWR being similar to LWE in terms of hardness, at least for certain parameters.

One of the first results [[BPR12](https://eprint.iacr.org/2011/401.pdf)] showed that LWR is as hard as LWE
for parameters chosen so the modulus and modulus-to-error ratio are super-polynomial. This requirement was
then improved in [[AKPW](https://eprint.iacr.org/2013/098.pdf)] with a new reduction which proves hardness
for a larger set of parameters including polynomial modulus and modulus-to-error ratio.

This allows for an increase in security and efficiency which helped increase the popularity of this technique.

<br>

***

## Key Exchange

***

The basic algorithm for key exchange between Alice and Bob is similar to the one we saw in LWE.
We denote a shift to the right by $$k$$ bits as $$\gg k$$ and $$msb(x)$$ the most significant bit
of $$x$$ (with $$\epsilon_p$$ bits). Our algorithm also introduces $$\epsilon_t$$
which should be small relative to $$\epsilon_q$$ and we have $$t=2^{\epsilon_t}$$ respectively.

1. Alice generates $$A\in\mathbb{Z}_q^{l\times l}$$ with coefficients chosen uniformly and $$s\in\mathbb{Z}_q^{l\times 1}$$ Gaussian.
2. Alice computes and sends $$b=(As \bmod q) \gg (\epsilon_q - \epsilon_p)\in \mathbb{Z}_p^{l\times 1}$$ to Bob.

Notice that instead of adding an error, the public key $$b$$ is determined by rounding.
Up next, Bob does his part:

1. Bob generates $$s'\in\mathbb{Z}_q^{l\times 1}$$ Gaussian
2. computes $$b' = (A^T s' \bmod q) \gg (\epsilon_q - \epsilon_p)\in \mathbb{Z}_p^{l\times 1}$$
3. computes $$v' = b^T(s'\bmod p)\in \mathbb{Z}_p$$
4. computes $$c  = ((v'\bmod p) \gg (\epsilon_p - \epsilon_t - 1)\bmod t)\in \mathbb{Z}_t$$
5. computes $$k' = msb(v')$$
6. finally, Bob sends $$b', c$$ to Alice

Alice completes the procedure again similarly to LWE. Another difference to notice is that the
shared bit is encoded in the most significant bit.

3. Alice computes $$v = b'^T(s\bmod p)\in \mathbb{Z}_p$$
4. computes $$k = msb(v - 2^{\epsilon_p - \epsilon_t - 1}c)$$

<br>

* * *

## Correctness

* * *

Similar to LWE, there is some probability that both parties will not agree on the same key but
we're happy as long as there's a reasonable probability of success.

From the algorithm, we want

$$k' = k$$

we see $$v$$ and $$v'$$ are close

$$v = b'^T(s\bmod p) = ((A^T s' \bmod q) \gg (\epsilon_q - \epsilon_p))^T(s\bmod p) \approx s'^TAs$$

$$v' = b^T(s'\bmod p) = ((As \bmod q) \gg (\epsilon_q - \epsilon_p))^T(s'\bmod p) \approx s^TA^Ts' = s'^TAs$$

$$c$$ can be though of as a correction which is used to make $$v$$ closer to $$v'$$ which used by Bob
to find his side of the key.

to see why the last equality holds we recall that the transpose of a $$1\times 1$$ matrix is itself
so $$s^TA^Ts' = (s^TA^Ts')^T = s'^TAs$$. Since the shared secret will be the most significant bit
of $$v$$ and $$v'$$ and we have that $$v\approx v'$$ we have that with high probability, Alice and Bob
agree on a secret.

<br>

***

### Asymmetric Encryption

***

Encrypting $$m$$ is done similarly with the only difference being instead of computing $$c$$,
you compute $$c_m=(v' + 2^{\epsilon_p-1}m\bmod p)\gg (\epsilon_p - \epsilon_t - 1)\in\mathbb{Z}_{2t}$$.

To decrypt, Alice would compute $$msb(m')$$ where $$m' = (v - 2^{\epsilon_p - \epsilon_t - 1}c_m)$$.

<br>

***

## Example

***

As for concrete numbers, we can use $$\epsilon_q = 13, \epsilon_p = 10, \epsilon_t = 3$$ (so there is a corresponding $$t=2^{\epsilon_t}$$)
Choose $$l=3$$

For high correctness, we choose a moderatiely small variance for our gaussian: $$\sigma = 2^6$$ but higher security purposes may want to choose
higher variance for more security. (the distribution is also truncated at $$\pm \sigma/2$$)

the numbers here were generated in python using `randint(0,q-1)` from the `random` package for uniform distributions and
a rounded `truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)` from `scipy.stats` package
for the Gaussian distribution.

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

we get

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

Now it's Bob's turn:

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

as expected

<br>

***
### Example
***

Using the same values from our earlier example and $$m = 1$$ we have

$$c_m = (799 + 2^9\bmod p)\gg (10 - 3 - 1) = 287 \gg 6  = 4$$

$$msb(m') = msb(801 - 2^{6}4) = msb(545) = 1$$

if instead $$m=0$$ then $$c_m = 12$$ and $$msb(m') = msb(801 - 2^6\cdot12) = msb(801-768) = msb(33) = 0$$ as expected

<br>

***

## Conclusion

***

Though similar to LWE, LWR is becoming increasingly preffered due to the fact that it does not rely on
needing to sample error terms (making it more efficient).
There have also been developments which seem to indicate that [LWR can be just as "hard" to solve as LWE](https://eprint.iacr.org/2016/589).

There is now only one more variant to talk about before we're prepared to talk about one of the round 3 finalists
for NIST post-quantum Key-Establishment algorithms. SABER. We will again be building on the theory covered so far
so understanding LWR will be useful.

<br>

* * *
### Additional Resources:
* * *

`Banerjee, A., Peikert, C., & Rosen, A. (2012, April). Pseudorandom functions and lattices. In Annual International Conference on the Theory and Applications of Cryptographic Techniques (pp. 719-737). Springer, Berlin, Heidelberg.`

`Alwen, J., Krenn, S., Pietrzak, K., & Wichs, D. (2013, August). Learning with rounding, revisited. In Annual Cryptology Conference (pp. 57-74). Springer, Berlin, Heidelberg.`


