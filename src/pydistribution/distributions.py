"""
Generate random variates from different distributions
"""
# pylint: disable=import-error disable the import error for random module
import math
from random import random  # noqa

from more_itertools import repeatfunc

DEFAULT_PRNG = random


def prn_handler(u, prng):
    """
    create a prn if needed and check that the prn is between 0 and 1

    :param u: psuedo random number, expected to come from the uniform(0,1) distribution
    :type u: float
    :param prng: pseudo-random number generator function that generates uniform(0,1) prn's
    :type prng: builtin_function_or_method
    :raises ValueError: occurs when u is not between 0 and 1
    :return: u or a newly generated u from the specified prng
    :rtype: float
    """
    if u is None:
        u = prng()
    if not 0 <= u < 1:
        raise ValueError("U must be between 0 and 1")
    return u


def weibull(lam, b, u=None, prng=DEFAULT_PRNG):
    """
    Generate a random variate from the Weibull Distribution

    Weibull distribution is commonly used to model time to failure.

    :param lam: lambda parameter of the Weibull distribution
    :type lam: int
    :param b: beta parameter of the Weibull distribution
    :type b: int
    :param u: psuedo random number, expected to come from the uniform(0,1) distribution
    :type u: float
    :param prng: pseudo-random number generator function that generates uniform(0,1) prn's
    :type prng: builtin_function_or_method
    :return: Random Variate from the Weibull Distribution
    :rtype: float
    """
    u = prn_handler(u=u, prng=prng)
    return (-1 / lam) * math.log(u) ** (1 / b)


def exponential(lam, u=None, prng=DEFAULT_PRNG):
    """
    Generate a random variate from the Exponential Distribution

    The exponential distribution is usually used to model the time between
    events in a poisson process.

    The exponential distribution is a special case of the Weibull distribution
    where b = 1.

    :param lam: lambda parameter of the exponential distribution
    :type lam: int or float greater than 0
    :param u: psuedo random number, expected to come from the uniform(0,1) distribution
    :type u: float
    :param prng: pseudo-random number generator function that generates uniform(0,1) prn's
    :type prng: builtin_function_or_method
    :return: random variate from the Exponential Distribution
    :rtype: float
    """
    return weibull(u=u, lam=lam, b=1, prng=prng)


def laplace(mu, b, prng=DEFAULT_PRNG):
    """
    Generate a random variate from the Laplace Distribution

    The laplace distribution is two exponential distributions mirrored around
    a point, mu where each exponential distribution has a value of lambda 1/b

    :param mu: central location of the distribution
    :type mu: int or float
    :param b: denominator of the lambda parameter for the exponentials
    :type b: int greater than 0
    :param prng: pseudo-random number generator function that generates uniform(0,1) prn's
    :type prng: builtin_function_or_method
    :return: random variate from the Laplace Distribution
    :rtype: float
    """
    return mu + (exponential(1 / b, prng=prng) - exponential(1 / b, prng=prng))


def triangular(minimum=0, mode=1, maximum=2, u=None, prng=DEFAULT_PRNG):
    """
    Generate a random variate from the Triangular Distribution

    The triangular distribution is useful to approximate processes where the
    measures of central tendency are known but there is not enough data to
    determine the shape of the distribution. The minimum, mode, and maximum
    values are used to approximate the distribution. The pdf of the triangular
    distribution graphed looks like a triangle.

    :param minimum: minimum value, defaults to 0
    :type minimum: int, optional
    :param mode: mode, defaults to 1
    :type mode: int, optional
    :param maximum: maximum value, defaults to 2
    :type maximum: int, optional
    :param u: psuedo random number, expected to come from the uniform(0,1) distribution
    :type u: float
    :param prng: pseudo-random number generator function that generates uniform(0,1) prn's
    :type prng: builtin_function_or_method
    :return: random variate from the Triangular Distribution
    :rtype: float
    """
    u = prn_handler(u=u, prng=prng)
    u_midpoint = (mode - minimum) / (maximum - minimum)
    if u < u_midpoint:
        x = minimum + math.sqrt(u * (maximum - minimum) * (mode - minimum))
    else:
        x = maximum - math.sqrt(
            (1 - u) * (maximum - minimum) * (maximum - mode)
        )
    return x


def bernoulli(p, u=None, prng=DEFAULT_PRNG):
    """
    Generate a random variate from the Bernoulli Distribution

    The bernoulli distribution is the result of a binary event (e.g. a coin
    flip) with a probability of success p.

    :param p: proability of a success
    :type p: float
    :param u: psuedo random number, expected to come from the uniform(0,1) distribution
    :type u: float
    :param prng: pseudo-random number generator function that generates uniform(0,1) prn's
    :type prng: builtin_function_or_method
    :return: 1 or 0
    :rtype: int
    """
    u = prn_handler(u=u, prng=prng)
    if u <= p:
        x = 1
    else:
        x = 0
    return x


def geometric(p, u=None, prng=DEFAULT_PRNG):
    """
    Generate a random variate from the Geometric Distribution

    The geometric distribution is the number of failures before the first
    success in a sequence of iid Bernoulli trials.

    :param p: probability of a success
    :type p: float
    :param u: psuedo random number, expected to come from the uniform(0,1) distribution
    :type u: float
    :param prng: pseudo-random number generator function that generates uniform(0,1) prn's
    :type prng: builtin_function_or_method
    :return: random variate from the Geometric Distribution
    :rtype: float
    """
    u = prn_handler(u=u, prng=prng)
    return math.ceil(math.log(1 - u) / math.log(1 - p))


def poisson(lam, prng=DEFAULT_PRNG):
    """
    Generate a random variate from the Poisson Distribution

    A poisson process relates to the number of events that occur in a given
    time interval.

    This implementation uses the acceptance rejection method to generate the
    random variate.

    :param lam: lambda parameter
    :type lam: int greater than 0
    :param prng: pseudo-random number generator function that generates uniform(0,1) prn's
    :type prng: builtin_function_or_method
    :return: random variate from the Poisson Distribution
    :rtype: int
    """
    if lam <= 20:
        a = math.exp(-lam)
        p = 1
        x = -1
        while p < a:
            u = prn_handler(u=None, prng=prng)
            p *= u
            x += 1
    else:
        x = max(0, math.floor(lam + (math.sqrt(lam) * standard_normal()) + 0.5))
    return x


def binomial(n, p, prng=DEFAULT_PRNG):
    """
    Generate a random variate from the Binomial Distribution

    The binomial distribution is the number of successes in n iid bernoulli
    trials.

    This implementation uses the convolutional method to sum n iid bernoulli
    random variates.

    :param n: number of bernoulli trials
    :type n: int
    :param p: probability of a success
    :type p: float
    :param prng: pseudo-random number generator function that generates uniform(0,1) prn's
    :type prng: builtin_function_or_method
    :return: random variate from the Binomial Distribution
    :rtype: int
    """

    def trial():
        return bernoulli(p=p, u=prng())

    return sum(repeatfunc(trial, times=n))


def erlang(lam, n, prng=DEFAULT_PRNG):
    """
    Generate a random variate from the Erlang Distribution

    The erlang distribution is the time until the nth event in a poisson process.

    This implementation uses the inverse transform method to generate the
    random variate. Another implementation could also use the convolutional
    method to take the sum of n iid exponential random variates. The inverse
    transform method is used here because it is more efficient. This efficiency
    is because only one log operation is performed instead of n log operations.

    :param lam: lambda parameter
    :type lam: int or float
    :param n: number of iid RVs to use to calculate. If modelling poisson
    process, n is the number of events to wait for.
    :type n: int
    :param prng: pseudo-random number generator function that generates uniform(0,1) prn's
    :type prng: builtin_function_or_method
    :return: random variate from the Erlang Distribution
    :rtype: float
    """
    return (-1 / lam) * math.prod(repeatfunc(prng, times=n))


def negative_binomial(n, p, prng=DEFAULT_PRNG):
    """
    Generate a random variate from the Negative Binomial Distribution

    The negative binomial distribution is the number of failures before the nth
    success in a sequence of iid Bernoulli trials. Put another way (and
    representative of the implementation of this function), the sum of n iid
    geometric random variates.

    This implementation uses the convolutional method to sum n geometric random
    variates.

    :param n: number of success, number of geometric random variates to sum
    :type n: int
    :param p: probability of a success
    :type p: float
    :param prng: pseudo-random number generator function that generates uniform(0,1) prn's
    :type prng: builtin_function_or_method
    :return: _description_
    :rtype: float
    """

    def trial():
        return geometric(p=p, u=prng())

    return sum(repeatfunc(trial, times=n))


def chi_square(n, prng=DEFAULT_PRNG):
    """
    Generate a random variate from the Chi-Square Distribution

    The sum of some number of iid squared standard normal random variates.

    This implementation uses the convolutional method to sum n standard normal
    random variates.

    :param n: the number of standard normal distributions to square and sum
    :type n: int
    :param prng: pseudo-random number generator function that generates uniform(0,1) prn's
    :type prng: builtin_function_or_method
    :return: random variate from the Chi-Square Distribution
    :rtype: float
    """

    def trial():
        return standard_normal(prng=prng) ** 2

    return sum(repeatfunc(trial, times=n))


def t(n, prng=DEFAULT_PRNG):
    """
    Generate a random variate from the t Distribution

    The ratio of a standard normal random variate to the square root of the ratio
    of a chi-square random variate to its degrees of freedom (i.e. the number of
    normal distributions that were squared to generate the chi-square random
    variate, n parameter for the chi-square random variate).

    :param n: number of standard normal distributions to square and sum, degrees
    of freedom
    :type n: int
    :param prng: pseudo-random number generator function that generates uniform(0,1) prn's
    :type prng: builtin_function_or_method
    :return: random variate from the t Distribution
    :rtype: float
    """
    normal_rv = standard_normal(prng=prng)
    chi_sq_rv = chi_square(n, prng=prng)
    return normal_rv / math.sqrt(chi_sq_rv / n)


def cauchy(prng=DEFAULT_PRNG):
    """
    Generate a random variate from the Cauchy Distribution

    The cauchy distribution is a generalization of the t distribution with 1
    degree of freedom.

    :param prng: pseudo-random number generator function that generates uniform(0,1) prn's
    :type prng: builtin_function_or_method
    :return: random variate from the Cauchy Distribution
    :rtype: float
    """
    return t(1, prng=prng)


def F(n, m, prng=DEFAULT_PRNG):
    """
    Generate a random variate from the F Distribution

    Generates the random variate by taking the product of the ratio of two
    chi-square random variates to their degrees of freedom (i.e. the number of
    normal distributions that were squared to generate the chi-square random
    variates, n parameter for each chi-square random variate).

    :param n: number of standard normal distributions to square and sum for the
    first chi-square random variate
    :type n: int
    :param m: number of standard normal distributions to square and sum for the
    second chi-square random variate
    :type m: int
    :param prng: pseudo-random number generator function that generates uniform(0,1) prn's
    :type prng: builtin_function_or_method
    :return: random variate from the F Distribution
    :rtype: float
    """
    return (chi_square(n, prng=prng) / n) * (chi_square(m, prng=prng) / m)


def standard_normal_crude(u=None, prng=DEFAULT_PRNG):
    """
    Generate a random variate from the Standard Normal Distribution using the A&S Method

    The A&S method is an approximate method for generating standard normal
    random variates. This method approximates the inverse CDF of the normal
    distribution. This method has an approximate  error of less than or equal
    to .00045

    :param u: psuedo random number, expected to come from the uniform(0,1) distribution
    :type u: float
    :param prng: pseudo-random number generator function that generates uniform(0,1) prn's
    :type prng: builtin_function_or_method
    :return: Random Variate from the Standard Normal Distribution
    :rtype: float
    """
    u = prn_handler(u=u, prng=prng)

    def sign(x):
        """
        Get the sign of a number

        :param x: number to get the sign of
        :type x: int or float
        :return: 1,0, or -1 depending on the sign of x
        :rtype: signed int
        """
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
    """
    Generate a random variate from the Standard Normal Distribution using the Polar Method

    :param prng: pseudo-random number generator function that generates uniform(0,1) prn's
    :type prng: builtin_function_or_method
    :param crude: Should the crude standard normal generator be used, defaults to False
    :type crude: bool, optional
    :param pair: Should a pair of standard normals be returned or only one,
    defaults to False, i.e. only one number is returned
    :type pair: bool, optional
    :return: one or two standard normal random variates
    :rtype: float or list of floats
    """
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


def normal(mu, sigma, z=None, prng=DEFAULT_PRNG):
    """
    Generate a random variate from the Normal Distribution

    :param mu: mu or mean parameter of the Normal Distribution
    :type mu: int or float
    :param sigma: sigma or standard deviation parameter of the Normal
    Distribution
    :type sigma: int or float
    :param z: Location on the standard normal distribution , defaults to None.
    If None, a random number will be generated
    :type z: float, optional
    :param prng: pseudo-random number generator function that generates uniform(0,1) prn's
    :type prng: builtin_function_or_method
    :return: Random Variate from the Normal Distribution
    :rtype: float
    """
    if z is None:
        z = standard_normal(prng)
    return mu + (math.sqrt(sigma) * z)
