---
layout: post
title: "C parallel query"
date: 2019-03-13
category: Programming
author: "Reo"
tags: C systems-programming
mathjax: true
---

Parallel Query Engine for text files in C (B09 A3)


## Topics
{:.no_toc}

* Content
{:toc}

### Specifications

This query engine has two basic parts:

1. An indexer which creates a data structure efficient for searching
2. A query engine that performs the searches

We want the indexer and query engine to be run separately. The indexer creates an index for a
directory of files and write the data structure(s) to the respective file(s).

The query engine has the following behaviour:

- Load the indexer-generated file(s) into memory, by default from the directory the program is called
- While STDIN is open, prompt the user for a **string** to search for
- Upon confirming, return `MAXRECORDS` most frequent appearances of **string** and which file it appears in
- If the `-d` option is given, the argument gives the directory of where to check for the index file(s)

ie.

```
while STDIN open:
  read a word from STDIN
  add results to a master frequency array sorted by frequency
  print frequency array to STDOUT from highest to lowest
```

Some additional things to note are:

- Only store `MAXRECORDS` most frequent records. Anything less frequent, or which comes in earlier and
is tied are overwritten.
- Assume input string are no larger than 32 characters (32 bytes) including null termination character.

### Ideas/Technologies

For the indexer, we simply need to make the required system calls in reading the files. The rest is constructing the data structures. We choose to make two files, `index` and `filenames` for this project.

The data structure in `index` is a linked list containing the words and an array of frequencies.
the one in `filenames` is an array of strings whos index corresponds to that of the array of frequencies present in an `index` node.

Concerning the query engine, we again traverse the file system to find the desired directory. Once there, we load `index` and `filenames` into memory for each subdirectory.

We could take advantage of multiprocessing here by using calls to `fork()` and assigning forked processes to each index. This will minimize wasted CPU cycles.

It will be convenient to have a struct for the frequency records of fixed size so helper functions always read/write a fixed size and it is easy to indicate when there are no more records to send.

### Looking Ahead

This project deals mainly with reading, and interpreting large files using built-in C libraries.
My solution to this problem also took advantage of multiprogramming with elementary data structures
the usage of pipes to allow inter-process communication.

The next post regarding this project will cover the indexer.
