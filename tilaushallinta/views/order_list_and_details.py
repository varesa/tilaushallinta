#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014
#

import datetime

from pyramid.view import view_config
from pyramid.response import Response

from ..models import DBSession
from ..models import Tilaaja
from ..models import Kohde
from ..models import Tilaus
from ..models import Tavara
from ..models import Paivaraportti


@view_config(route_name='order_list', renderer='../templates/orders/order_list.pt')
def view_tilaukset_list(request):
    tilaukset = DBSession.query(Tilaus).all()
    return {"tilaukset": tilaukset}


def compare_sets(list):
    difference = False
    for val1, val2 in list:
        if val1 != val2:
            difference = True
    return difference


def remove_empty_tavarat(tavarat_tmp):
    tavarat = {}
    for tavara_id, value in tavarat_tmp.items():
        if (value['koodi'] != "" or
            value['nimi'] != "" or
            value['maara'] != "" or
            value['hinta'] != ""):
            tavarat[tavara_id] = value
    return tavarat


def update_perustiedot(request, tilaus):
    tilaus_id = request.POST['tilaus_id']
    tilaaja_id = request.POST['tilaaja_id']
    kohde_id = request.POST['kohde_id']


    tilaaja = DBSession.query(Tilaaja).filter_by(id=tilaaja_id).first()

    tilaaja.nimi = request.POST['tilaaja_nimi']
    tilaaja.yritys = request.POST['tilaaja_yritys']
    tilaaja.ytunnus = request.POST['tilaaja_ytunnus']
    tilaaja.osoite = request.POST['tilaaja_osoite']
    tilaaja.postitoimipaikka = request.POST['tilaaja_postitoimipaikka']
    tilaaja.postinumero = request.POST['tilaaja_postinumero']
    tilaaja.puhelin = request.POST['tilaaja_puhelin']
    tilaaja.email = request.POST['tilaaja_email']


    kohde = DBSession.query(Kohde).filter_by(id=kohde_id).first()

    kohde.nimi = request.POST['kohde_nimi']
    kohde.yritys = request.POST['kohde_yritys']
    kohde.ytunnus = request.POST['kohde_ytunnus']
    kohde.osoite = request.POST['kohde_osoite']
    kohde.postitoimipaikka = request.POST['kohde_postitoimipaikka']
    kohde.postinumero = request.POST['kohde_postinumero']
    kohde.puhelin = request.POST['kohde_puhelin']
    kohde.email = request.POST['kohde_email']


    tilaus.muut_yhteysh = request.POST['muut_yhteysh']
    tilaus.tyo = request.POST['tyo']
    tilaus.maksuaika = request.POST['maksuaika']
    tilaus.viitenumero = request.POST['viitenumero']

    return tilaus


def add_paivaraportti(tilaus):
    """
    Create a new Paivaraportti in the database
    :param tilaus: The order in which to create the new report
    :rtype: None
    """
    tilaus.paivaraportit.append(Paivaraportti(date=datetime.datetime.now(), hintaluokka=2))


def raportit_form_to_dict(request):
    """
    Get data from request POST and put the values relevant to Paivaraportti objects in a dictionary
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


def string_to_float_or_zero(string):
    """
    Try to convert a string to an float, returns 0.0 on failure
    :param string: String to convert
    :type string: str
    :return: float value of the string or 0.0
    :rtype: float
    """
    try:
        return float(string)
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


def raportti_modify_from_dict(raportti_id, raportti_dict):
    """
    Modify a Paivaraportti object with data from a dictionary
    :param raportti_id: id of the object to modify
    :type raportti_id: int
    :param raportti_dict: dictionary with the new data
    :type raportti_dict: dict
    :rtype: None
    """
    raportti = DBSession.query(Paivaraportti).filter_by(id=raportti_id).first()
    raportti.teksti = raportti_dict['teksti']
    raportti.hintaluokka = string_to_int_or_zero(raportti_dict['hintaluokka'])
    raportti.matkat = string_to_float_or_zero(raportti_dict['matkat'])
    raportti.tunnit = string_to_float_or_zero(raportti_dict['tunnit'])
    raportti.muut   = string_to_float_or_zero(raportti_dict['muut'])


def save_paivaraportit(request, tilaus):
    """
    Save the Paivaraportti data
    :param request: Request from client containing new values as POST data
    :type request: Request
    :param tilaus: Tilaus object to save the data in
    :type tilaus: Tilaus
    :rtype: None
    """
    raportit_request = raportit_form_to_dict(request)

    for raportti_id, raportti_new in raportit_request.items():
        for raportti_old in tilaus.paivaraportit:
            if int(raportti_old.id) == int(raportti_id):
                raportti_modify_from_dict(raportti_id, raportti_new)


def tavarat_form_to_dict(request):
    tavarat = {}
    for key, value in request.POST.iteritems():
        if '-' not in key:
            continue

        tavara_id, field = key.split('-')
        if tavara_id not in tavarat.keys():
            tavarat[tavara_id] = {}

        tavarat[tavara_id][field] = value
    return tavarat


def tavara_new_from_dict(tavara_dict):
    return Tavara(date=datetime.datetime.now(),
                  koodi=tavara_dict['koodi'], nimi=tavara_dict['nimi'],
                  maara=string_to_int_or_zero(tavara_dict['maara']), hinta=string_to_float_or_zero(tavara_dict['hinta']),
                  tyyppi=(
                      "" +
                      ('A' if ('A' in tavara_dict.keys()) else '') +
                      ('T' if ('T' in tavara_dict.keys()) else '')
                  ))


def tavara_modify_from_dict(tavara_id, tavara_dict):
    tavara = DBSession.query(Tavara).filter_by(id=tavara_id).first()
    tavara.koodi = tavara_dict['koodi']
    tavara.nimi = tavara_dict['nimi']
    tavara.maara = string_to_int_or_zero(tavara_dict['maara'])
    tavara.hinta = string_to_float_or_zero(tavara_dict['hinta'])
    tavara.tyyppi = (
        "" +
        ('A' if ('A' in tavara_dict.keys()) else '') +
        ('T' if ('T' in tavara_dict.keys()) else '')
    )


def save_tavarat(request, tilaus):
    tavarat = remove_empty_tavarat(tavarat_form_to_dict(request))

    for tavara_id, tavara_dict in tavarat.items():  # Loop throug received list of items
        if 'n' in tavara_id:                        # If 'n' -> we are creating a new item
            tavara = tavara_new_from_dict(tavara_dict)
            DBSession.add(tavara)
            tilaus.tavarat.append(tavara)
        else:
            tavara_modify_from_dict(tavara_id, tavara_dict)
                    

@view_config(route_name='order_details', renderer='../templates/orders/order_details.pt')
def view_order_details(request):
    order_id = request.matchdict['id']
    tilaus = DBSession.query(Tilaus).filter_by(id=order_id).first()

    if 'data' in request.POST.keys():

        #########################################################
        # Form data sent for updating the basic order information
        #########################################################

        if request.POST['data'] == 'perustiedot':
            update_perustiedot(request, tilaus)

        ###########################################
        # Form data sent for updating daily reports
        ###########################################

        if request.POST['data'] == 'paivaraportti':
            if 'save' in request.POST.keys():
                save_paivaraportit(request, tilaus)
            elif 'add' in request.POST.keys():
                add_paivaraportti(tilaus)
            #update_paivaraportit(request, tilaus)

        ############################################
        # Form data sent for updating the items list
        ############################################

        if request.POST['data'] == 'tavarat':
            save_tavarat(request, tilaus)

    current_date = datetime.datetime.now()

    for x in tilaus.paivaraportit:
        print(str(x) + ", .date= " + str(x.date))

    return {'tilaus': tilaus, 'current_date': current_date}


@view_config(route_name='order_summary')
def view_order_summary(request):
    return {}


@view_config(route_name='order_setstate')
def view_order_setstate(request):
    order_id = request.matchdict['id']
    newstate = request.POST['newstate']

    tilaus = DBSession.query(Tilaus).filter_by(id=order_id).first()
    tilaus.tila = newstate

    return Response('OK')