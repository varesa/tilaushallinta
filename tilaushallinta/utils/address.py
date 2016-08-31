#
# This source code is licensed under the terms of the
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2016
#


def join_address(address, postcode, city):
    """
    Join address components checking for empty components
    :param list:
    :return:
    """
    city = ' '.join(filter(len, [postcode, city]))
    components = filter(len, [address, city])
    address = ', '.join(components)
    return address