---
layout: post
title: Cryptopals Challenges 19-20
category: crypto
author: 'reo'
tags: python cryptopals
mathjax: 
---

We complete [cryptopals challenge](https://cryptopals.com/)
20 in this post which involves breaking CTR mode and is a more complete
version of challenge 19.

## Contents
{:.no_toc}

* Content
{:toc}

<br>

***

## Observations

***

We are given a file with 60 lines all encrypted using AES CTR mode with the same
nonce.

```python
GKEY=os.urandom(16)
NONCE=os.urandom(8)

ctList = list()
# read each line into a separate list item. Decode and encrypt
with open('20.txt', 'r') as ptFile:
    for line in ptFile.read().splitlines():
        ctList.append(ctr_enc(base64.b64decode(line.replace('\n','')),GKEY,NONCE))
```

Our first observation is the fact that because all of the texts have been encrypted
using the same nonce, this can be reformulated as the repeating key xor problem
we solved in an [earlier challenge](/crypto/2020/07/14/06-crypals-challenge.html).

<br>

***

## Rephrasing the Problem as One We've Already Solved

***

We will use a similar approach using frequency analysis to determine the most likely
key and hence figure out a large portion of the plaintext.
Instead of a dictionary, we use an array this time with weights at the index which corresponds
to the numerical value of the ascii characters.

Frequencies were taken from [practical cryptography](http://practicalcryptography.com/cryptanalysis/letter-frequencies-various-languages/english-letter-frequencies/)
webpage.

```python
# letter frequencies courtesy of practical cryptography website
# index corresponds to ASCII value
freqs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.2, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         4, 0, 0, 0, 0, 0, 0, 0.2, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 8.55, 1.6, 3.16, 3.87, 12.1, 2.18, 2.09, 4.96, 7.33, 0.22, 0.81, 4.21, 2.53, 7.17, 7.47,
         2.07, 0.1, 6.33, 6.73, 8.94, 2.68, 1.06, 1.83, 0.19, 1.72, 0.11, 0, 0, 0, -4, 0,
         0, 8.55, 1.6, 3.16, 3.87, 12.1, 2.18, 2.09, 4.96, 7.33, 0.22, 0.81, 4.21, 2.53, 7.17, 7.47,
         2.07, 0.1, 6.33, 6.73, 8.94, 2.68, 1.06, 1.83, 0.19, 1.72, 0.11, 0, 0, 0, -4, 0]
```

In order to make the problem look even closer to repeating key xor, we trim them
to be the same length and concatenate them back to back.
`min(map(len, ctList))` is used here to grab the minimum length out of all of
the ciphertexts, this will be the common length we will use.

```python
# first trim all texts to the same length and concatenate them
keylen = min(map(len, ctList))
ct = b''
for i in range(len(ctList)):
    ct += ctList[i][:keylen]
```

Next, we figure out the byte most likely to be the correct key one byte at a time

```python
keyCand = b''
keySum = 0
for j in range(keylen): # over each byte of the key
    chunk = b''
    # combine bytes which are congruent mod keylen as a chunk
    for k in range(j, len(ct), keylen):
        chunk += bytes([ct[k]])
    # and create likely key fragments corresponding to each chunk
    keyFragment, fragmentSum = key_byte(chunk)
    keyCand += keyFragment
    keySum += fragmentSum
```

keySum here is optional but can be used in a stronger attack where we create a list
of the most likely keys and attempt those. For simplicity, we ignore its value in
this solution and use only the most likely key.

<br>

***

## Scoring Key Bytes

***

Our strategy used in computing the most likely key bytes is implemented in `key_byte()`:

```python
def key_byte(chunk):
    keyCand = -1 # the byte most likely to be the key
    sumCand = -1 # the total score of the most likely key

    for k in range(256): # for every possible 1-byte key
        currSum = 0
        for i in range(len(chunk)):
            # check what the current byte decrypts to and score appropriately
            char = k^chunk[i]
            if (bytes([char]).isascii()):
                currSum += freqs[char]
        if (currSum > sumCand): # update most likely candidate if necessary
            sumCand = currSum
            keyCand = bytes([k])
    return keyCand, sumCand
```

We can check that our strategy works by xoring the ciphertext against our attempted keys

```python
for i in range(len(ctList)):
    print(strxor(keyCand, ct[i*keylen:(i+1)*keylen]))
```

we get

```
b'I\'m rated "R"...this is a warning, ya better void / P'
b'Cuz I came back to attack others in spite- / Strike l'
b"But don't be afraid in the dark, in a park / Not a sc"
b'Ya tremble like a alcoholic, muscles tighten up / Wha'
b'Suddenly you feel like your in a horror flick / You g'
b"Music's the clue, when I come your warned / Apocalyps"
b"Haven't you ever heard of a MC-murderer? / This is th"
b'Death wish, so come on, step to this / Hysterical ide'
b'Friday the thirteenth, walking down Elm Street / You '
b'This is off limits, so your visions are blurry / All '
b"Terror in the styles, never error-files / Indeed I'm "
b'For those that oppose to be level or next to this / I'
b"Worse than a nightmare, you don't have to sleep a win"
b'Flashbacks interfere, ya start to hear: / The R-A-K-I'
b'Then the beat is hysterical / That makes Eric go get '
b'Soon the lyrical format is superior / Faces of death '
b"MC's decaying, cuz they never stayed / The scene of a"
b"The fiend of a rhyme on the mic that you know / It's "
b'Melodies-unmakable, pattern-unescapable / A horn if w'
b'I bless the child, the earth, the gods and bomb the r'
b'Hazardous to your health so be friendly / A matter of'
b"Shake 'till your clear, make it disappear, make the n"
b"If not, my soul'll release! / The scene is recreated,"
b'Cuz your about to see a disastrous sight / A performa'
b'Lyrics of fury! A fearified freestyle! / The "R" is i'
b"Make sure the system's loud when I mention / Phrases "
b'You want to hear some sounds that not only pounds but'
b'Then nonchalantly tell you what it mean to me / Stric'
b"And I don't care if the whole crowd's a witness! / I'"
b'Program into the speed of the rhyme, prepare to start'
b"Musical madness MC ever made, see it's / Now an emerg"
b"Open your mind, you will find every word'll be / Furi"
b"Battle's tempting...whatever suits ya! / For words th"
b"You think you're ruffer, then suffer the consequences"
b'I wake ya with hundreds of thousands of volts / Mic-t'
b'Novocain ease the pain it might save him / If not, Er'
b"Yo Rakim, what's up? / Yo, I'm doing the knowledge, E"
b'Well, check this out, since Norby Walters is our agen'
b'Kara Lewis is our agent, word up / Zakia and 4th and '
b"Okay, so who we rollin' with then? We rollin' with Ru"
b'Check this out, since we talking over / This def beat'
b'I wanna hear some of them def rhymes, you know what I'
b"Thinkin' of a master plan / 'Cuz ain't nuthin' but sw"
b'So I dig into my pocket, all my money is spent / So I'
b"So I start my mission, leave my residence / Thinkin' "
b'I need money, I used to be a stick-up kid / So I thin'
b"I used to roll up, this is a hold up, ain't nuthin' f"
b"But now I learned to earn 'cuz I'm righteous / I feel"
b'Search for a nine to five, if I strive / Then maybe I'
b"So I walk up the street whistlin' this / Feelin' out "
b'A pen and a paper, a stereo, a tape of / Me and Eric '
b'Fish, which is my favorite dish / But without no mone'
b"'Cuz I don't like to dream about gettin' paid / So I "
b'So now to test to see if I got pull / Hit the studio,'
b'Rakim, check this out, yo / You go to your girl house'
b"'Cause my girl is definitely mad / 'Cause it took us "
b"Yo, I hear what you're saying / So let's just pump th"
b'And count our money / Yo, well check this out, yo Eli'
b'Turn down the bass down / And let the beat just keep '
b'And we outta here / Yo, what happened to peace? / Pea'
```

Which is exactly the deciphered text (up to length of the shortest line) as desired.
