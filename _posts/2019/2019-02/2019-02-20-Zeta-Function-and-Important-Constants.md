---
layout: post
title: "Zeta Function and Important Constants"
category: math
author: "Reo"
tags: complex_analysis
mathjax: true
---

This post covers an interesting way to relate the famous Zeta function and constants $$i$$, $$\pi$$, and lesser-known
$$\gamma$$ being the Euler-Mascheroni Constant. In order that goal we discuss a convenient way to rewrite
$$\zeta(s)$$ as a sum with a holomorphic function.

## Contents
{:.no_toc}

* Content
{:toc}

<br>

The Zeta function mainly gets its fame from Number Theory but it is also interesting to study in the
context of complex analysis.

Our goal here will be to evaluate the integral over a ball centered at 1. For a complex variable $$z$$
we denote the real part of $$z$$ as $$\Re(z)$$.

* * *

## Rewriting $$\zeta(s)$$

* * *

Since we will be computing a contour integral, it would be convenient to be
able to write $$\zeta(s)$$ as a sum involving a holomorphic function. To that end, we present
the following Lemma and Proposition. For convenience, we let $$\sigma=\Re(s)$$.

**Lemma:** $$\vert n^{-s}\vert = n^{-\sigma}$$

_proof_:

$$
\vert n^{-s}\vert = \vert e^{-s\ln(n)} \vert = e^{-\sigma\ln(n)} = n^{-\sigma}
$$

**Proposition:** If $$\Re(s) > 0$$ then

$$
\zeta(s) = \frac{1}{s-1} + H(s)
$$

where $$H(s)$$ is holomorphic in $$\Re(s)>0$$.

The proof presented here is a detailed version of the one in Stein and Shakarchi's Complex Analysis textbook:

_proof_: Let $$f(x) = x^{-s}$$ and set

$$
\delta_n(s) = \int_n^{n+1} f(n) - f(x)\:dx
$$

consider $$x\in[n,n+1]$$ real and $$n\ge 1$$ an integer. When $$x=n$$ we have

$$
\vert n^{-s} - x^{-s} \vert = \vert n^{-s} - n^{-s} \vert = 0 \le\frac{\vert s \vert}{n^{\sigma+1}}
$$

since $$\Re(s)>0$$ so the rightmost value is in fact strictly positive. Next, let $$x\in(n,n+1]$$ be arbitrary,
by mean value theorem we have that there exists some $$c\in (n,x)$$ such that

$$
f'(c) = \frac{f(x) - f(n)}{x - n}
$$

taking magnitute and noticing that $$1 \le (x-n)^{-1}$$ for every choice of $$x\in(n,n+1]$$ we have

$$
\vert f(x) - f(n) \vert = \vert f(n) - f(x) \vert \le \vert f'(c) \vert = \vert -sc^{-s-1}\vert \le \vert s\vert\vert n^{-s}\vert\vert n^{-1} \vert
$$

We may now directly apply our lemma and we get

$$
\vert \delta_n(s) \vert = \vert f(n) - f(x) \vert \le \frac{\vert s\vert}{n^{\sigma + 1}}
$$

Now consider

$$H(s) = \sum_{n=1}^{\infty}\delta_n(s) = \sum_{n=1}^{\infty}n^{-s} - \int_1^\infty x^{-s}\:dx = \sum_{n=1}^{\infty}n^{-s} - \frac{1}{s-1}$$

$$\Re(s)>0$$ implies $$\sigma + 1 > 1$$ so by
comparison test and the bound we found for $$\vert \delta_n(s)\vert$$ we have that $$H(s)$$ converges uniformly
on $$\Re(s)>0$$ and is well defined.

Recall that $$\zeta(s) = \sum_{n=1}^{\infty}n^{-s}$$ for $$\Re(s) > 1$$ so we have $$H(s) = \zeta(s) + (s-1)^{-1}$$ on this
region but since $$\sum_n\delta_n(s)$$ is holomorphic on $$\Re(s) > 0$$ it follows that $$\zeta(s)$$ is extensible to that
region as well and the identity continues to hold so we have

$$
\zeta(s) = H(s) + \frac{1}{s-1}
$$

for $$\Re(s) > 0$$ where $$H(s)$$ is holomorphic everywhere as desired.

* * *

## Evaluating the Curve Integral

* * *

Now for the computation mentioned in the title,
let $$S_{\epsilon}(1)$$ denote a ball of radius $$\epsilon$$ centered at $$1$$ with, say, $$\epsilon=1/2$$.

<div class="latex-align">
$$
\begin{align*}
  \oint_{S_{\epsilon}(1)} \zeta^2(s)\: ds &= \oint_{S_{\epsilon}(1)} \left( \frac{1}{s-1} + H(s) \right)^2\: ds\\
  &= \oint_{S_{\epsilon}(1)} (s-1)^{-2} + 2H(s)(s-1)^{-1} + H(s)^2 \: ds\\
  &= \oint_{S_{\epsilon}(1)} \frac{2H(s)}{s-1}\: ds &&\text{Cauchy's Theorem, Residue Theorem}\\
  &= 4 \pi i \text{Res}_{s=1}\left(\frac{H(s)}{s-1}\right) && \text{Cauchy's Integral formula}\\
  &= 4 \pi i \lim_{s \to 1}H(s) &&\text{computing the residue}\\
\end{align*}
$$
</div>

* * *

## Reduced to a Limit Problem

* * *

We now turn our attention to evaluating $$\lim_{s \to 1}H(s)$$ but first we recall $$\int_1^\infty x^{-s}dx=1/(s-1)$$:
<div class="latex-align">
$$
\begin{align*}
  \lim_{s \to 1}H(s) &= \lim_{s \to 1}\left(\zeta(s) - \frac{1}{s-1}\right) && \text{definition of } H(s)\\
  &= \lim_{s\to 1}\left( \left( \sum_{n=1}^\infty \frac{1}{n^s} \right) - \int_1^{\infty}\frac{dx}{x^s} \right)\\
  &= \sum_{n=1}^\infty\left( \frac{1}{n} - \int_n^{n+1}\frac{dx}{x} \right) &&\text{evaluate at $s=1$}\\
  &= \sum_{n=1}^{\infty}\left( \frac{1}{n} - (\ln(n+1) - \ln(n)) \right) &&\text{Fundamental Theorem of Calculus}\\
  &= \lim_{N\to\infty}\sum_{n=1}^{N}\left( \frac{1}{n} - (\ln(n+1) - \ln(n)) \right)\\
  &= \lim_{N\to\infty}\sum_{n=1}^{N}\left( \frac{1}{n}\right) - \ln(N)&&\text{telescoping sum, $\ln(1)=0$}\\
  &= \gamma &&\text{definition of the Euler-Mascheroni Constant}
\end{align*}
$$
</div>
Hence, we arrive at the final answer for the original question: $$\int_{S_{\epsilon}(1)} \zeta^2(s)\: ds = 4\pi i\gamma$$.

I would like to give credit to my Complex Analysis professor Giulio Tiozzo for these elegant solutions
to interesting puzzles.
