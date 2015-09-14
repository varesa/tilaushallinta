#
# This source code is licensed under the terms of the
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2015
#

import datetime
from tilaushallinta.models import Laite
from tilaushallinta import DBSession
from tilaushallinta.views.utils import string_to_float_or_zero


def remove_empty_laitteet(laitteet_tmp):
    laitteet = {}
    for laite_id, value in laitteet_tmp.items():
        if value['nimi'] != "" or value['tyyppitiedot'] != "" or value['maara'] != "" or value['valmistusvuosi'] != "":
            laitteet[laite_id] = value
    return laitteet


def laitteet_form_to_dict(request):
    laitteet = {}
    for key, value in request.POST.iteritems():
        if '-' not in key:
            continue

        laite_id, field = key.split('-')
        if laite_id not in laitteet.keys():
            laitteet[laite_id] = {}

        laitteet[laite_id][field] = value
    return laitteet


def laite_new_from_dict(laite_dict):
    return Laite(date=datetime.datetime.now(),
                 nimi=laite_dict['nimi'], tyyppitiedot=laite_dict['tyyppitiedot'],
                 maara=string_to_float_or_zero(laite_dict['maara']),
                 valmistusvuosi=string_to_float_or_zero(laite_dict['valmistusvuosi']),
                 tyyppi=(
                    "" +
                    ('H' if ('H' in laite_dict.keys()) else '') +
                    ('K' if ('K' in laite_dict.keys()) else '')
                 ))


def laite_modify_from_dict(laite_id, laite_dict):
    laite = DBSession.query(Laite).filter_by(id=laite_id).first()
    laite.nimi = laite_dict['nimi']
    laite.tyyppitiedot = laite_dict['tyyppitiedot']
    laite.maara = string_to_float_or_zero(laite_dict['maara'])
    laite.valmistusvuosi = string_to_float_or_zero(laite_dict['valmistusvuosi'])
    laite.tyyppi = (
        "" +
        ('H' if ('H' in laite_dict.keys()) else '') +
        ('K' if ('K' in laite_dict.keys()) else '')
    )


def save_laitteet(request, huolto):
    laitteet = remove_empty_laitteet(laitteet_form_to_dict(request))

    for laite_id, laite_dict in laitteet.items():  # Loop throug received list of items
        if 'n' in laite_id:                        # If 'n' -> we are creating a new item
            laite = laite_new_from_dict(laite_dict)
            DBSession.add(laite)
            huolto.laiteluettelo.laitteet.append(laite)
        else:
            if string_to_float_or_zero(laite_dict['maara']) == 0:
                for t in huolto.laitteet:
                    if t.id == int(laite_id):
                        huolto.laitteet.remove(t)
                        DBSession.delete(t)
            else:
                laite_modify_from_dict(laite_id, laite_dict)