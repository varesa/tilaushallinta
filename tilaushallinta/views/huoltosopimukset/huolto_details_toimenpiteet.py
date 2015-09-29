#
# This source code is licensed under the terms of the
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2015
#

import datetime
from tilaushallinta.models import MaintenanceOperation
from tilaushallinta import DBSession
from tilaushallinta.views.utils import string_to_int_or_zero, string_to_float_or_zero


def add_lisatoimenpide(huolto):
    """
    Create a new MaintenanceOperation in the database
    :param huolto: The order in which to create the new report
    :rtype: None
    """
    huolto.lisatoimenpiteet.append(Lisatoimenpide(date=datetime.datetime.now(), hintaluokka=2))


def toimenpiteet_form_to_dict(request):
    """
    Get data from request POST and put the values relevant to MaintenanceOperation objects in a dictionary
    :param request: request to read POST data from
    :type request: Request
    :return: dictionary of dict[id][field] = value
    :rtype: dict
    """
    toimenpiteet = {}
    for key, value in request.POST.iteritems():
        if '-' not in key:
            continue

        toimenpide_id, field = key.split('-')
        if toimenpide_id not in toimenpiteet.keys():
            toimenpiteet[toimenpide_id] = {}

        toimenpiteet[toimenpide_id][field] = value

    return toimenpiteet


def toimenpide_modify_from_dict(toimenpide_id, toimenpide_dict):
    """
    Modify a MaintenanceOperation object with data from a dictionary
    :param toimenpide_id: id of the object to modify
    :type toimenpide_id: int
    :param toimenpide_dict: dictionary with the new data
    :type toimenpide_dict: dict
    :rtype: None
    """
    toimenpide = DBSession.query(Lisatoimenpide).filter_by(id=toimenpide_id).first()
    toimenpide.teksti = toimenpide_dict['teksti']
    toimenpide.hintaluokka = string_to_int_or_zero(toimenpide_dict['hintaluokka'])
    toimenpide.matkat = string_to_float_or_zero(toimenpide_dict['matkat'])
    toimenpide.tunnit = string_to_float_or_zero(toimenpide_dict['tunnit'])
    toimenpide.muut = string_to_float_or_zero(toimenpide_dict['muut'])


def save_lisatoimenpiteet(request, huolto):
    """
    Save the MaintenanceOperation data
    :param request: Request from client containing new values as POST data
    :type request: Request
    :param huolto: MaintenanceJob object to save the data in
    :type huolto: MaintenanceJob
    :rtype: None
    """
    toimenpiteet_request = toimenpiteet_form_to_dict(request)

    for toimenpide_id, toimenpide_new in toimenpiteet_request.items():
        for toimenpide_old in huolto.lisatoimenpiteet:
            if int(toimenpide_old.id) == int(toimenpide_id):
                toimenpide_modify_from_dict(toimenpide_id, toimenpide_new)