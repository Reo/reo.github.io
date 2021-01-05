---
layout: post
title: Cryptopals Challenges 31-32
category: crypto
author: 'reo'
tags: python cryptopals
mathjax: 
---

The final challenge of this [cryptopals set](https://cryptopals.com/)
has us use a timing leak to attack HMAC SHA-1.
Both challenges 31 and 32 are very similar so we go over both solutions here.

## Contents
{:.no_toc}

* Content
{:toc}

<br>

***

## System Setup

***

We will have a server running locally which checks whether or not an hmac is
valid in a way which leaks information. Let's call this `webapp.py`.
The insecure check will do a byte-by-byte
comparison with an artificial delay for each byte and exit early if at any point
the byte is different from the one it expects.

```python
from time import sleep
import os
import md4

GKEY=os.urandom(16)

def make_hmac(message):
    mmd = md4.MD4()
    mmd.add(GKEY + message)
    return mmd.finish()

def verify_hmac(message, hmac):
    return insecure_compare(make_hmac(message), hmac)

def insecure_compare(b1,b2):
    '''
    insecurely compares same-length bytestrings b1 and b2 byte-by-byte
    with a 50ms sleep in between
    '''
    if (len(b1) != len(b2)):
        print('wrong len!')
        return False

    for i in range(len(b1)):
        sleep(0.05)
        if (b1[i]!=b2[i]):
            return False
    return True
```

The artificial delay set here is 50ms, this can be tweaked and made smaller to
test the limits of our attack.

<br>

***

### Simple Python Web Server

***

Next, we have the part in charge of actually hosting the web server

```python
from flask import Flask
from flask import request
app = Flask(__name__)

@app.route('/data')
def verify():
    file = request.args.get('file').encode()
    sig = bytes.fromhex(request.args.get('signature'))
    if verify_hmac(file, sig):
        return 'OK!'
    else:
        print(make_hmac(file).hex())
        raise ValueError

app.run()
```

This starts a server which expects a `GET` request at `localhost:5000/data`
followed by a query string which has `file=<filename>&signature=<hmac>` where `<hmac>` is
the HMAC which corresponds to filename.

<br>

***

## Comparing Connection Times

***

We now tackle the file which performs the attack. We need a library which allows us
to connect to the server and one which will make timing operations easy.

```python
from urllib.parse import urlparse, parse_qs, quote
import http.client
import time
```

Assuming we don't know the delay the server adds, the idea here would be to set a baseline
of how long an incorrect comparison takes for a given byte position and compare it against
how long the comparison takes for all other byte values. The value which has the largest
difference when compared to this baseline is very likely the correct byte. We do this over
all 16 bytes of the signature.

```python
filename='malicious'

# assume the first byte is not \x00
baseline = connect('http://localhost:5000', filename, '0'*32)[1]

currbytes = bytearray(b'\x00'*16)
for pos in range(16):
    running_max = 0
    # 255 possible values
    for val in range(256):
        currbytes[pos] = val
        comp = connect('http://localhost:5000', filename, currbytes.hex())[1]
        if comp > running_max:
            running_max = comp
            running_val = val
    baseline = running_max
    currbytes[pos] = running_val
```

Notice that we crack the signature byte-by-byte so this is significantly faster than brute
force since there are only $$16\times 256$$ attempts with this approach
compared to the $$2^{128}$$ of brute force.

<br>

***

## Connecting to the Server

***

All that remains is the code which connects us to the server and times the interaction

```python
def connect(url, filename, sig):
    q = 'file=' + filename + '&signature=' + sig
    parsed = urlparse(url)
    httpconn = http.client.HTTPConnection(parsed.hostname, parsed.port)

    start = time.time_ns()
    httpconn.request('GET', '/data?' + q)
    status = httpconn.getresponse().status
    end = time.time_ns()
    diff = end - start

    return status, diff
```

<br>

***

## Conclusion

***

Once the attack finishes, we can use the status to verify it worked:

```python
if __name__ == "__main__":
    assert (connect('http://localhost:5000', filename, currbytes.hex())[0] == 200)
```

If the artificial delay were large enough, we would be able to terminate early in the conparison phase once
a large jump in computation time is found. As comparison timing gets smaller, it becomes difficult to
distinguish amongst the noise of things such as connection times etc. This can be somewhat improved
at the cost of running time by taking an average of various connection attempts with a given byte.

