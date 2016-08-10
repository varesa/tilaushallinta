#
# This source code is licensed under the terms of the
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2016
#

from tilaushallinta.views.shared.utils import string_to_float_or_zero


def form_to_dict(request):
    d = {}
    for key, value in request.POST.iteritems():
        if '-' not in key:
            continue

        item_id, field = key.split('-')
        if item_id not in d.keys():
            d[item_id] = {'id': item_id}

        d[item_id][field] = value
    return d


def remove_empty(items_tmp, fields):
    items = {}
    for item_id, item in items_tmp.items():
        for field in fields:
            if item[field] != "":
                items[item_id] = item
    return items


def save_changes(request, order, fields, createfunc, modifyfunc, deletefunc):
    items = remove_empty(form_to_dict(request), fields)

    keys = sorted(items.keys())
    for item_id in keys:
        item_dict = items[item_id]
        if 'n' in item_id:
            createfunc(order, item_dict)
        else:
            if string_to_float_or_zero(item_dict['maara']) == 0:
                deletefunc(order, item_dict)
            else:
                modifyfunc(order, item_dict)
