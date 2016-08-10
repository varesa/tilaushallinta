#
# This source code is licensed under the terms of the
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2016
#

import datetime

from pyramid.view import view_config

from tilaushallinta.models import DBSession
from tilaushallinta.models import Paivaraportti
from tilaushallinta.models import Tilaus
from tilaushallinta.views.orders.order_parts import save_parts
from tilaushallinta.views.shared.update_tilaaja_kohde import update_tilaaja, update_kohde
from tilaushallinta.views.shared.utils import string_to_float_or_zero, string_to_int_or_zero


def compare_sets(list):
    difference = False
    for val1, val2 in list:
        if val1 != val2:
            difference = True
    return difference


def update_perustiedot(request):
    update_tilaaja(request.POST)
    update_kohde(request.POST)

    tilaus_id = request.matchdict['id']
    tilaus = DBSession.query(Tilaus).filter_by(id=tilaus_id).first()

    tilaus.muut_yhteysh = request.POST['muut_yhteysh']
    tilaus.tyo = request.POST['tyo']
    tilaus.maksuaika = request.POST['maksuaika']
    tilaus.viitenumero = request.POST['viitenumero']


def add_paivaraportti(tilaus):
    """
    Create a new Paivaraportti in the database
    :param tilaus: The order in which to create the new report
    :rtype: None
    """
    tilaus.paivaraportit.append(Paivaraportti(date=datetime.datetime.now(), hintaluokka=2,
                                              tunnit=0.0, matkat=0.0, muut=0.0))


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


@view_config(route_name='order_details', renderer='tilaushallinta.templates:orders/order_details.pt')
def view_order_details(request):
    order_id = request.matchdict['id']
    tilaus = DBSession.query(Tilaus).filter_by(id=order_id).first()

    if 'data' in request.POST.keys():

        #########################################################
        # Form data sent for updating the basic order information
        #########################################################

        if request.POST['data'] == 'perustiedot':
            update_perustiedot(request)

        ###########################################
        # Form data sent for updating daily reports
        ###########################################

        if request.POST['data'] == 'paivaraportti':
            if 'save' in request.POST.keys():
                save_paivaraportit(request, tilaus)
            elif 'add' in request.POST.keys():
                add_paivaraportti(tilaus)

        ############################################
        # Form data sent for updating the items list
        ############################################

        if request.POST['data'] == 'tavarat':
            save_parts(request, tilaus)

    current_date = datetime.datetime.now()

    return {'tilaus': tilaus, 'current_date': current_date, 'parts': sorted(tilaus.tavarat, key=lambda part: part.koodi)}
