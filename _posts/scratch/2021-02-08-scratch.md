---
layout: post
title: "The Math behind What Could have Been Heartbleed's Successor"
category: Crypto
author: 'reo'
tags: scratch
mathjax: true
---

## Intro

* * *

<br>

**possibly have an animation running in the background, some music**

**heartbleed logo**

You may have heard the term "Heartbleed" and how it made the internet less secure.
Heartbleed was a bug in a popular implementation of TLS which compromised communications
between devices allowing theft of sensitive information; possibly even the server's private keys.

**heartbleed 2 mockup**

In this video we go over the mathematical background of a vulnerability which was present
in a number of popular TLS implementations which also allowed theft of a server's private key.

Thankfully this was patched relatively quickly once the library authors were notified
which meant it was stopped before it could have as big of an impact as heartbleed.

Our conversation of this attack borrows notions from group theory, and the
theory of Elliptic Curves as well as algorithm and protocol design.

**snowflake, curve, communication boxes**

I will cover the required math so with the exception of the
Chinese Remainder Theorem, a famous result in number theory, you shouldn't
need a particularly strong mathematical background to follow along.

<br>

* * *

## Overview

* $$s_A\times P_B$o* *

<br>

**title card**

Asymmetric encryption is used on the modern internet to secure everything from personal chats
to corporate communications.

One of the most popular
protocols for securing communications, used everywhere from WhatsApp and LINE to
EAP is Elliptic Curve Diffie Hellman (ECDH).

**phones communicating**

In order to visualize and understand the attack, we first need some basic group theory.

**small window with relevant visualization**

**takeaways**
1. (*)cyclic groups
2. order of subgroup divides order of group
3. $$k$$ times a point is the point added to itself

Next, we start our conversation on Elliptic Curves.

**small window with relevant visualization**

**takeaways**
1. (*)$$\pm y$$ for any given point $$(x,y)$$
2. "point at infinity"
3. (*)Definition of addition of points on elliptic curves
4. (*)$$b$$ is not used when computing point addition
5. Elliptic curves over finite fields
6. Points on an elliptic curve are a group under "addition" so can be used for DH Key Agreement

Following that, we take a sidestep to talk about the protocols.

We'll go over ECDH and introduce a simplified version of TLS to understand how
we can abuse it to leak information about the secret key.

**small window with relevant visualization**

**takeaway**
9. ECDH
1. 4-step exchange

With these tools, we'll be ready to go through an example of the attack.

**small window with relevant visualization**

**small pause**

<br>

## Group Theory

* * *

**title card**

Let's start by reviewing some basic group theory:

**snowflake**

Consider the rotational symmetries of this snowflake on a plane.

Notice that rotations of 60 degrees give us a symmetric shape with the only difference
being labeling of the vertices.

**rotate 60 deg at a time**

If we define our personalized "addition" to be taking the sum of the angles of rotation, we can say something like

* * *
"rotation by 60 degrees + rotation by 120 degrees = rotation by 180 degrees".
* * *
**snowflake rotating by 60 degrees, a second rotating by 180, and a third by 60 then 120. Highlight 180 total** (frame 180)

Notice that this is again a symmetry.

**third rotation drops in place (frame 320)**

This motivates a definition.

**frame 400**

For our purposes: a group is a set or collection of elements

**collection of elements with curly braces fram 450**

along with an operation "+"

**plus sign**

such that:

the sum of any two elements from our set, is again in the same set.

and

there is a member in the set which doesn't change the value of whatever it's added to.
In a sense, it behaves like the number 0.

If we populate our set with the rotational symmetries

**populate with with rotational symmetries**

And use the + we defined earlier.

**define + to be sum of angles**

We notice that sums of these symmetries always gives back a symmetry and the 0 degree rotation
acts as our "0 element" or identity.

**show examples of sums of rotations**

It's also convenient to define 
multiplying an element by a positive integer $$k$$ as adding
that element to itself $$k$$ times.

**show k(60 deg rotation) for k = 1, 2, 3**

Notice that creating a collection of the rotations which result from adding 60 degrees to itself $$k$$ times

**start with set populated with just 60 deg rotation then add to itself to generate group**

creates the whole group.

We call this a "cyclic group" since repeated additions of one elements cycles
though every element in the group. An element with this property is called
a generator.

**visualization is timed to end about here**

**probably next section**


Two:

**create two sets, the 0 180 and 0 120 240 sets**

For certain subsets of our rotations we have another nice property. If those subsets are also groups under the
same addition, we call those "subgroups".

For instance, consider the subset of only 0 and 180 degree rotations. That is still a group under the addition we defined.

**show example addition**

Same thing if we take the 0, 120, 240 rotations.

**show example addition**

Three:

Looking at the number of elements in our subgroups

**numbers 2 and 3 appear above newly created sets**

(2 and 3 respectively)

each we notice they divide the number of elements in the whole group

**6 appears above whole set**

(6).

This is no coincidence, the number of elements (or "order") of the subgroups must divide the
order of its parent group.

**takeaways title card**

> Key takeaways of this section:

1. Intuitive idea of what a group is **snowflake rotation with + sign**
2. "cyclic" groups and "subgroups" **rotations being added to a set**
3. The order of a subgroup divides the order of a group (for finite groups)

<br>

* * *

## DH Key Agreement (This is being scrapped for later)

* * *

A crucial tool in modern cryptography is so-called Key Agreement protocols which allow two parties to agree on
a secret key which they can both use to encrypt future messages through an insecure channel.

If this wren't the case, we would have a big issue where two parties who want to communicate securely
would first need to agree on a secret key.
But in order to keep the key a secret, it would need to be sent through a secure channel which doesn't exist
since they haven't yet agreed on a key to use.

the Diffie Hellman protocol solves this problem using cyclic groups.

The secret keys are a number smaller than the order of the cyclic group.

The public key is the result of adding the generator to itself the secret number of times.

The agreed upon key is then the secret number times the recipient's public key.

> Key takeaways:

1. Diffie-Hellman key generation
2. Diffie-Hellman Key Exchange



<br>

* * *

## Elliptic Curves

* * *

**section title card**

We will study a special family of Elliptic Curves.
For our purposes, "Elliptic curves" are the curves which result from the points which satisfy the equation

**equation appears**

$$
y^2 = x^3 + ax + b
$$

and are nonsingular.

Notice that since we have $$y^2$$

**draw x and y axes**

if the point $$(x,y)$$ is on the curve,

**draw (x,y) in space**

then so is the point $$(x,-y)$$.

**draw (x,-y)**

This can be seen when drawing the curve over the real numbers

**animate drawing a generic curve with (x,y) and (x,-y) on it**

the only case where this does not yield a distinct point is at $$y=0$$ since $$y = -y$$ in this case.

**highlight point**

* * *
**pause**

To study how these are used in cryptography, we turn to group theory.

Define our set to contain every point on this curve, plus, a special point often referred to as the point at
infinity.

This special point serves as the "0 element" of our group.

**fill curly braces with points presented earlier and ellipses . . .**

Notice since there are infinitely many points,
we can't actually write all of them.

**frame 770** Next, define addition between points $$P$$ and $$Q$$

*ALT* frame **770**: To define addition, it is productive to look at the algorithm the target
uses to add elements in the group.
**frame 1040**

**take two points from the set and place them where they belong on curve**

to be the third intersection point

**third intersection point**

reflected across the $$x$$ axis

**reflect across x axis**

of if we're adding a point to itself,

**clean up previous lines etc. leaving only one point**

we take the tangent at that point

**draw tangent**

and compute the reflection of the second intersection point.

**draw second intersection and its reflection**

There is one special point often reffered to as "the point at infinity".

**draw a point above the plane where the top of sphere will be with a special colour**

This is a concept borrowed from projective spaces

**sphere appears and curve is projected onto it demoing orthographic projection**

but for our purposes, we take the existence of such a point for granted.

This point serves as the identity and adding it to the set of points,

**add special point to set**

our set with "addition" is now a bona fide group which has the nice properties we covered earlier.

* * *
### Algorithm
* * *

**section title card**

For our attack, it is important to understand the algorithm used to add points on an elliptic curve:

**typing on computer animation split screen with a visualization of what's happening on the curve**

`def add(P, Q):`

`if` P or Q is the point at infinity,

**plug in the point at infinity "point" sphere into one of the function parameters**

simply return the other point, since it's our "0" element.

**frame 1215**

**return the other point**

* * *

if neither is the point at infinity, then both points lie on the curve.

for convenience we let P = (xpyp), Q = (xqyq) and their sum R = (xr, yr).

**frame 1455**

`else` P, Q\ne infinity so we let $$P = (x_p, y_p), Q = (x_q, y_q), R = (x_r, y_r)$$ and compute $$P + Q = R$$

**the algebra stuff is on screen/typing section**

We first find is the slope of the line which intersects both points. There are two cases to consider.

**these ifs are nested, so, indented**

`if` $$P\ne Q$$

**show two distinct points on the curve visual**

we can use the "rise over run" formula from high school

**show rise and run lines on curve visual and type the following on terminal section**

$$m = \frac{y_q - y_p}{x_q - x_p}$$

**frame 1720 - 1760**

`else` we're adding $$P$$ to itself (computing $$P + P$$ aka $$2P$$)

**show two previous points getting closer and line changing accordingly on the curve visual**

If instead, P==Q we're adding the point to itself so
we have the limiting case where we take the line tangent to the curve at the point.

**line becomes tangent at this point**

**frame 1940**

The slope can be found by taking the ratio of partial derivatives on each side.

**frame 2000**

**type this out on terminal side of window**

$$m = (3x_p^2 + a)/(2y_p)$$

Something important to note is that we use the $$a$$ term from the equation of the curve here.
Pushing on,

we compute the constant term of our line which we may use to find the x and y coordinates of the resulting point.

**frame 2270**

Geometrically, the resulting point is the distinct point our line intersects, reflected across the x axis.

Clearly, this is always again a point on the curve (or the point at infinity) so we have a group.

Notice though, that we never used the b term when computing the sum. This is extremely important to our attack.

**frame 2600**

**next section**

**highlight a term in "code"**

We now have the slope.

**keep one of the lines on curve visual**

Using the equation of a line:

$$y = mx + c$$

**write next to line on curve visual**

We can solve for $$c$$ with the information we have

$$c = y_p - mx_p$$

**type on console visual**

Plugging this back into our curve equation we have

$$
(mx + (y_p - mx_p))^2 = x^3 + ax + b
$$

**comment on console visual**

which after simplifying results in a cubic with three roots which are exactly
the three points where the line intersects the curve.

**light those points up**

$$
0 = x^3 - m^2x^2 + (a - bm)x + b - r^2
$$

**comment on console visual**

We have thus reduced the problem of finding $$x_r$$

**light x_r** up on the curve

to finding the root of this cubic different from $$x_p$$ and $$x_q$$

**light up the two other points of intersection**

A simple exercise in expanding the root-form of the cubic with roots $$x_p, x_q, x_r$$

$$K x^3 + L x^2 + Mx + N = (x - x_p)(x-x_q)(x-x_r)$$

**comment on console visual**

shows us that $$-L = x_p + x_q + x_r$$.

**comment on console visual**

This can be proved easily by simply expanding the brackets out.

**pause**

the result tells us

$$x_p + x_q + x_r = m^2$$

**comment on console visual**

solving for $$x_r$$ we have

$$x_r = m^2 - x_p - x_q$$

**comment on console visual and highlight x we found on curve visual**

Finally, we plug in $$x_r$$ to the equation of the line to find the corresponding $$y$$.
Note that we multiply by $$-1$$ since we are reflecting across the $$x$$ axis:

$$
y_r = -(mx_r + (y_p - mx_p)) = m(x_p - x_r) - y_p
$$

**comment on console visual and highlight sum point on curve visual**

Notice that at no point did we need the $$b$$ term of the curve for these computations.

**show curve equation with b term in red**

Ignoring the $$b$$ term makes the algorithm more efficient so popular algorithms opt
to compute $$P+Q$$ with this method. We will abuse this in our attack.

* * *

**key takeaways title card**

Key takeaways of this section:
1. $$\pm y$$ is on the curve for any given point $$(x,y)$$
2. Geometric intuition of addition of points on elliptic curves
3. "point at infinity"
4. Points on an elliptic curve are a group under "addition"
5. $$b$$ is not used when computing point addition

<br>

* * *

## EC over Finite Fields

* * *

**new section title card**

**2600**

In practice, we would rather work with finite collections and integers instead of
real numbers so let's consider the set of points where x and y are integers.

**frame 2765**

It turns out the intuitions we covered earlier (including the addition algorithm)
still work if we restict ourselves to just the integers modulo a prime p > 3.

**2950**

though it doesn't look much like a curve anymore we can still consider the points which
satisfy the congruence

(congruence)

**frame 3100**

*new*
In fact, for certain choices of a and b, the points form a cyclic group.
*new*

**add 50 to each keyframe after this**

using the geometric interpretation of our point addition, we find the sum of two points by

**frame 3170**

drawing a line between the two points, finding the third point on the curve it intersects,
and flipping that across the x axis.

**frame 3310**

Since we're dealing mod p, notice
we arrive at the same point
if the line "loops around"
the p by p region in purple.

**frame 3450**

We can illustrate this looping with a bit of topology:

**frame 3520**

We first, stretch our region, then glue the ends which loop into each other together

**frame 3640**

In this sense, elliptic curves over mod p can be thought of as points on a torus.

**frame 3730**

**next scene**


and since we're taking the modulus, lines between points wrap around nicely.

 over finite fields, in particular,
we consider $$\mathbb{Z}_p$$ for prime $$p$$.

If you're not familiar with fields, you can just
think of them as having the same operations you're familiar with over the reals (addition, multiplication,
roots) except all are dealt with mod $$p$$ so we're dealing with congruences and only have
numbers $$0$$ to $$p-1$$.

We now consider the points in Z_p^2 which satisfy our equation

**write equation again**

Since they are just integers, elliptic curves now look like a set of discrete points on the plane representing two real numbers.

**show discrete points on the plane**

In fact, since we're dealing mod $$p$$, notice that the lines we used last time can be thought of
as "looping around" so we only need to consider the first period or fundamental region.

**show line ghosting looping around**

In order to more naturally think about this looping, we can see that lines on this region behave
as if they were on a torus seen by folding up the region as follows:

**show animation of region being folded up into a torus**

now the lines naturally transition from one end to another.

Here is an example of point addition over Zp:

**show point addition on torus**

With an appropriate choice of point and curve, this group can in fact be cyclic.
ie. adding a point to itself enough times will generate the entire group.

**show small example of a cyclic group on this**

Tori such as this one will be used to illustrate elliptic curves over finite fields and
the operations on them.

we can now talk about the protocol which we will be attacking

* * *
## LEGACY
* * *

Elliptic Curves are such a large topic that they can have a presentation all on their own but for our purposes we will
cover only enough to understand our attack.

For simplicity, suppose we have a non-singular (no "cusps" or "self-intersections") Weierstrass-form curve, so

$$
y^2 = x^3 + ax + b
$$

It turns out the points on these curves define a group! Addition of two (different) points P1, P2 is done as follows:

1. take the line between P1 and P2 (finding delta y / delta x)
2. find the third point, R where this line intersects the curve
3. reflect R across the x axis, this reflected point is P1 + P2

doubling a point (adding a point to itself) is done similarly where instead of finding the slope between
two distinct points, we take the tangent at the point we're doubling. Notice this requires finding
dx/dy and hence involves the $$a$$ term of the weierstrass equation but not b. In fact neither of these depend on b.
this is important and will also come back later

real curves are nice to see the shape but for security (and to make computation more reliable on computers) we often work
in a discrete setting. It turns out if instead of the reals, we use a finite field eg. the integers mod a prime p, the
points which solve the equation still form a group.

Recall that Zp is just the set of integers mod p so addition, multiplication, etc. are also taken to be mod p and
the equation becomes a congruence mod p.

We only have a finite, discrete set of points and instead of the whole of R^2, the only points to consider are the ones
on Zp^2 (plus the point at infinity)

Something interesting about Zp is that instead of considering the whole plane, we can focus just on the fundamental region
and continue lines as if they had "looped back around". With this, our geometric intuition still holds some merit as demonstrated
here:

(a = 4, b = 0, r = 7 add (0,0) with (3,5) looping around ending up at (6,3) then reflect to end up at (6,-3) = (6,4))

folding up the sides which loop into each other we see zp^2 can be represented as a torus so we'll do that from there on out

* * *
## LEGACY
* * *

<br>

## The Protocol

* * *

* * *
### ECDH
* * *

**new section title card**

We've reached the point where we just need to model the protocol and we can begin our attack.
We first need a basic understanding of ECDH. Thankfully, with what we've learned this is relatively straight-forward.

**frame 300**

**set up alice and bob**

Suppose A and B wanna agree on a secret number but their messages can be seen by anyone.
ECDH is one of the most efficient ways to accomplish this.

**frame 520**

**visual this scenario**

To set up, Alice and Bob agree on a curve mod p with n points, and a generator for the group.
We'll refer to the generator point as G.

**frame 730**

**torus representing shared curve and special point representing base point**

They each choose a secret key from 1 to $$n-1$$

**each side chooses their secret number**

and multiply the base point by the secret key.

**frame 890**

These new points are known as Alice and Bob's public keys.

**frame 980**

**show Alice and Bob's public points**

To arrive at a secret number, Alice and Bob first exchange their public keys.

**frame 1080**

**show their points being transferred over the wire**

Then multiply their secret keys by the received public key.

**1180**

**show independent secret computation which happens here**

Since the product of the secret keys commute, Alice and Bob have extablished a shared point on the curve.

**show this equality**

**1300**

The secret number can be chosen as the x coordinate of the common point.

**highlight the point the both arrived at and x coord ring**

**1380**

In practice, the number of points on these curves is about 68 decimal digits long.
This makes strategies like guessing the secret infeasible.

* * *
### TLS
* * *

**1580**

**new section title card**

Finally, we consider a simplified version of TLS 1.2
which is still widely used at the time of this video's release.

In this scenario, Bob can be thought of as a server which hosts, perhaps, a banking website
while Alice is simply someone trying to securely access the website.

**set up protocol view**

1. The client sends their public point to the server
2. The server computes the shared secret and sends their public point to the client
3. The client sends an HMAC of the shared secret to confirm everything went well **hmac is maybe just rep as jumbled alphanumerics**
4. The server returns success/failure depending on whether the same key was agreed on

You can think of the HMAC as being a "one-way" function so it can only be used to check
if Alice and Bob agreed on the same number but you can't go the other way around
(find the secret number given its HMAC output).

**~2800**

<br>

## The Attack

* * *

**new section title card**

We finally have all the tools we need to perform the attack.

Our observation that the point addition algorithm doesn't involve the constant term motivates a definition:
We say the curve E* is an "invalid curve with respect to E" if E and E* differ only in their constant term.

**~3270**

**visual this**

We can now set up our attack. Suppose the public shared curve has a = 10 and b = 5

$$y^2\equiv x^3 + 10x + 5\pmod{31}$$

**represent this as a torus**

with 42 points. This information is always made public in real implementations.

**points finish drawing about now**
**show n=42 somewhere**

**~3420**

The number we want to crack is Bob's secret which for this example we'll say is 22

**s_B=22**

**write this somewhere**

**~3540**

There are a few pre-computations we can do before even having to establish a connection with Bob:

**~3670**

**section out spot for the precomps**

1. we first pick primes such that their product is larger than $$n^2 = 1764$$
say 2, 3, 5, 7, and 11

**~3850**

**store these primes somewhere**

2. Next, we find invalid curves and points on those invalid curves such that
the points have the same order as the chosen primes

**~4010**

**pull result from a toolbox or something**

*optional*
Since we know the order of the elements divide the order of the group,
we use curves with orders which are multiples of our primes.
*optional*

Some relatively efficient computations allow us to find the following curves and points on them:

R_0 = (0,0) of order 2 in curve

$$y^2\equiv x^3 + 10x + 0\pmod{31}$$

**rep as a torus**

$$y^2\equiv x^3 + 10x + 4\pmod{31}$$

has points R1=(23, 30) and R2=(6,30) with order 5 and 7 respectively.

**highlight the two points**

R3=(2,12) of order 11 and R_4 = (15, 13) order 3 on the invalid curve

$$y^2\equiv x^3 + 10x + 23\pmod{31}$$

**rep as a torus and hilight point**

<br>

## Online Portion

* * *

The only thing left to do now is to abuse the implementation of the protocol
so Bob unknowingly leaks information about his private key.

Here's what the first run looks like:

**network setup**

1. start a connection with the server claiming R1 is our public key.
2. Bob computes $$s_B R1 = 22R1 \equiv 2R1$$
3. send HMAC($$(1\times R_1)_x$$)
4. $$(1R1)_x \ne (2R1)_x$$ so server responds with `failure`

We keep trying until we reach success

1. start a connection with the server claiming R1 is our public key.
2. Bob computes $$s_B R1 = 22R1 \equiv 2R1\pmod{5}$$
3. send HMAC($$(2\times R_1)_x$$)
4. $$(2R1)_x == (2R1)_x$$ so server responds with `success`

We can use one of the Lemmas we developed earlier again

**pull from toolbox again**

tells us $$2\equiv \pm s_B\pmod{5}$$.
We can solve the plus minus ambiguity by squaring both sides: $$4\equiv s_B^2\pmod{5}$$.

**visual this congruence**

This gives us the first of our system of congruences, we find the remaining similarly

**fastforward connections**

4, 1, 0, 3

We are left with a system of congruences of Bob's public key and can use CRT to solve for
s_B^2 = 484 so s_b = \sqrt{484} = 22 as expected.

<br>

## Conclusion

* * *

On curves used in practice, this attack was achievable in as few as about 3000 queries. This made the attack
not only feasible but extremely quick (a matter of minutes potentially not counting the precomputations).
There are of course optimizations which can be made to make the attack even more efficient including parallelization.

Have a wonderful day. :)

* * *

## TLS and attack-only:

<br>

## Intro

* * *

<br>

**possibly have an animation running in the background, some music**

**heartbleed logo**

You may have heard the term "Heartbleed" and how it made the internet less secure.
Heartbleed was a bug which compromised internet communication
allowing theft of sensitive information; possibly even the server's private keys.

**heartbleed 2 mockup**

but Heartbleed isn't the only one of its kind.
There was another lesser known vulnerability --- present even in oracle's EC library.

This bug could have been disasterous it also allowed theft of a server's private keys.

In this video, we learn about ECs and the TLS ECDH protocol. We'll use this knowledge
to illustrate the math behind what could have been heartbleed's successor.

Some background in group theory, particularly cyclic groups is recommended.

**planes close in and black screen**

<br>

* * *

## EC

* * *

*music timings*

*~0:37*

We warm up with some definitions. We'll refer to congruences of the form

**120**

(congruence)

as elliptic curves and (x,y) pairs which satisfy them as ellptic curve points.

For example, if

**320**

a and b are 3 and p = 7, then on the grid of integers, there are infinitely many curve points,
shown here in red.

**points**

It's useful to categorize them into congruence classes component-wise mod p.

**multiple colours**

One can show that this set of points, along with a special identity element,
form a group under "addition".

**670**

To understand how we define addition,
let's compute the sum of the yellow and red curve points.

**760**

This is done by drawing a line between them, finding the third curve point it
intersects, and reflecting that across the x-axis.

**960**

Let's try this again this time staying within a p by p region by having
the left and right edges loop into each other and the similarly for the
top and bottom edges.

We arrive at an equivalent point mod p.

**1280**

In fact, any such curve can be characterized with its p by p region and
using some topology, we can better visualize the looping.

After stretching the region out, we simply glue the ends which loop
into each other together.

And we see, elliptic curves are really just donuts in disguise.

<br>

* * *

## TLS

* * *

We can now move on to the protocols.

**360**

Suppose Alice wants to securely connect to a banking website. We'll call the website host Bob.

**490**

Instead of carelessly sending sensitive information over the internet,
Alice and Bob wanna agree on a secret number to encrypt their conversation.

**720**

This should be done such a way so that even if someone is monitoring the conversation,
they can't efficiently guess the key they agreed on. (ie. there is no significant
advantage gained in evesdropping the key-establishment protocol).

**980**

One of the most popular ways to establish a secret number is as follows:

**1050**

Alice and Bob first agree on public parameters which include:

**1120**

the coefficients a,b and prime modulus p of an elliptic curve

$$y^2 \equiv x^3 + ax + b\pmod{p}$$

**1240**

the total number of points on the curve $$n$$,

and a point on the curve referred to as the "base point" $$G$$.

**1800**

Next, Alice and Bob independently choose a number between 1 and $$n$$.
These are called secret keys.

**1940**

Their public keys are computed as the base point added to itself
the secret key amount of times or equivalently, the secret times the base point.

The exchange then takes place

* * *

### TLS

* * *

**2130**

1. First, Alice shares her public key p' with Bob
2. **2240** Bob computes his secret times Alice's public point and defines $$k$$ as the x coord of that result. He sends Alice his public key.
3. **2440** Alice computes $$k'$$ as the x coord of her own secret times Bob's public key and sends Bob HMAC$$(k')$$
4. **2560** Bob completes the protocol by comparing what he receives and HMAC$$(k)$$ responding success if they match and failure otherwise.

**2730**

Alice and Bob have agreed on a secret number k = k'.

We took the x coordinates just as a simple way to turn the point into
a number which was our goal.

**2800**

The HMAC is worth explaining.

You can think of it as sending just a fingerprint to verify against or more formally, it behaves like
a "one-way function" with no inverse.

This can be used to confirm they agreed on the same key without leaking information to an evesdropper.

* * *

## The Attack

* * *

**3000**

with this, we're ready for the star of the show, the attack.

**camera change**

We'll use larger, more secure parameters this time around.

**3100**

with a = 10, b = 5, and $$p=31$$

$$y^2\equiv x^3 + 10x + 5\pmod{31}$$

**represent this as a torus**

This gives us a curve with $$n=42$$ points.

**points finish drawing about now**

**3260**

The number we want to crack is Bob's secret which for this example we'll say is 22

**s=22**

There's a few preparations we can make before establishing a connection with Bob:

**section out spot for the precomps**

**3470**

We first pick primes such that their product is larger than $$n^2 = 1764$$. Say 2, 3, 5, 7, and 11

**store these primes somewhere**

**3640**

Next, pick points on elliptic curves such that
those points have the same order as the chosen primes

**3770**

we have the point

(0,0) of order 2 on the first curve

$$y^2\equiv x^3 + 10x + 0\pmod{31}$$

**rep as a torus**

$$y^2\equiv x^3 + 10x + 4\pmod{31}$$

**3900**

The second curve
has points R1=(23, 30) and R2=(6,30) with orders 5 and 7 respectively.

**highlight the two points**

**4050**

Finally, the points R3=(2,12) of order 11 and R_4 = (15, 13) order 3 are both
on the curve

$$y^2\equiv x^3 + 10x + 23\pmod{31}$$

**rep as a torus and hilight point**

<br>

## Online Portion

* * *

**4210**

Now Mallory has
Bob unknowingly leak information about his private key
using the protocol we covered earlier.

Here's what the first run looks like:

**4380**

**network setup**

1. Mallory starts a connection with Bob claiming one of the crafted points is her public key.
2. **4515** Bob thinks the point is on the secure public curve so following protocol, Bob computes his secret times the point.
Since the point has order 2, this is equivalent to multiplying by 2.
3. **4660** Mallory then guesses the result is congruent 1 mod 2 and sends the corresponding HMAC to Bob
4. **4825** the points are different so fingerprints don't match and Bob responds with failure. $$(1R_0)_x \ne (2R_0)_x$$ so server responds with `failure`

**4975**

Mallory guessed wrong, so she restarts the connection.
The first half is the same but this time, she lets k' = 2 times the point

**5090**

This time, both parties arrived at the same point so Bob responds with success.

**5130**

Let's take a look at what we've got now

**visual this congruence**

**5280**

we learned that the x coordinate of 2 times our point is the same as the
x coordinate of bob's secret s times our point.

**5400**

ie. 2 congruent pm s mod 2

**5470**

The pm appears because the additive inverse of our point also shares the same x coordinate.
We can resolve this ambiguity by simply squaring both sides

0 equiv sB^2 mod 2

**5630**

if we continue this guess and check with Bob,

sb^2 equiv

0 mod 2

1 mod 3

4 mod 5

1 mod 7

0 mod 11

**fastforward connections**

we're left with a system of congruences for bob's secret squared.

**5740**

Next, let x1 to x5 be the solutions the following congruences

(equation)

**5820**

taking the smallest positive solution, CRT tells us s^2 = 484.
Taking square root we're left with s = 22 and Mallory has successfully cracked Bob's secret key.

<br>

## Conclusion

* * *

**Bill Evans Alice in Wonderland take 2 recording 7:47 theme returns + ending mimic**

On curves used in practice, this attack was achievable in a couple thousand queries. This made the attack
not only feasible but extremely quick (potentially a matter of minutes not counting the precomputations).
There are of course optimizations which can be made to make the attack even more efficient such as
paralellization.

This presentation is based heavily on work by Antipa et al which is included in the description. Make sure to
check it out for a more technical look at this attack.

I hope you were able to learn something, have a wonderful day. :)

