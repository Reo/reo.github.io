---
layout: post
title: 'Secret Splitting and Sharing'
category: 'Cryptographic Protocols'
author: 'reo'
tags: Protocols 'Secret Sharing'
mathjax: true
---

Some secrets are so powerful, they should only be
revealed when multiple parties agree to open it up.
Think missle launches in the movies where multiple
members must simultaneously turn a key. The digital
equivalent of this is Secret Splitting (or more
generally Secret Sharing).

## Contents
{:.no_toc}

* Content
{:toc}

<br>

* * *

## Secret Splitting

* * *

Starting simple, suppose we have a secret $$S$$ to be split
up among five
members and we want all of them to be present in order to
decipher the message.

This is relatively straight-forward. Simply generate four
random bitstrings $$B_1, B_2, B_3, B_4$$ the same length
as $$S$$ and compute

$$B_5 = S\oplus B_1 \oplus B_2 \oplus B_3 \oplus B_4$$

now, the first member get $$B_1$$, the second $$B_2$$, and
so on. All five together can reconstruct $$S$$ but any fewer
will get gibberish.

(In fact, notice the similarity to One-time pad).

<br>

* * *

## Weakening the Assumptions

* * *

In reality, secret splitting is not particularly useful
because it requires cooperation of everyone involved.
A more generalized version called secret sharing has been
widely studied and has many variations.

The basic idea behind secret sharing is that instead of
needing all $$n$$ participants, we only require particular
subsets of them in order to decipher the message.

<br>

* * *

## Blakley's Secret Sharing

* * *

The first approach to secret sharing we study has a nice
geometric interpretation. Suppose we have a team with
$$n$$ members and want any subset with
at least $$k$$ members to be able to decipher the secret.

This can be done by encoding the data as a point in
$$\mathbb{R}^k$$, choosing $$n$$ distinct $$k-1$$-dimensional
hyperplanes which intersect the point, and distributing
them to the $$n$$ members.

When the team members would like to reconstruct the secret,
$$k$$ of them would find the point in common from their
hyperplanes. This point is unique and is exactly the secret
by construction.

Consider this example with $$k=3$$, notice that with only
one or two planes, it's impossible to deduce the original point
but the point is entirely determined once the third plane is
introduced.

<br>

* * *

## Weaknesses and Variations on Secret Sharing

* * *

in general, "fragments" which are used
to reconstruct the secret
(the hyperplanes in the above example)
are often referred to as "shares".

Notice that in the above algorithm there is no way to veriify
whether somebody is using a valid share. This can lead to
problems.

Since there is no verification of shares, a malicious actor
(Mallory)
can pretend to have a share, participate in the protocol
rebuiling the secret, and escape with more knowledge. In
the worst-case scenario, Mallory is a superfluous member and
the secret is reconstructed with nobody realizing Mallory didn't
have a valid share since the reconstruction was successful.

There are variations on secret sharing which target various
problems which may present themselves.

<br>

* * *

### Secret Sharing without Central Authority

* * *

Going back to our movie example with missile launches, suppose
that the secret is actually a launch code and hence you can't
risk one person knowing the secret even if it is just to later
distribute it.

There is an example of this is presented in the references [1]
with the high-level idea being that participants first set up
a scheme where:

- They each contribute equally to determination of the secret
- All of the individual contributions must be presented for
the secret to be reconstructed

Afterwards, those who participated in step one can split their
share traditionally, perhaps using Blakley's so other subsets
can recreate the secret.

<br>

* * *

### Secret Sharing with Compromised Shares

* * *

If a share is ever lost or stolen, it would be convenient if
there were a way to modify the encrypted secret so that the
compromised share is no longer valuable without having to
perform the whole process from scratch. There is a protocol
to acheive precisely this which uses a trusted party Trent.

It is presented in detail in the references [2] but the idea
is as follows:

1. Trent finds out a share has been compromised
2. Trent generates a random number $$R$$ and distributes modification $$M_R$$ to the participants keeping $$R$$ secret
3. The participants compute their new shares using $$M_R$$
4. Trent modifies the expression used to combine the shares taking $$R$$ into account

<br>

* * *

## Applications

* * *

Secret sharing can have some applications in password recovery,
medical agrements (eg. need at least $$k$$ of a certain specialist),
and more. There are many variations not included in this article.

<br>

* * *

## References

* * *

Applied Cryptography 3.6-3.7

[1] Ingemarsson, I., & Simmons, G. J. (1990, May). A protocol to set up shared secret schemes without the assistance of a mutually trusted party. In Workshop on the Theory and Application of of Cryptographic Techniques (pp. 266-282). Springer, Berlin, Heidelberg.
[2] Charnes, Chris & Pieprzyk, Josef & Safavi-Naini, Reihaneh. (1994). Conditionally Secure Secret Sharing Schemes with Disenrollment Capability… 89-95. 10.1145/191177.191196.

slides references

