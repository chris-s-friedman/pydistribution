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
        self.__logger__ = get_logger(__name__, testing_mode=False)
        if not isinstance(seed, int):
            raise TypeError("seed may only be an integer")
        self.seed = seed


class lcg(Random):
    """
    Linear Congruential Generators (LCG's)
    """

    def generic(self, n, a, mod, c, unif=True):
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
        :param unif: Indicate if the returned values should be transformed to be
        uniform(0,1) (between 0 and 1)
        :type unif: bool
        :yield: iterable of random numbers
        :rtype: iter
        """
        x = self.seed
        iter_n = 0
        while iter_n < n:
            x = ((a * x) + c) % mod
            if unif:
                yield x / mod
            else:
                yield x
            iter_n += 1

    def minstd(self, n):
        """
        LCG that uses the MINSTD configuration of an LCG:
        - a = 16807
        - c = 0
        - mod = (2 ^ 31) - 1

        :param n: number of random numbers to generate
        :type n: int
        :return: generated random numbers
        :rtype: iter
        """
        m = (2**31) - 1
        if not 1 < self.seed < m:
            raise ValueError(f"seed must be between 1 and {m}")
        return self.generic(n=n, a=16807, c=0, mod=m)

    def randu(self, n):
        """
        LCG that uses the RANDU configuration of an LCG:
        - a = 65539
        - c = 0
        - mod = (2 ^ 31)

        NOTE: RANDU is an example of a bad LCG. Do not use this in production.
        This implementation of an LCG is for educational purposes only.

        :param n: number of random numbers to generate
        :type n: int
        :return: generated random numbers
        :rtype: iter
        """
        m = 2**31
        if not 1 < self.seed < m:
            raise ValueError(f"seed must be between 1 and {m}")
        self.__logger__.warning(
            "RANDU is an example of an LCG with poor statistical properties."
            "Do not use this."
        )
        return self.generic(n=n, a=16807, c=0, mod=m)
