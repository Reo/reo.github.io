---
layout: post
title: "Hyper Sudoku Solver"
category: Programming
author: "Reo"
mathjax: true
---

Hyper Sudoku is a game with relatively simple rules. Here, I present a couple of possible algorithms for
solving said game. Ways to think about this solution include as a brute force "counting",
a "weighted graph" problem, restrictions problem, or as a "smallest cover" problem. I will go over
the brute force, and weighted graph solutions here.

## Topics
{:.no_toc}

* Content
{:toc}

### Specifications

This is a small, quick project which uses elementary data structures and algorithms to solve a
hyper sudoku puzzle. Once again, we will be using python.

First, the specifications. The puzzle board is given as an array of arrays which contain values
0 through 9. A 0 represents an "empty" spot while the remaining numbers hold their regular
meaning. Valid and non-valid boards are allowed though for boards with more than one solution,
any one solution will do. Non-valid boards expect a return value of `None` while valid boards
expect the same board with the 0s replaced with the solution numbers.

### Design take 1

At first glance, it may not seem like a terrible idea to simply traverse the board in some
arbitrary order, say top left to bottom right, trying all possible digits from 1 through 9 until a
valid number is found. If at any point there is a contradiction, we backtrack the last non-hint
spot with some leeway. If all possibilities are exhausted in the first attempted cell, then the
puzzle must therefore be unsolvable (since all possible numbers were found to cause a
contradiction).

The checks for move validity are intuitive: simply check the row, column, square, and (if
applicable) hypersquare the cell is a member of. Some comparisons can be saved each call by
noticing that there are three cells which are already checked during the square comparisons and
hence there is no need to check again during those for the row and column comparisons.

For the purposes of these checks, there is always a matrix which holds the "in progress" grid which
would be the same one that is returned if a solution is found. As can be expected, when backtracking
we may "erase" cell attempts by simply marking in a 0 in its spot.

This is a straight-forward DFS which makes it not too difficult to translate into working code
and the verification step is independent which allows the code to be modular and work for different
types of sudoku boards (X-sudoku etc.).

{: class="center"}
|![Brute force solving animation](https://upload.wikimedia.org/wikipedia/commons/8/8c/Sudoku_solved_by_bactracking.gif)|
|:--:|
|*Visualization of design 1 [source: Wikimedia](https://commons.wikimedia.org/wiki/File:Sudoku_solved_by_bactracking.gif)*|

### Efficiency and adversarial boards (1)

In terms of efficiency, in the worst case this implementation gets far with 1 through 9 in the
first empty cell causing a large amount of comparisons and backtracking. These come at a large cost
and can in fact make the solution take an unreasonably long time. Specifically, if we go my row and
top left to bottom right, the following board it constructed to force this algorithm to go through
the worst-case set of steps which makes visible the inefficiency of this design.

{: class="center"}
| ![Adversarial board for brute force](https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Sudoku_puzzle_hard_for_brute_force.svg/361px-Sudoku_puzzle_hard_for_brute_force.svg.png){: class="invert-color"} |
|:--:|
|*A Sudoku that is difficult to be solved by design 1. [source: Wikimedia](https://commons.wikimedia.org/wiki/File:Sudoku_puzzle_hard_for_brute_force.svg)*|

Since each empty space can have a digit 1-9, the complexity in practice can be exponential.

* * *

### Design take 2

In the previous design, the fixed order of choosing cells is a vulnerability (discussed further in
the conclusion). There are also comparisons which are done repeatedly without any need. For
example, if a 2 cannot go in cell (1, 1) because a hint is in that same row, then we should not
have check if a 2 can go in (1, 1) ever again.

Further, starting at a point where we run DFS with a large number of possibilities means we may
have to backtrack, at worst, as many times are there are possible branches to the start point. The
same idea carries on for the second and so on.

We notice that by attempting values, the possible valid moves for other cells also begins to
shrink. This shrinking means a smaller branching factor for the graph and hence less possible
backtracking. The motivation for design take 2 is then as follows:

Start by jotting down all possibilities for all empty cells as "small numbers" related to the cell.
From here, we see which cell has the least number valid moves and choose any one of those. After
this choice, we adjust any other empty cell accordingly (in the same row, etc.) which may lower the
number of possibilities. We then take the one which has the least possible number of moves after
this adjustment and so on.
If a contradiction is found, backtrack to a cell where we can make another choice and do so. If all
possibilities have been attempted for the first cell then the puzzle is unsolvable, otherwise, we
have the solution.

In view of this, the data structures which would facilitate this implementation would be a min-heap (priority queue)
which contains information about the cell using the number of valid moves in the cell as a priority
value. Further, we can use a matrix to keep track of index locations so as to not have to do
a linear search using the built-in index() function but for our purposes, the required efficiency
has been reached and for simplicity we may use index().

{: class="center"}
| ![A Sudoku board with "small numbers"](https://www.learn-sudoku.com/images/pencil_marks_sample.gif){: class="invert-color"} |
|:--:|
| *A Sudoku board with "small numbers". [source](https://www.learn-sudoku.com/pencil-marks.html)* |

### Efficiency and adversarial boards (2)

If we compare now the time complexity, we no longer have the issue of staring on a cell where we are
forced to try an unnecessarily large number of possibilities. With that comes in improvement in how
deep we must backtrack before trying more possibilities. Updating the list as we go along also gives
a reasonable probability of discovering possibility sets of size 0 or 1 which are immediate to
evaluate.

Further we now note that adversarial boards are not nearly as trivial to construct hence making
this a more consistent board. That is not to say that it is without faults however.

Unsolvable puzzles which require a large number of trials before the algorithm finds out no inputs
work do exist, one such being the following.

{: class="center"}
| ![unsolvable hard board for design 2](/assets/images/hyper-sudoku.png){: class="invert-color"}|
|:--:|
|*A Hyper-Sudoku which is difficult to solve using approach 2*|

### Conclusion

The first approach, though straight-forward, had  a lot of room for improvement and left a lot to be
desired in terms of efficiency. For instance,
having a fixed filling order makes it possible and even easy for someone who
intentionally wants to create a time-consuming board to do so. In fact, even without explicit
knowledge of the algorithm, it is possible to make a reasonable guess towards the path
taken by the algorithm by simply timing.

The second approach took on the most glaring issues without adding a whole lot of complexity, and
at the same time remained quite intuitive in the sense that it is a legitimize strategy for a
human to approach solving a sudoku puzzle as well.

