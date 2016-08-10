#
# This source code is licensed under the terms of the
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2016
#


import datetime

from tilaushallinta.models import DBSession, Tavara
from tilaushallinta.views.shared.form_item_lists import save_changes
from tilaushallinta.views.shared.utils import string_to_float_or_value, string_to_float_or_zero


def part_new_from_dict(part_dict):
    return Tavara(date=datetime.datetime.now(),
                  koodi=part_dict['koodi'], nimi=part_dict['nimi'],
                  maara=string_to_float_or_value(part_dict['maara'], 1), hinta=string_to_float_or_zero(part_dict['hinta']),
                  yksikko=part_dict['yksikko'],
                  tyyppi=(
                      "" +
                      ('A' if ('A' in part_dict.keys()) else '') +
                      ('T' if ('T' in part_dict.keys()) else '')
                  ))


def part_create(order, part_dict):
    part = part_new_from_dict(part_dict)
    DBSession.add(part)
    order.tavarat.append(part)


def part_modify(order, part_dict):
    part = DBSession.query(Tavara).filter_by(id=part_dict['id']).first()
    part.koodi = part_dict['koodi']
    part.nimi = part_dict['nimi']
    part.maara = string_to_float_or_zero(part_dict['maara'])
    part.hinta = string_to_float_or_zero(part_dict['hinta'])
    part.yksikko = part_dict['yksikko']
    part.tyyppi = (
        "" +
        ('A' if ('A' in part_dict.keys()) else '') +
        ('T' if ('T' in part_dict.keys()) else '')
    )


def part_delete(order, part_dict):
    for part in order.tavarat:
        if part.id == int(part_dict['id']):
            order.tavarat.remove(part)
            DBSession.delete(part)


def save_parts(requst, order):
    save_changes(requst, order,
                 ['koodi', 'nimi', 'maara', 'hinta'],
                 part_create, part_modify, part_delete)
