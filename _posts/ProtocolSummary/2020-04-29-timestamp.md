---
layout: post
title: 'Timestamp Protocols'
category: 'Cryptographic Protocols'
author: 'reo'
tags: Protocols Timestamp Blockchain
mathjax: true
---

Some of the previous Protocols we've discussed mentioned using a
timestamp in one way or another. It turns out having a reliable
way to attach a timestamp is quite a complicated feat in and of
itself.

## Contents
{:.no_toc}

* Content
{:toc}

<br>

* * *

## Goals

* * *

The aim of this article will be to explore options of timestamping
protocols where

- The data itself is timestamped, regardless of the medium (disk, tape, etc.)
- It should be obvious if any change is made to the timestamped data
- It should be obvious if any time different from the current one is used

<br>

* * *

## First Attempt

* * *

As usual, an approach where we can assume the existence of a trustworthy
party "Trent" is more straightforward. The protocol may go as follows:

1. Alice sends a copy of the document to be timestamped to Trent
2. Trent records the date and time he received the document and keeps a copy

if Bob wants to verify a timestamp, he simply asks trent to bring up the
relevent document.

Simple yet unrealistic.

To list just a few of the issues, this relies on trent having enough
storage and bandwidth, a secure database to store them, etc.

<br>

* * *

## Weakening the Assumptions

* * *

We can improve the first approach using a hash function and
digital signatures.

1. Alice sends Trent a hash of the document
2. Trent attaches the date and time to the hash he received and digitally signs it
3. Trent sends the signed hash with the timestamp back to Alice

Bob can verify the timestamp is legitimate by checking Trent's signature.

Trent now doesn't have to worry about needing an exorbitant amount of storage
and bandwidth.
He also isn't responsible for keeping the sensitive data on the
documents themselves.
Another neat side effect is that Alice can verify herself that she received
the expected timestamp and correct hash along with it taking necessary actions
if there were any mistakes along the way.

This works if Trent is completely reliable but unfortunately that's not always
realistic. Would it be possible to create a system which can defend even against
Alice and Trent cooperating to fake a timestamp?

<br>

* * *

## Linking Protocol

* * *

Here's an idea, what if Trent were to attach metadata to the timestamps linking
them to each other. In essence causing timestamps to "sandwich" between to others.

<br>

* * *

### Terms

* * *

We'll need to define a few terms to get started, let

- $$n$$ be the current (ordered) timestamp number Trent is issuing
- $$H_i$$ be the hash of the $$i$$th document
- $$t_i$$ be the timestamp given to the $$i$$th document
- $$I_i$$ be the identity of the author of the $$i$$th timestamped document
- $$L_i=(I_{i-1}, H_{i-1}, I_{i-1}, L_{i-1})$$ where $$H$$ is a hash function
- $$S_k$$ be Trent's signature using his private key

<br>

* * *

### The Protocol

* * *

1. Alice sends Trent $$(H_n, A)$$. Notice in particular $$I_n=A$$
2. Trent sends Alice $$T_n=S_k(n,A,H_n,t_n,I_{n-1},H_{n-1},t_{n-1}, L_n)$$
3. When Trent timestamps the next document, he sends Alice $$I_{n+1}$$

The verification process is a little more involved this time. If Bob wants
to verify the validity, she contacts $$I_{n-1}$$ and $$I_{n+1}$$ to see if
the information matches up. Should that not be enough to convince him,
Bob would go on to contact $$I_{n-2}$$ and $$I_{n+2}$$ and so on.

<br>

* * *

### Drawbacks

* * *

This protocol still uses a central authority in Trent and now requires
more parties to cooperate in an attempt to keep Trent honest. It may not
be entirely realistic to have this chain of cooperating participants
especially when there is no incentive.

<br>

* * *

## Recent Work

* * *

More recently, decentralized timestamping is using blockchain technology
for a system which has no centralized authority and does not require
explicit collaboration from other parties. There is an example of this
in [1] which secures video integrity using this method of timestamping.

<br>

* * *

## References

* * *

Applied Crypto 4.1

[1] https://www.gipp.com/wp-content/papercite-data/pdf/gipp2016a.pdf

