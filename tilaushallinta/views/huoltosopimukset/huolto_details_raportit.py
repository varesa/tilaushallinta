#
# This source code is licensed under the terms of the
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2015
#

import datetime
from tilaushallinta.models import Huoltoraportti
from tilaushallinta import DBSession
from tilaushallinta.views.utils import string_to_int_or_zero, string_to_float_or_zero


def add_huoltoraportti(huolto):
    """
    Create a new Huoltoraportti in the database
    :param huolto: The order in which to create the new report
    :rtype: None
    """
    huolto.huoltoraportit.append(Huoltoraportti(date=datetime.datetime.now(), hintaluokka=2))


def raportit_form_to_dict(request):
    """
    Get data from request POST and put the values relevant to Huoltoraportti objects in a dictionary
    :param request: request to read POST data from
    :type request: Request
    :return: dictionary of dict[id][field] = value
    :rtype: dict
    """
    raportit = {}
    for key, value in request.POST.iteritems():
        if '-' not in key:
            continue

        raportti_id, field = key.split('-')
        if raportti_id not in raportit.keys():
            raportit[raportti_id] = {}

        raportit[raportti_id][field] = value

    return raportit


def raportti_modify_from_dict(raportti_id, raportti_dict):
    """
    Modify a Huoltoraportti object with data from a dictionary
    :param raportti_id: id of the object to modify
    :type raportti_id: int
    :param raportti_dict: dictionary with the new data
    :type raportti_dict: dict
    :rtype: None
    """
    raportti = DBSession.query(Huoltoraportti).filter_by(id=raportti_id).first()
    raportti.teksti = raportti_dict['teksti']
    raportti.hintaluokka = string_to_int_or_zero(raportti_dict['hintaluokka'])
    raportti.matkat = string_to_float_or_zero(raportti_dict['matkat'])
    raportti.tunnit = string_to_float_or_zero(raportti_dict['tunnit'])
    raportti.muut = string_to_float_or_zero(raportti_dict['muut'])


def save_huoltoraportit(request, huolto):
    """
    Save the Huoltoraportti data
    :param request: Request from client containing new values as POST data
    :type request: Request
    :param huolto: Huolto object to save the data in
    :type huolto: Huolto
    :rtype: None
    """
    raportit_request = raportit_form_to_dict(request)

    for raportti_id, raportti_new in raportit_request.items():
        for raportti_old in huolto.huoltoraportit:
            if int(raportti_old.id) == int(raportti_id):
                raportti_modify_from_dict(raportti_id, raportti_new)