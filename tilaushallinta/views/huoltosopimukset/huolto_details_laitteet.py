#
# This source code is licensed under the terms of the
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2016
#

import datetime

from tilaushallinta import DBSession
from tilaushallinta.models import Laite
from tilaushallinta.views.shared.form_item_lists import save_changes
from tilaushallinta.views.shared.utils import string_to_float_or_zero, string_to_float_or_value


def device_new_from_dict(device_dict):
    return Laite(date=datetime.datetime.now(),
                 nimi=device_dict['nimi'], tyyppitiedot=device_dict['tyyppitiedot'],
                 maara=string_to_float_or_value(device_dict['maara'], 1),
                 valmistusvuosi=string_to_float_or_zero(device_dict['valmistusvuosi']),
                 tyyppi=(
                    "" +
                    ('H' if ('H' in device_dict.keys()) else '') +
                    ('K' if ('K' in device_dict.keys()) else '')
                 ))


def device_new(job, device_dict):
    device = device_new_from_dict(device_dict)
    DBSession.add(device)
    job.laiteluettelo.laitteet.append(device)


def device_modify(job, device_dict):
    laite = DBSession.query(Laite).filter_by(id=device_dict['id']).first()
    laite.nimi = device_dict['nimi']
    laite.tyyppitiedot = device_dict['tyyppitiedot']
    laite.maara = string_to_float_or_zero(device_dict['maara'])
    laite.valmistusvuosi = string_to_float_or_zero(device_dict['valmistusvuosi'])
    laite.tyyppi = (
        "" +
        ('H' if ('H' in device_dict.keys()) else '') +
        ('K' if ('K' in device_dict.keys()) else '')
    )


def device_delete(job, device_dict):
    for device in job.laiteluettelo.laitteet:
        if device.id == int(device_dict['id']):
            job.laiteluettelo.laitteet.remove(device)
            DBSession.delete(device)


def save_devices(request, job):
    save_changes(request, job,
                 ['nimi', 'tyyppitiedot', 'maara', 'valmistusvuosi'],
                 device_new, device_modify, device_delete)
