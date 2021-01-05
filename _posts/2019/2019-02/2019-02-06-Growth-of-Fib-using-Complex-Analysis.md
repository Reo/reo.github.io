---
layout: post
title: "Growth of Fibonacci using Complex Analysis"
category: math
author: "Reo"
tags: complex_analysis
mathjax: true
---

We study the popular question about the the growth of the Fibonacci sequence
with an unorthodox approach using techniques from
complex analysis.

## Contents
{:.no_toc}

* Content
{:toc}

<br>

* * *

## Formula for Radius of Convergence

* * *

<br>
**Claim:** The Fibonacci sequence grows no faster than $$\left(\frac{\sqrt{5} + 1}{2}\right)^n$$
<br>
ie. if $$a_n$$ is the $$n$$th Fibonacci number, we want to show $$\limsup_{n\to\infty}a_n=\left(\frac{\sqrt{5} + 1}{2}\right)^n$$
<br>

*proof:*
<br>
Recall $$\limsup$$ appears in determining the radius of convergence for a complex-valued power series so
for instance, a series (centered at 0) with radius of convergence $$R$$ and coefficients $$a_n$$ satisfies

$$R=\left(\limsup_{n\to\infty}\sqrt[n]{a_n}\right)^{-1}$$

* * *

## Constructing a Related Function

* * *

We let these $$a_n$$ correspond to the Fibonacci sequence and consider the function defined by the power series
<div class="latex-align">
\[
  f(z) = \sum_{n=0}^{\infty} a_n z^n
\]
</div>

In order for this to be well defined, it must converge for some nontrivial radius.
Observe that the elements present in the sequence are bound by a similar sequence which
doubles at each step (this follows from the fact that for $$n>2$$, $$a_n = a_{n-1} + a_{n-2}$$ where
$$a_{n-2} < a_{n-1}$$). By comparison to a power series with coefficients $$b_n = 2^n$$ we see f(z)
is well defined (and holomorphic) in a neighbourhood about 0 with a radius of convergence of at least 1/2.
We now write $$f(z)$$ as follows:

<div class="latex-align">
$$
\begin{align*}
  f(z) &= \sum_{n=1}^{\infty} a_n z^n
  && a_0 = 0\\
  &= z + \sum_{n=1}^{\infty} a_{n+1} z^{n+1}&& a_1=1\\
  \iff f(z) - z &= \sum_{n=1}^{\infty}a_{n+1} z^{n+1}
\end{align*}
$$
and we will find these results to be useful
$$
\begin{align*}
  z f(z) &= \sum_{n=1}^{\infty} a_n z^{n+1} &&\text{simple multiplication by $z$}
\end{align*}
$$
$$
\begin{align*}
  z^2 f(z) &= \sum_{n=1}^{\infty} a_{n-1} z^{n+1} &&\text{multiplication by $z^2$ and shift index}
\end{align*}
$$
</div>

But by the definition of $$a_n$$ we have $$a_{n+1}=a_{n-1}+a_n$$ so we can write

<div class="latex-align">
$$
\begin{align*}
  f(z) - z &=\sum_{n=1}^{\infty}a_{n+1} z^{n+1}\\
  &= \sum_{n=1}^{\infty} (a_n + a_{n-1}) z^{n+1}\\
  &= \sum_{n=1}^{\infty} a_n z^{n+1} + \sum_{n=1}^{\infty} a_{n-1} z^{n+1}\\
  &= zf(z) + z^2f(z)
\end{align*}
$$
</div>
\\
Through simple manipulations to this recurrence, we may study an equivalent closed representation

$$
  f(z) - zf(z) - z^2f(z) = z \quad \iff \quad f(z) = \frac{z}{1-z-z^2}
$$

* * *

## Relating Back to Radius of Convergence

* * *

We can use the quadratic formula to see $$f(z)$$ is meromorphic with the its two poles at
$$z = (-1\pm\sqrt{5})/2$$, this takes us to the
conclusion that the power series for $$f(z)$$ has a radius of convergence
$$R = (-1 + \sqrt{5})/2$$. We now recall the formula for radius of convergence

<div class="latex-align">
$$\limsup_{n\to\infty} a_n = \left( \frac{\sqrt{5} - 1}{2} \right)^{-n} = \left( \frac{2}{\sqrt{5} - 1} \right)^n = \left( \frac{\sqrt{5} + 1}{2} \right)^n$$
</div>
as desired.

I would like to give credit to my Complex Analysis professor Giulio Tiozzo for these elegant solutions
to interesting puzzles.
