#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014
#


def get_latest_ids(arr):
    """
    Sort an list of database objects, returning the latest (highest uuid) of every objects (id)
    :param arr: list to be sorted
    :type arr: list
    :return: sorted and filtered list
    :rtype: list
    """

    latest = []
    lastid = None

    arr_sorted = sorted(arr, key=lambda obj: (obj.id, obj.uuid), reverse=True)
    """
    Sort like: tilaus3v3, tilaus3v2, tilaus3v1, tilaus2v2, tilaus2v1, ...
    First of every major number is the latest
    """
    for obj in arr_sorted:
        if obj.id is not lastid:
            latest.append(obj)
            lastid = obj.id
    latest.reverse()
    return latest