---
layout: post
title: "Lambda Expressions in MIT Scheme"
category: Programming
author: "Reo"
tags: LISP MIT-scheme functional programming
mathjax: true
---

We briefly go over the history, and use of lambda expressions which appear in
functional languages (and others which support this feature such as Java). We define
first-class functions and proceed to an example in MIT Scheme.

## Topics
{:.no_toc}

* Content
{:toc}

<br>

***

## Introduction

***

Functional programming has its origins in academia where Alonzo Church developed a model of computation
based on a simple rule --- variable substitution. These are essentially modern-day
procedures where one specifies in what manner a function manipulates its variables. Evaluation
is as simple as "pluging in" values given as input by invoking the procedure.

Notice that functions themselves may be given as input, this allows flexibility and modularity when writing programs
in this paradigm since small functions can be composed and manipulated to form more complicated constructs.

If you need a refresher on LISP syntax, you can check out [the first post]().

<br>

***

## Setup

***

We set up a few simple procedures to begin with:

```scheme
(define (square x)
  (* x x))

(define (double f)
  (lambda (x) (f (f x))))

(define (compose f g)
  (lambda (x) (f (g x))))

(define (repeated f n)
  (if (= n 1)
    (lambda (x) (f x))
    (repeated (compose f f) (- n 1))))
```

Here we see the `lambda` keyword a few times, let's consider its first appearance `lambda (x) (f (f x))`.
This expression simply returns a function which takes in one variable, `x` and itself returns `f (f x)`.

<br>

***

## Example

***

Consider
```scheme
((double square) 2)
```

you guessed it, this returns `(square (square (2)) = 16` which is the square function composed with itself applied to 2.
Lambda expressions are not too scary when you think of them this way, here is a slightly more involved example with
`repeated`:

```scheme
(display ((repeated square 3) 2))
```

This returns `2^16`! Notice that at each iteration, we're computing double of the original function. Applying this three
times to `square` our exponent goes from 2 to 4 to 16.

This is only a basic numerical example but when generalized to applying to lists of values, this becomes
quite powerful and is in fact used in the industry.
