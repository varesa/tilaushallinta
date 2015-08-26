#
# This source code is licensed under the terms of the
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2015
#

import datetime

from pyramid.view import view_config

from tilaushallinta.models import DBSession
from tilaushallinta.models import Huolto
from tilaushallinta.models import Laite
from tilaushallinta.models import Huoltoraportti

from tilaushallinta.views.utils import string_to_float_or_zero, string_to_int_or_zero


def compare_sets(sets):
    difference = False
    for val1, val2 in sets:
        if val1 != val2:
            difference = True
    return difference


def remove_empty_laitteet(laitteet_tmp):
    laitteet = {}
    for laite_id, value in laitteet_tmp.items():
        if value['nimi'] != "" or value['tyyppitiedot'] != "" or value['maara'] != "" or value['valmistusvuosi'] != "":
            laitteet[laite_id] = value
    return laitteet


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
                    

@view_config(route_name='huolto_details', renderer='../../templates/huoltosopimus/huolto_details.pt')
def view_huolto_details(request):
    huolto_id = request.matchdict['huolto']
    huolto = DBSession.query(Huolto).filter_by(id=huolto_id).first()

    if 'data' in request.POST.keys():
        ###########################################
        # Form data sent for updating daily reports
        ###########################################

        if request.POST['data'] == 'huoltoraportti':
            if 'save' in request.POST.keys():
                save_huoltoraportit(request, huolto)
            elif 'add' in request.POST.keys():
                add_huoltoraportti(huolto)

        ############################################
        # Form data sent for updating the items list
        ############################################

        if request.POST['data'] == 'laitteet':
            save_laitteet(request, huolto)

    current_date = datetime.datetime.now()

    return {'huolto': huolto, 'current_date': current_date}
