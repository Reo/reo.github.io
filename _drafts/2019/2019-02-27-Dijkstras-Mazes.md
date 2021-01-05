---
layout: post
title: "Dijkstra's mazes (Design)"
date: 2019-04-03
category: Programming
tags: image python programming
author: "Reo"
mathjax: true
---

In this post, we go over an elementary approach for a computer to traditional mazes. This
will make use of the Python Imaging Library and as the posts then goes on to show, can be expanded
to highlighting other paths which may be desired.

## Topics
{:.no_toc}

* Content
{:toc}

### Specifications

For the initial problem, we formally define a maze to be a set of black and white pixels arranged
such that the top left and bottom right pixels are white, and there exists a conncted path
from the top left to the bottom right composed entirely of white pixels (no diagonal movement
allowed). The images are in PPM format.

### Design

As suggested by the title, we will be implementing the solution using Dijkstra's algorithm. Seeing
as this is a greedy algorithm we will maintain a priority queue which determines the next pixel
which is to be chosen. Seeing as for moderately large images, this queue can grow quite quickly,
we notice upon further inspection that if not careful, increasing the priority for items in the
queue can get costly using a linear search for finding the index.

There are of course solutions to this problem. One way to approach it may be to simply insert a new
item with the adjusted priority into the queue which is $$\mathcal{O(\lg n)}$$ but this grows
continues to grow the priority queue.

What we do instead is have a matrix with the same dimensions as the image and have the corresponding
item in the matrix store the index. This allows for constant time retrieval with the addition of
what amounts to a few assignments in other queue operations. This results in a much improved
amortized cost especially when considering the frequency that priorities are actually decreased.

From here on out, it is simply a matter of implementing Dijkstra's in the context of our problem.

### Efficiency and adversarial input

Given our choice of search for next move, it is possible to create a maze which takes the path
a through a long, and ultimately futile detour before trying the lower-priority routes. This can
cause the number of comparisons to increase enough to affect performance for sufficiently large
mazes and should be taken into consideration. If there are ties, there can be probabilistic
methods which may improve the expected time in these cases. The matrix used potentially takes up
more space than using a Python dictionary though it was chosen to maintain simplicity.

Go over possibilities for input which makes algorithm take longest time
and actual efficiency of the algorithm considering the chosen flow control
and data structures.

### Conclusion

Note how neat it is that something so practical can be interpreted as a
more general problem in computer science. Keeping to the spirit of this example,
we may adjust the weight function to trace different types of paths such as most similar colour.
We may select different start and end points, different priorities for next pixel
choice, etc.
