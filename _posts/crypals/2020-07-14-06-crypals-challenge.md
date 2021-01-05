---
layout: post
title: Cryptopals Challenge 6
category: crypto
author: 'reo'
tags: python cryptopals
mathjax: 
---

This cryptopals challenge involves significantly more code.
In order to break repeating-key XOR we will also be moving away from our words file and turn to
[frequency analysis](https://en.wikipedia.org/wiki/Frequency_analysis)
when cracking the key.

## Contents
{:.no_toc}

* Content
{:toc}

<br>

* * *

## Setup

* * *

At the head of our file are the imports we use
```python
import base64
from Crypto.Util.strxor import strxor
from operator import itemgetter
```

we also want to import the text which we will use to attack the system (this is a known ciphertext attack)

```python
# grab text and remove newlines
CipherFile = open('6.txt', 'r')
cipherbytes = base64.b64decode(CipherFile.read().replace('\n',''))
textlen = len(cipherbytes)
CipherFile.close()
```

<br>

* * *

## Hamming Distance

* * *

Some helper functions will be useful in finding candidates for the key size.
Because the key repeats,
eventually we would have same characters encrypting to the same byte hence the
smaller the hamming distance between blocks of a guessed length, the more likely
the guessed length is the correct one.

We can write a method which computes the hamming distance
between a pair of byte strings `b1` and `b2`.

```python
def hamming_dist(b1, b2):
    diff = strxor(b1, b2)
    ham_dist = 0
    # count the number of '1's resulting from their xor
    for i in range(len(diff)):
        ham_dist += bin(diff[i]).count('1')
    return ham_dist
```

and more generally, we could use this to compute the average hamming distance between `n`
byte strings:

```python
def avg_hamming_dist(b, n, keylen):
    total = 0
    div = n*(n-1)/2 # number of comparisons is 1 + ... + n-1
    # compute hamming distance between every pair and divide by total number of comparisons
    for i in range(n-1):
        for j in range(i+1, n):
            total += hamming_dist(b[i*keylen:(i+1)*keylen], b[j*keylen:(j+1)*keylen])

    return (total/div)
```

<br>

* * *

## Crack the Key length

* * *

We could then write code which creates a list of likely key lengths. We exclude the
trivial length 1 keys since we have already broken that in a [previous challenge](/crypto/2020/06/30/crypals-challenges.html#challenge-3)
and guess that the key is no longer than 42 bytes but this can be adjusted to taste.

```python
keylen_list = list()
# our range of guesses for keylengths
for keylen in range(2, 42):
    guess_dist = avg_hamming_dist(cipherbytes, HAMMING_DIST_DEPTH, keylen)/keylen
    keylen_list.append((keylen, guess_dist))
keylen_candidates = sorted(keylen_list,key=itemgetter(1))
```

itemgetter here is used to sort the key lengths by how likely they are to appear (how small their
average hamming distance is) `HAMMING_DIST_DEPTH` is the number of blocks to check,
the more we check the slower the computation but the more accurate our average becomes.
Perhaps we choose

```python
HAMMING_DIST_DEPTH=15
```

<br>

* * *

## Keys given Key Length

* * *


After finding the most likely key lengths, we fix a keylength guess and
try to find the most likely keys given our fixed key length. We could do this
for various key-length guesses, say we pick
`KEYLEN_CANDIDATES_CHECKED=4` of them to check.

In turn, for each one of these we check we apply the single-byte XOR crack and assign a score
based on character frequencies. For example, if our key length guess is 8 we would
join all bytes with position congruent 0 mod 8 into a chunk and assign that a score using
single-byte XOR crack.
We would do the same for those congruent 1 mod 8 and so on. This would give us
a total score for the key in terms of letter frequencies.

```python
# letter frequencies courtesy of Wikipedia, space ' ' was estimated
freqs = {
        'e': 13, 't': 9.1, 'a': 8.2, 'o': 7.5, 'i': 7, 'n': 6.7, 's': 6.3, 'h': 6.1,
        'r': 6, 'd': 4.3, 'l': 4, 'c': 2.8, 'u': 2.8, 'm': 2.4, 'w': 2.4, 'f': 2.2,
        'g': 2, 'y': 2, 'p': 1.9, 'b': 1.5, 'v': 0.98, 'k': 0.77, 'j': 0.15, 'x':0.15,
        'q': 0.095, 'z': 0.074, ' ': 7
        }
```

```python
# now try to determine the key statistically by scoring possible key fragments
key_candidates = []
key_sums = []
for i in range(KEYLEN_CANDIDATES_CHECKED): # over the KEYLEN_CANDIDATES_CHECKED most probable key lengths
    curr_len = keylen_candidates[i][0]
    keyCand = b''
    keySum = 0 # An accumulator to store the score given to the current key guess
    for j in range(curr_len): # over each byte of the key
        chunk = b''
        # combine these bytes as a chunk
        for k in range(j, textlen, curr_len):
            chunk += bytes([cipherbytes[k]])
        # and create likely key fragments corresponding to each chunk
        keyFragment, fragmentSum = key_byte(chunk)
        keyCand += keyFragment
        keySum += fragmentSum
    key_candidates.append(keyCand)
    key_sums.append(keySum)
```

<br>

* * *

## Scoring Keys

* * *


We still need to go over how `key_byte()` determines a byte which is most likely for a given `chunk`.
As mentioned earlier, this is a scoring similar to what one would do for cracking single-byte
XOR except since these are spread across the string we cannot simply check for the existence of
a dictionary word.

```python
def key_byte(chunk):
    keyCand = -1 # the byte most likely to be the key
    sumCand = -1 # the total score of the most likely key

    for k in range(256): # for every possible 1-byte key
        currSum = 0
        for i in range(len(chunk)):
            # check what the current byte decrypts to and score appropriately
            char = bytes([k ^ chunk[i]])
            if ((char.isascii()) and (char.lower().decode() in freqs)):
                currSum += freqs[char.lower().decode()]
        if (currSum > sumCand):
            sumCand = currSum
            keyCand = bytes([k])
    return keyCand, sumCand
```

With this, we have a set of the most likely keys according to frequency analysis which we may present:

```python
print('the ' + str(KEYLEN_CANDIDATES_CHECKED) + ' most likely keys in order (in terms of keylength) are:')
for i in range(KEYLEN_CANDIDATES_CHECKED):
    print(key_candidates[i])
```

<br>

* * *

## Complete Code

* * *

An example solution to the challenge may then be the following code:

```python
from Crypto.Util.strxor import strxor
from operator import itemgetter

# letter frequencies courtesy of Wikipedia, space ' ' was estimated
freqs = {
        'e': 13, 't': 9.1, 'a': 8.2, 'o': 7.5, 'i': 7, 'n': 6.7, 's': 6.3, 'h': 6.1,
        'r': 6, 'd': 4.3, 'l': 4, 'c': 2.8, 'u': 2.8, 'm': 2.4, 'w': 2.4, 'f': 2.2,
        'g': 2, 'y': 2, 'p': 1.9, 'b': 1.5, 'v': 0.98, 'k': 0.77, 'j': 0.15, 'x':0.15,
        'q': 0.095, 'z': 0.074, ' ': 7
        }
HAMMING_DIST_DEPTH=15
KEYLEN_CANDIDATES_CHECKED=4

def hamming_dist(b1, b2):
    diff = strxor(b1, b2)
    ham_dist = 0
    # count the number of '1's resulting from their xor
    for i in range(len(diff)):
        ham_dist += bin(diff[i]).count('1')
    return ham_dist

def avg_hamming_dist(b, n, keylen):
    total = 0
    div = n*(n-1)/2 # number of comparisons is 1 + ... + n-1
    # compute hamming distance between every pair and divide by total number of comparisons
    for i in range(n-1):
        for j in range(i+1, n):
            total += hamming_dist(b[i*keylen:(i+1)*keylen], b[j*keylen:(j+1)*keylen])

    return (total/div)

def key_byte(chunk):
    keyCand = -1 # the byte most likelyl to be the key
    sumCand = -1 # the total score of the most likely key

    for k in range(256): # for every possible 1-byte key
        currSum = 0
        for i in range(len(chunk)):
            # check what the current byte decrypts to and score appropriately
            char = bytes([k ^ chunk[i]])
            if ((char.isascii()) and (char.lower().decode() in freqs)):
                currSum += freqs[char.lower().decode()]
        if (currSum > sumCand):
            sumCand = currSum
            keyCand = bytes([k])
    return keyCand, sumCand

# grab text and remove newlines
CipherFile = open('6.txt', 'r')
cipherbytes = base64.b64decode(CipherFile.read().replace('\n',''))
textlen = len(cipherbytes)
CipherFile.close()

keylen_list = list()
# our range of guesses for keylengths
for keylen in range(2, 42):
    guess_dist = avg_hamming_dist(cipherbytes, HAMMING_DIST_DEPTH, keylen)/keylen
    keylen_list.append((keylen, guess_dist))
keylen_candidates = sorted(keylen_list,key=itemgetter(1))

# now try to determine the key statistically by scoring possible key fragments
key_candidates = []
key_sums = []
for i in range(KEYLEN_CANDIDATES_CHECKED): # over the KEYLEN_CANDIDATES_CHECKED most probable key lengths
    curr_len = keylen_candidates[i][0]
    keyCand = b''
    keySum = 0
    for j in range(curr_len): # over each byte of the key
        chunk = b''
        # combine these bytes as a chunk
        for k in range(j, textlen, curr_len):
            chunk += bytes([cipherbytes[k]])
        # and create likely key fragments corresponding to each chunk
        keyFragment, fragmentSum = key_byte(chunk)
        keyCand += keyFragment
        keySum += fragmentSum
    key_candidates.append(keyCand)
    key_sums.append(keySum)

print('the ' + str(KEYLEN_CANDIDATES_CHECKED) + ' most likely keys in order (in terms of keylength) are:')
for i in range(KEYLEN_CANDIDATES_CHECKED):
    print(key_candidates[i])
```
