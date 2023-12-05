def is_01(u):
    """
    Test if a number is between 0 and 1

    :param u: number to test
    :type u: float
    :return: Indication if number is between 0 and 1
    :rtype: bool
    """
    if 0 < u < 1:
        return True
    else:
        return False
