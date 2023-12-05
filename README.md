# pydistribution

Generate random variates in python

## Installation

### Installing from github

```sh
pip install git+https://github.com/chris-s-friedman/pydistribution@latest-release
```

### Installing from src

To install from src, download and unzip the source files or clone the repo into 
the directory `pydistribution`.

Then navigate into the cloned directory:

```sh
cd pydistribution
```

Finally, use pip to install the package:

```sh
pip install .
```


## Usage

`pydistribution` can generate random variates from 15 different probability 
distributions:

- Weibull
- Exponential
- Laplace
- Triangular
- Bernoulli
- Geometric
- Poisson
- Binomial
- Erlang
- Negative Binomial
- Chi Square
- t
- Cauchy
- F
- Normal

To generate random variates from different probability distributions:

```python
from pydistribution.distributions import *

# Weibull
print(weibull(lam=1, b=2))
# Exponential
print(exponential(lam=1))
# Laplace
print(laplace(u=0, b=5))
# Triangular
print(triangular(minimum=-40, mode=10, maximum=60))
# Bernoulli
print(bernoulli(p=0.5))
# Geometric
print(geometric(p=0.5))
# Poisson
print(poisson(lam=1))
# Binomial
print(binomial(n=10, p=0.5))
# Erlang
print(erlang(n=50, lam=1))
# Negative Binomial
print(negative_binomial(n=50, p=0.5))
# Chi Square
print(chi_square(n = 10))
# t
print(t(n = 5))
# Cauchy
print(cauchy())
# F
print(F(n = 50, m = 50))
# Normal
print(normal(mu=5, sigma=3.2))
```

### Specifying values for `u`

Some functions are only dependent on a single input uniform(0,1) random
number. For these functions, a value for `u` may be specified so that a
result may be generated for specific values of `u`:

```python
from pydistribution.distributions import bernoulli
print(bernoulli(p=0.5, u=.12345)) # returns 1
```

Visit the docstrings or look at the arguments for functions you are using to see
if a given function takes a value for `u`.

### Using a specific psuedo-random number generator

By default, `pydistribution` uses the uniform(0,1) psuedo-random number
generator (prng) packaged in the random module of base python,
`random.random()`.

To use the random.random() prng with a set seed and then generate a bernoulli
random variate:

```python
from pydistribution.distributions import bernoulli
import random

random.seed(12345678)
prng_with_seed = random.random

print(bernoulli(p=0.5, prng=prng_with_seed)) # returns 0
print(bernoulli(p=0.5, prng=prng_with_seed)) # returns 0
print(bernoulli(p=0.5, prng=prng_with_seed)) # returns 1
print(bernoulli(p=0.5, prng=prng_with_seed)) # returns 1
print(bernoulli(p=0.5, prng=prng_with_seed)) # returns 0
```

Likewise, you can use prngs from other packages, such as [numpy](https://numpy.org/doc/stable/reference/random/index.html).

To do the same as above with numpy's `default_rng` and a different seed:

```python
from pydistribution.distributions import bernoulli
from numpy.random import default_rng

np_prng = default_rng(987654321).random

print(bernoulli(p=0.5, prng=np_prng)) # returns 1
print(bernoulli(p=0.5, prng=np_prng)) # returns 1
print(bernoulli(p=0.5, prng=np_prng)) # returns 1
print(bernoulli(p=0.5, prng=np_prng)) # returns 1
print(bernoulli(p=0.5, prng=np_prng)) # returns 1
```

## Project Structure

At the root of the project is this readme file with specific instructions and
notes about `pydistribution`’s functionality and installation instructions. Also
at root is a file, `pyproject.toml`. This is a configuration file that contains
package metadata as well as instructions for how package managers should install
the code. Last, at root is a directory, `src`. Inside this folder is another
directory, `pydistribution`. Inside this folder is a file, `distributions.py`.
The contents of this file are the code used to generate RVs. 