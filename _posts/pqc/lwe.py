import random
import scipy.stats as stats
import numpy as np

lower, upper = -2, 2
mu, sigma = 0, 0.5
X = stats.truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)

# prime number to use for field
q = 9791

# dimension
n = 7

A = []

# sample A
for i in range(n):
    A.append(random.sample(range(q), n))
A = np.array(A)

print(A)

# sample s
s = np.array(random.sample(range(q), n)).T

print(s)

E = []

for e in X.rvs(n):
    E.append(round(e))
E = np.array(E).T

print(E)

b = (A.dot(s) + E) % q

print(b)

# ENCRYPTION

# send a random bit
m = random.randint(0,1)

print('m is: ' + str(m))

s_prime = np.array(random.sample(range(q), n))

print(s_prime)

E_prime = []

for e in X.rvs(n):
    E_prime.append(round(e))
E_prime = np.array(E_prime)

print(E_prime)

E_double_prime = round(X.rvs(1)[0])

print(E_double_prime)

b_prime = (s_prime.dot(A) + E_prime) % q

print(b_prime)

v_prime = (s_prime.dot(b) + E_double_prime) % q

print('v prime')
print(v_prime)

c = (v_prime + ((q//2) * m)) % q

print(c)

# DECRYPTION

v = b_prime.dot(s) % q

print('v')
print(v)

m_prime = (c - v) % q

print(m_prime)

if ((m_prime <= q//4) or ((m_prime - q) >= -q//4)):
    print(m == 0)
else:
    print(m == 1)
