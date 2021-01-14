---
layout: post
title: 'Post-Quantum Cryptography: NTRU'
category: Crypto
author: 'reo'
tags: NTRU lattice
mathjax: true
---

Along with discussions of large-scale quantum computers comes the often cited threats to
cryptography currently in use. Though some may argue we are still a ways away from anything
we should be concerned about, recent developments seem to indicate [Shor's Algorithm](https://en.wikipedia.org/wiki/Shor%27s_algorithm)
is not too far off.

## Contents
{:.no_toc}

* Content
{:toc}

<br>

***

## Intro

***

There are a number of practial factors currently delaying the development of a large-scale quantum computer
but some experts believe it may not be too far off with Michele Mosca
[having written](https://eprint.iacr.org/2015/1075).

> I estimate a 1/7 chance of breaking RSA-2048 by 2026 and a 1/2 chance by 2031.

and in October 2019 a milestone was achieved with an example of
[Quantum Supremacy](https://www.nature.com/articles/s41586-019-1666-5).

> Our Sycamore processor takes about 200 seconds to sample one instance of a
> quantum circuit a million times—our benchmarks currently indicate that the
> equivalent task for a state-of-the-art classical supercomputer would take
> approximately 10,000 years.

Further, [IBM claims](https://techcrunch.com/2020/09/15/ibm-publishes-its-quantum-roadmap-says-it-will-have-a-1000-qubit-machine-in-2023/)

> it is on its way to building a quantum processor with more than 1,000 qubits — and somewhere between 10 and 50 logical qubits — by the end of 2023.

clearly quantum computation is scaling up and could be a threat to cryptographic standards if no change is made.
For that purpose, NIST began a [post-quantum crypto](https://csrc.nist.gov/projects/post-quantum-cryptography)
project and a number of post-quantum cryptography algorithms have been proposed. One which particularly appears to have
great promise is Lattice-based cryptography.

<br>

***

## Definitions and Review

***

Lattices are very similar to traditional vector spaces which are often taught in a first course of linear algebra.
A lattice over linearly independent $$\pmb{v}_1,\ldots \pmb{v}_n$$ can be defined as:

$$
\left\{
\sum_{i=1}^n\alpha_i\pmb{v}_i\:\Big|\: \alpha_i\in\mathbb{Z}
\right\}
$$

in essense, it's the same as a real vector space with the exception that the scalars are taken to be integral.
More precisely, these lattices are isomorphic to the group $$\mathbb{Z}^n$$ with binary operation $$+$$.

There are interesting problems here such as the *Shortest Vector Problem* (SVP) which has been [proven](https://dl.acm.org/doi/10.1145/237814.237838)
to be NP hard in some cases and the *Closest Vector Problem* with [similar results](https://www.sciencedirect.com/science/article/abs/pii/S0020019099000836?via%3Dihub)
in terms of hardness.

|![SVP example](https://upload.wikimedia.org/wikipedia/commons/3/32/SVP.svg){:class="svg invert-color"}|
|:--:|
| *A basic example of SVP, given b1, b2 find the vector in cyan (courtesy, Wikipedia)* |

Though the problem seems quite easy in the diagram above, the difficulty in solving quickly ramps up as the number of
dimensions increases.

Recall that $$\mathbb{Z}[X]/(X^N-1)$$ is the ring of polynomials with coefficients in $$\mathbb{Z}$$ and powers of
$$X$$ strictly less than $$N$$. We define multiplication of polynomials in this ring as follows

$$
f * g = c_{N-1}X^{N-1} + \cdots + c_0
$$

where if $$a_j$$ denotes the $$j$$th coefficient of $$f$$ and $$b_k$$ the $$k$$th of $$g$$ then

$$
c_i = \sum_{j+k\equiv i}a_jb_k,\qquad\quad i\in\{0,\ldots N-1\}
$$

the congruence taken mod $$N$$ of course.

<br>

***

## NTRU (Public Key Encryption) Setup

***

Here is only one variation on NTRU though many have been proposed.

All parties agree on integers $$N,p,q$$ such that gcd$$(p,q)=1$$ and $$p\ll q$$.
They also individually pick polynomials $$f,g\in\mathbb{Z}[X]/(x^N-1)$$, say

$$
f = a_{N-1}X^{N-1} +\cdots + a_0\qquad\text{and}\qquad g = b_{N-1}X^{N-1} +\cdots + b_0\:\:\text{.}
$$

Let

$$
h=f*g = c_{N-1}X^{N-1} + \cdot + c_0
$$

Note that $$f$$ must be invertible mod $$p$$ and mod $$q$$ ie. there exists $$F_p,F_q\in\mathbb{Z}[X]/(x^N-1)$$
such that

$$
F_p*f \equiv 1\pmod{p}\qquad\text{and}\qquad F_q*f\equiv 1\pmod{p}
$$

the public key is then

$$
(N,p,q,h)
$$

and the private key is $$(f,F_p)$$. Note that $$g\equiv f*h\pmod{q}$$ so nothing is lost by not storing it
should it be needed.

<br>

***

## NTRU Asymmetric Encryption/Decryption

***

Alice sends a message $$m$$ to Bob as follows:
1. Encodes $$m$$ as a polynomial in $$\mathbb{Z}[X]/(x^N-1)$$ with coefficients no larger than $$(p-1)/2$$ in magnitude.
2. Choose a "small" polynomial $$\phi$$ and compute $$c\equiv p\phi*h + m\pmod{q}$$.
3. Send the ciphertext $$c$$ to Bob

Bob can then attempt to decrypt the message:
1. Compute $$a\equiv f*c\pmod{q}$$ with all coefficients in $$a$$ being at most $$q/2$$ in magnitude
2. (Likely) recover the message with $$m \equiv F_p*a\pmod{p}$$

There are parameters which have been shown to make failure extremely unlikely but we can examine why this
usually works.

<br>

***

## Informal Proof

***

We want to show Bob receives the intended message from Alice. From the algorithm, we have

$$
\begin{align}
a &\equiv f*c\pmod{q}\\
  &\equiv f*(p\phi * h + m)\pmod{q}\\
  &\equiv f*p\phi*F_q*g + f*m\pmod{q}\\
  &\equiv p\phi*g + f*m\pmod{q}
\end{align}
$$

Since $$\phi,g,f,m$$ have small coefficients and $$q$$ is much larger than $$p$$ it is very likely that
$$p\phi*h+f*m$$ has coefficients with magnitude less than $$q/2$$ (before taking mod $$q$$) in which case

$$
a=p\phi*g+f*m
$$

holds. Multiplying $$F_p$$ we have

$$
F_p*a = pF_p*\phi*g + F_p*f*m\equiv 0 + 1*m\equiv m\pmod{p}
$$

as expected.

<br>

***

## Small Example

***

Suppose we have parameters $$(N,p,q) = (5,3,16)$$ and
Bob chooses $$f=X^4+X-1$$, $$g=X^3 -X$$. We find

$$
F_p= X^3+X^2-1,\quad F_q = X^3 + X^2 - 1,\quad h = -X^4-2X^3 + 2X + 1
$$

Now, Alice computes the ciphertext to $$m=X^2-X+1$$ with corresponding $$\phi=X-1$$ as

$$
c\equiv 3\phi*h+m\equiv -3X^4 + 6X^3 + 7X^2 - 4X - 5\pmod{16}
$$

Bob receives $$c$$ and decrypts:

$$
a\equiv f*c\equiv 4X^4-2X^3-5X^2+6X-2\pmod{16}
$$

$$
F_p*a\equiv X^2-X+1\equiv m\pmod{3}
$$

so Bob has obtained the message as expected.

<br>

***

## Conclusion and Notes

***

This variation of NTRU is similar to the one presented in [Trappe and Washington](https://www.oreilly.com/library/view/introduction-to-cryptography/9780136758181/)

Informally, the *SVP* harness assumption tells us that we can construct lattices
such that it is "hard" to find the smallest vector on our lattice (think of these as having many
more dimensions than the two in the figure above). There may be another article more precisely
detailing the relation between lattices and NTRU in the future.

