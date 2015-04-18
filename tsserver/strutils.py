def to_camel_case(snake_case):
    """
    Convert snake_case string to camelCase

    :param snake_case: snake_case string to convert
    :type snake_case: str
    :return: camelCase string
    :rtype: str
    """
    words = snake_case.split('_')
    return words[0] + ''.join(x.capitalize() for x in words[1:])
