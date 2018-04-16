def map_range(s:  float, a: (float, float), b: (float, float)):
    '''
    Map a value from one range to another.
    :param s: The source value, it should be a float.
    :param a: The range where s exists
    :param b: The range onto which we want to map s.
    :return: The target value, s transformed from between a1 and a2 to between b1 and b2.
    '''
    (a1, a2), (b1, b2) = a, b

    # if target range is zero in size; value is same as top and bottom.
    if b1 == b2:
        return b1

    # if source range is zero in size; place value in middle of target range.
    if a1 == a2:
        return b1 + abs(b2 - b1) / 2

    return b1 + ((s - a1) * (b2 - b1) / (a2 - a1))
