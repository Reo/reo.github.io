---
layout: post
title: "Intro Cryptography: RSA"
category: Math
author: "Reo"
mathjax: true
---

As more and more of our lives become digital in one sense or another, questions about privacy and
security arise naturally. This post works as a prelude to a deeper study in cryptography through
the introduction of a brief history and a traditional example in the form of the *RSA* algorithm.

## Topics
{:.no_toc}

* Content
{:toc}

## Introduction

Modern cryptography is a relatively new field when compared to most other foci of studies in
mathematics. With the goal of sending secure messages over a network, early research was mostly
done in organizations which would not release their work such as the NSA in the united States, it
wasn't until about 1970 two of the largest public advancements were made. The first one being the
development of DES --- a new standard for enciphering messages developed at IBM with the purpose of
developing secure electronic communication between organizations which often handled sensitive data
such as financial institutions.

One of the largest shortcomings of cryptographic standards until this point is that in order to
transmit messages, much like in legacy enciphering techniques used in the second world war, the code
book to decipher them must first be passed along some secure channel. As expected, should this
secure channel be compromised or at any point the codebook become available to a third party, the
cipher can be broken quite easily and hence the initial secure communication would once again have
to be established in order to keep the messages secret.

The second one of these
advancements addressed just that. Often referred to as Diffie-Hellman key exchange, it paved the way
for asymmetric key encryption. Asymmetric key algorithms improved on their symmetric counterparts
described above by having both the sender and recipient keep a key secret at all times and one
agreed-upon key public. These keys are related (details on this relation depend on the implementation)
but the secret key should not be easily deducible from the public one. This allowed for the
creation of more efficient crypto systems including some which are widely used today such as AES.

## RSA Method

Rivest–Shamir–Adleman (RSA), named after the authors who described the algorithm in 1977,
is a form of public-key cryptography
which involves private-public key pairs. It relies on the difficulty of factoring a number which
is the product of two large primes, let's call them $$p, q$$ so that $$pq=n$$. Now, in order to
remain secure, these primes are often hundreds of digits long making their $$n$$ quite large.
The best way to illustrate this process is through an example, though these computations are
tailored for a computer so we will be using much smaller primes.

For this example, suppose we wish to send the message *HELLO* and use standard ASCII encoding
to do so. This ascii table is courtesy of Wikipedia.

![ASCII-table](https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/ASCII-Table.svg/1000px-ASCII-Table.svg.png){:class="svg invert-color"}

We create our public-private key pairs as follows:

choose two primes, $$p=23, q=31$$ (in this example $$n=713$$) we also need a number $$e$$ who is
relatively prime to $$\phi(n) = (p-1)(q-1) = 22\cdot 30$$ where $$\phi(n)$$ is understood to be the
Euler Phi function. Choose $$e=7$$.

The public key is then the numbers $$n$$ and $$e$$, while the numbers $$p$$ and $$q$$ are kept
secret as our private key.

|![message-passing-graphic](/assets/images/2019-02-13-KeyMessagePass.png){:class="svg invert-color"}|
|:--:|
| *high level overview of A sending a message to B* |

### Enciphering

We first encode the message, as a sequence of blocks who have fewer digits than $$n$$.
In our case, $$n$$ has 3 digits which means we may simply use the ASCII encodings which for our purposes
are at most two digits long. We obtain the following sequence as a result:

<div>
$$
    72 \quad 69 \quad 76 \quad 76 \quad 79
$$
</div>

At this stage, the message is in plaintext and can be decoded by anyone who intercepts it, so we label
each block at this stage $$p_i$$.
The ciphertext blocks $$c_i$$ can now be found by taking the $$p_i^e $$mod $$n$$. For our example
this yields

<div>
$$
    c_1 \equiv p_1^7 \equiv 72^7 \equiv 485 \: (\text{mod } 713)
$$
</div>

continuing in this fashion, we obtain the sequence which represents the ciphertext.

<div>
$$
    485 \quad 276 \quad 143 \quad 143 \quad 198
$$
</div>

### Deciphering

We begin by defining $$b$$ as the least common multiple between $$p-1$$ and $$q-1$$, and $$d$$ as
the least positive solution to

<div>
$$
    ex\equiv 1 \: (\text{mod} \: b)
$$
</div>

In our example, $$b=22\cdot 30/\text{gcd}(22, 30) = 660/2 = 330$$ so to find $$d$$ we solve

<div>
$$
    7x\equiv 1 \:(\text{mod} \: 330)
$$
</div>

We obtain $$d=x=283$$

All that remains now to unscramble the text is to evaluate $$c_i^d$$ mod $$n$$. The modular
exponentiation algorithm can be used here to evaluate the encodings for the plaintext. For
$$i=1$$ we have:

<div>$$
    485^{283} \equiv 72 \: \text{mod} \: 713
$$</div>

As expected, upon taking $$c_i^d$$ mod $$n$$ across the remaining $$i$$ we get back our plaintext
which can then be deciphered using
our agreed upon encoding. In our case, this is (ASCII) and we are done.

## Conclusion

One of the key takeaways here is that someone who does not know the values for
$$p$$ and $$q$$ would
have a hard time trying to figure out the value of $$b$$ and hence reversing the process to
find the plaintext.

As mentioned in the introduction, computers have only gotten faster and better at solving this
sort of factoring problem. The response to keep communications secure has been mostly to increase key size.
The problem is now becoming that key sizes are getting quite large and RSA itself is becoming
more inefficient as time goes on.
That said, there is hope. More sophisticated techniques which use smaller
keys have been proposed and are beginning to become popular one of which is so-called elliptic
curve cryptography.

Sources:

https://en.wikibooks.org/wiki/Cryptography/History

definitions and RSA example:
VandenEynden, Waveland press
