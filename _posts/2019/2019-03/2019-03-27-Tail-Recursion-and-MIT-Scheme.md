---
layout: post
title: "Tail Recursion and MIT Scheme"
category: Programming
author: "Reo"
tags: LISP MIT-scheme functional programming
---

This post will serve to introduce the reader to basic syntax of MIT scheme and explain
precisely what is meant by tail recursion. This will serve as preparation to the
more famous topic in functional programming being lambda expressions.

We discuss a few key points culminating in
an example written in MIT Scheme. These are applicable not only in strictly functional
languages but also multi-paradigm languages with functional capabilities such as Java.

## Topics
{:.no_toc}

* Content
{:toc}

<br>

* * *

## Overview

* * *

In order to introduce more focused topics in functional programming, it's convenient to first
mention the fundamentals. In our case, we will be working in MIT Scheme, a type of [LISP](https://en.wikipedia.org/wiki/Lisp_(programming_language)).
This choice is made both because it continues to be developed but also since
the presentation of concepts here will borrow closely from the seminal text [SICP](Structure and Interpretation of Computer Programs).

Before diving into the syntax, recall that **Polish Notation** simply means that operators precede their
operands so $$x+y$$ becomes $$+ x y$$. Notice that this removes ambiguity for more complex expressions
and can more easily be parsed into a tree for computer evaluation.


* * *

## Syntax

* * *

As when learning any new language, we briefly go over the syntax the interpreter/compiler expects.
In our dialect of LISP, we may write functions as follows, noting that
operations are written in Polish notation:

```scheme
(define x 3) ; x = 3
(define y 9) ; y = 9
(define (z w) (+ (+ x y) w))  ;z = ((x + y) + w)
(display x)
(display y)
(display (z 2))
```

This will display the numbers `3`, `9`, and `14`. An important distinction to be made here
from traditional programming languages is that `x` and `y` are functions just like `z`
they just happen to return a constant value. This is in contrast to them being "variables"
which store a value such as an integer. Note also how the argument passed to z needs no additional parentheses.

We can now begin our discussion of tail recursion in this syntax

* * *

## Tail Recursion

* * *

Tail Recursion is simply when the implementation of a procedure is recursive however when
evaluated, only one call frame needs to be kept track of at any point in the evaluation.
This is best illustrated with an example:

```scheme
(define (sumrec x)
  ( if (= x 1)
  x
  (+ x (sumrec (- x 1)))
  ))

(display sumrec 3)
```

notice that the computations here are

```
(sumrec 3)
( + 3 (sumrec 2))
( + 3 ( + 2 (sumrec 1)))
(+ 3 ( + 2 ( + 1)))
```

so all previous states must be kept while in the next recursive imlementation

```scheme
(define (sumtailrec x r)
  ( if (= x 0)
  r
  (sumtailrec (- x 1) (+ x r))
  ))
(display sumtailrec 3 0)
```

the computations are

```
(sumtailrec 3 0)
(sumtailrec 2 3)
(sumtailrec 1 5)
(sumtailrec 0 6)
```

So we don't need the entire call stack but only the most recent one since in a sense the auxiliary
variable `r` is keeping track of the information we needed. This is effectively an iterative
process which has been implemented using recursive procedure.

Modern compilers for languages such as C now support this sort of optimization but future discussions
will include features which functional programming languages are known for such as the aforementioned
lambda expressions.

