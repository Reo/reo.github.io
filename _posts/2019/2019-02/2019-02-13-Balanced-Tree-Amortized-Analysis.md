---
layout: post
title: "Balanced Tree Amortized Analysis"
tags: data structure, cost_analysis
category: Programming
author: "Reo"
mathjax: true
---

This is a simple exercise in amortized analysis which computer science
students often encounter early in their careers. I use the potential method described
in [CLRS](https://en.wikipedia.org/wiki/Introduction_to_Algorithms) to show the amortized cost of *INSERT* and *EXTRACT* in
an arbitrary (initially empty), balanced tree is $$\mathcal{O}(\log n)$$ and $$\mathcal{O}(1)$$
respectively.

As the title states, we are dealing with balanced trees, defined for our purposes
as being a tree which retains a height of $$\mathcal{O}(log n)$$ where $$n$$ is the number of keys. This
is important since we require the *INSERT* and *EXTRACT* operations to be $$\mathcal{O}(\log n)$$.
The first section is simply an introduction or refresher on
the technique itself taken from CLRS while we use a handy technique of considering a concrete
case and generalizing when determining the potential function in the next section.

## Contents
{:.no_toc}

* Content
{:toc}


* * *

## Potential Method

* * *

(This section is paraphrased from CLRS chapter 17.3)

The potential method is a technique used to find an amortized cost for each
operation. the total amortized cost across $$n$$ operations would then be the
sum of each of these amortized costs.

Defining $$\hat{c}_i$$ to be the amortized cost of the $$i$$th operation,
$$c_i$$ the true cost, $$D_i$$ the state of a data structure after $$i$$
operations, and *potential function* $$\Phi : D \to \mathbb{R}$$ where $$D$$ is
the set of all possible states for our data structure, say, after $$n$$
operations. We let

<div>
$$
\hat{c}_i = c_i + \Phi(D_i) - \Phi(D_{i-1})
$$
</div>

and notice that due to the telescoping sum. we may write the total amortized cost as

<div>
$$
\begin{align*}
  \sum_{i=1}^n \hat{c}_i &= \left(\sum_{i=1}^n c_i\right)
   + \Phi(D_n) - \Phi(D_{0})
\end{align*}
$$
</div>

All we require to guarantee the total amortized cost gives an upper bound to the
true cost is that the potential function be such that
$$\Phi(D_i)\ge\Phi(D_0)$$ for all $$i$$.

* * *

## Choice of Potential Function

* * *

Instead of an arbitrary balanced tree, it is convenient to begin
by considering a simpler example. Take a binary heap for instance which fills in a
predetermined fashion. In this case, we observe that there is a relationship
between the number of keys present amongst the subtrees and the total number
of keys in the whole heap. In particular we note that in a heap with $$n$$
keys where $$v$$ is a key in the heap and $$\tau(v)$$ is the number of keys
present in the subtree rooted at $$v$$, then the following relation holds:

<div>
$$
\sum_{v}\tau(v) = \sum_{k=0}^{n} \lceil\lg (k+1)\rceil
$$
</div>

We may then try taking the right hand side to be the potential function ie.

<div>
$$
\Phi(D_i) = \sum_{k=0}^{n} \lceil\lg (k+1)\rceil
$$
</div>

We notice that our tree can have no less than
0 keys, and in fact
$$\Phi(D_0) = 0 \le \Phi(D_i)$$ for all $$i$$ as desired. We proceed with the
analysis.

* * *

## Analysis

* * *

Recall that we required the tree be balanced so we can take the true costs
($$c_i$$) to be $$\mathcal{O}(\lg n)$$.

We first look at the result for *INSERT*

<div>
$$
\begin{align*}
  \Phi(D_i) - \Phi(D_{i-1}) &= \sum_{i=0}^n\lceil\lg(i+1)\rceil - \sum_{i=0}^{n-1}\lceil\lg(i+1)\rceil\\
  &= \lceil\lg(n+1)\rceil &&\text{cancellation of terms}
\end{align*}
$$
</div>
<div>
$$
\begin{align*}
  \hat{c}_i &= c_i + \left( \Phi(D_i) - \Phi(D_{i-1}) \right)\\
  &= \mathcal{O}(\lg n) + \lceil\lg(n+1)\rceil && \text{true cost is known and difference was evaluated above}\\
  &\in \mathcal{O}(\lg n)
\end{align*}
$$
</div>

We do similarly for *EXTRACT*:

<div>
\begin{align*}
  \Phi(D_i) - \Phi(D_{i-1}) &= \sum_{i=0}^{n-1}\lceil\lg(i+1)\rceil - \sum_{i=0}^{n}\lceil\lg(i+1)\rceil\\
  &= -\lceil\lg(n+1)\rceil
\end{align*}

\begin{align*}
  \hat{c}_i &= c_i + \left( \Phi(D_i) - \Phi(D_{i-1}) \right)\\
  &= \mathcal{O}(\lg n) - \lceil \lg n + 1 \rceil\\
  &\in \mathcal{O}(1)
\end{align*}
</div>

We arrive at the conclusion that for an initially empty balanced tree and sufficient operations, despite
having a true cost $$\mathcal{O}(\lg n)$$, *EXTRACT* is in a sense paid for by the
preceding *INSERT* operations and has a constant amortized cost.
