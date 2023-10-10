from datetime import datetime

from custom_python_tools.logging import get_logger


class Random(object):
    """
    Different Random Number Generators
    """

    def __init__(self, seed=round(datetime.now().timestamp())):
        """
        Class for generating pseudo-random-numbers.

        :param seed: starting value to generate prn's, defaults to
        round(datetime.now().timestamp())
        :type seed: int, optional
        """
        self.logger = get_logger(__name__, testing_mode=False)
        self.seed = seed

    def lcg_generic(self, n, a, mod, c):
        """
        generate random numbers using a linear congruential generator(LCG). An
        LCG follows the form X_{n+1} = ((a * x_{n}) + c) mod m.

        :param n: Number of random numbers to generate
        :type n: int
        :param a: multiplier
        :type a: int
        :param mod: modulus
        :type mod: int
        :param c: additive portion
        :type c: int
        :yield: iterable of random numbers
        :rtype: iter
        """
        x = self.seed
        iter_n = 0
        while iter_n < n:
            x = ((a * x) + c) % mod
            yield x
            iter_n += 1

    def lcg_minstd(self, n):
        """
        LCG that uses the minstd configuration of an LCG:
          - a = 16807
          - c = 0
          - mod = (2 ^ 31) - 1

        :param n: number of random numbers to generate
        :type n: int
        :return: generated random numbers
        :rtype: iter
        """
        return self.lcg_generic(n=n, a=16807, c=0, mod=(2**31) - 1)
