"""
Generate random variates from different distributions
"""
# pylint: disable=import-error disable the import error for random module
import math
from random import random  # noqa

from more_itertools import repeatfunc

DEFAULT_PRNG = random


def prn_handler(u, prng):
    if u is None:
        u = prng()
    if not 0 < u < 1:
        raise ValueError("U must be between 0 and 1")
    return u


def weibull(lam, b, u=None, prng=DEFAULT_PRNG()):
    u = prn_handler(u=u, prng=prng)
    return (-1 / lam) * math.log(u) ** (1 / b)


def exponential(lam, u=None, prng=DEFAULT_PRNG()):
    return weibull(u=u, lam=lam, b=1)


def triangular(minimum=0, mode=1, maximum=2, u=None, prng=DEFAULT_PRNG()):
    u = prn_handler(u=u, prng=prng)
    u_midpoint = (mode - minimum) / (maximum - minimum)
    if u < u_midpoint:
        x = minimum + math.sqrt(u * (maximum - minimum) * (mode - minimum))
    else:
        x = maximum - math.sqrt(
            (1 - u) * (maximum - minimum) * (maximum - mode)
        )
    return x


def bernouli(p, u=None, prng=DEFAULT_PRNG()):
    u = prn_handler(u=u, prng=prng)
    if u <= p:
        x = 1
    else:
        x = 0
    return x


def geometric(p, u=None, prng=DEFAULT_PRNG()):
    u = prn_handler(u=u, prng=prng)
    return math.ceil(math.log(1 - u) / math.log(1 - p))


def poisson(lam, prng=DEFAULT_PRNG):
    if lam <= 20:
        a = math.exp(-lam)
        p = 1
        x = -1
        while p < a:
            u = prn_handler(u=u, prng=prng)
            p *= u
            x += 1
    else:
        x = max(0, math.floor(lam + (math.sqrt(lam) * standard_normal()) + 0.5))
    return x


def binomial(n, p, prng=DEFAULT_PRNG):
    def trial():
        return bernouli(p=p, u=prng())

    return sum(repeatfunc(trial, times=n))


def erlang(lam, n, prng=DEFAULT_PRNG):
    return (-1 / lam) * math.prod(repeatfunc(prng, times=n))


def negative_binomial(n, p, prng=DEFAULT_PRNG):
    def trial():
        return geometric(p=p, u=prng())

    return sum(repeatfunc(trial, times=n))


def chi_square(n, prng=DEFAULT_PRNG):
    def trial():
        return standard_normal(prng=prng)(0, 1) ** 2

    return sum(repeatfunc(trial, times=n))


def t(n, prng=DEFAULT_PRNG):
    normal_rv = standard_normal(prng=prng)
    chi_sq_rv = chi_square(n, prng=prng)
    return normal_rv / math.sqrt(chi_sq_rv / n)


def cauchy(prng=DEFAULT_PRNG):
    return t(1, prng=prng)


def F(n, m, prng=DEFAULT_PRNG):
    return (chi_square(n, prng=prng) / n) * (chi_square(m, prng=prng) / m)


def standard_normal_crude(prng=DEFAULT_PRNG, u=None):
    u = prn_handler(u=u, prng=prng)

    def sign(x):
        if x > 0:
            return 1
        if x == 0:
            return 0
        return -1

    t = abs((-math.log(min(u, 1 - u)) ** 2) ** (0.5))

    c0 = 2.515517
    c1 = 0.802853
    c2 = 0.010328
    d1 = 1.432788
    d2 = 0.189269
    d3 = 0.001308

    return sign(u - 0.5) * (
        t
        - (
            (c0 + (c1 * t) + (c2 * (t**2)))
            / (1 + (d1 * t) + (d2 * (t**2)) + d3 * (t**3))
        )
    )


def standard_normal(prng=DEFAULT_PRNG, crude=False, pair=False):
    if crude:
        return standard_normal_crude(prng=prng)
    w = 1
    while w >= 1:
        u = [prn_handler(u=None, prng=prng) for i in range(2)]
        # center ui around 0:
        v = []
        for ui in u:
            v.append((2 * ui) - 1)
        w = sum([i**2 for i in v])
    y = math.sqrt((-2 * math.log(w)) / w)
    z = [i * y for i in v]
    if pair:
        return z
    return z[0]


def scaled_normal(mu, sigma, z=None, prng=DEFAULT_PRNG):
    if z is None:
        z = standard_normal(prng)
    return mu + (math.sqrt(sigma) * z)
