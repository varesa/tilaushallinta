#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2015
#


def string_to_float_or_zero(string):
    """
    Try to convert a string to an float, returns 0.0 on failure
    :param string: String to convert
    :type string: str
    :return: float value of the string or 0.0
    :rtype: float
    """
    try:
        return float(string.replace(',', '.'))
    except ValueError:
        return 0


def string_to_int_or_zero(string):
    """
    Try to convert a string to an int, returns 0 on failure
    :param string: String to convert
    :type string: str
    :return: integer value of the string or 0
    :rtype: int
    """
    try:
        return int(string)
    except ValueError:
        return 0
