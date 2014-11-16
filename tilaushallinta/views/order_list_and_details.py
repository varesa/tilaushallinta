#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014
#

import datetime

from pyramid.view import view_config

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


def update_perustiedot(request, tilaus): # TODO: Remove redundant checks
    tilaus_uuid = request.POST['tilaus_uuid']
    tilaaja_uuid = request.POST['tilaaja_uuid']
    kohde_uuid = request.POST['kohde_uuid']
    # Check for differences in "Tilaaja" model
    tilaaja_old = DBSession.query(Tilaaja).filter_by(uuid=tilaaja_uuid).first()
    tilaaja_differs = compare_sets(
        ((tilaaja_old.nimi, request.POST['tilaaja_nimi']),
         (tilaaja_old.yritys, request.POST['tilaaja_yritys']),
         (tilaaja_old.ytunnus, request.POST['tilaaja_ytunnus']),
         (tilaaja_old.osoite, request.POST['tilaaja_osoite']),
         (tilaaja_old.postitoimipaikka, request.POST['tilaaja_postitoimipaikka']),
         (tilaaja_old.postinumero, request.POST['tilaaja_postinumero']),
         (tilaaja_old.puhelin, request.POST['tilaaja_puh']),
         (tilaaja_old.email, request.POST['tilaaja_email']))
    )
    tilaaja = None
    if tilaaja_differs:
        tilaaja.nimi = request.POST['tilaaja_nimi']
        tilaaja.yritys = request.POST['tilaaja_yritys']
        tilaaja.ytunnus = request.POST['tilaaja_ytunnus']
        tilaaja.osoite = request.POST['tilaaja_osoite']
        tilaaja.postitoimipaikka = request.POST['tilaaja_postitoimipaikka']
        tilaaja.postinumero = request.POST['tilaaja_postinumero']
        tilaaja.puhelin = request.POST['tilaaja_puh']
        tilaaja.email = request.POST['tilaaja_email']


    # Check for differences in "Kohde" model
    kohde_old = DBSession.query(Kohde).filter_by(uuid=kohde_uuid).first()
    kohde_differs = compare_sets(
        ((kohde_old.nimi, request.POST['kohde_nimi']),
         (kohde_old.yritys, request.POST['kohde_yritys']),
         (kohde_old.ytunnus, request.POST['kohde_ytunnus']),
         (kohde_old.osoite, request.POST['kohde_osoite']),
         (kohde_old.postitoimipaikka, request.POST['kohde_postitoimipaikka']),
         (kohde_old.postinumero, request.POST['kohde_postinumero']),
         (kohde_old.puhelin, request.POST['kohde_puh']),
         (kohde_old.email, request.POST['kohde_email']))
    )
    kohde = None
    if kohde_differs:
        kohde.nimi = request.POST['kohde_nimi']
        kohde.yritys = request.POST['kohde_yritys']
        kohde.ytunnus = request.POST['kohde_ytunnus']
        kohde.osoite = request.POST['kohde_osoite']
        kohde.postitoimipaikka = request.POST['kohde_postitoimipaikka']
        kohde.postinumero = request.POST['kohde_postinumero']
        kohde.puhelin = request.POST['kohde_puh']
        kohde.email = request.POST['kohde_email']

    # Check for differences in the "Tilaus" model
    tilaus_old = DBSession.query(Tilaus).filter_by(uuid=tilaus_uuid).first()
    tilaus_differs = compare_sets(
        ((tilaus_old.muut_yhteysh, request.POST['muut_yhteysh']),
         (tilaus_old.tyo, request.POST['tyo']),
         (tilaus_old.maksuaika, request.POST['maksuaika']),
         (tilaus.viitenumero, request.POST['viitenumero']))
    )
    if tilaus_differs:

        tilaus_old.muut_yhteysh = request.POST['muut_yhteysh']
        tilaus_old.tyo = request.POST['tyo']
        tilaus_old.maksuaika = request.POST['maksuaika']
        tilaus_old.viitenumero = request.POST['viitenumero']

        tilaus = DBSession.query(Tilaus).order_by(Tilaus.uuid.desc()).first()

    return tilaus


def add_paivaraportti(tilaus):
    tilaus.paivaraportit.append(Paivaraportti(date=datetime.datetime.now()))


def raportit_form_to_dict(request):
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
    try:
        return float(string)
    except ValueError:
        return 0


def string_to_int_or_zero(string):
    try:
        return int(string)
    except ValueError:
        return 0


def raportit_check_difference_dict_object(raportti_dict, raportti_object):
    return compare_sets((
        (raportti_dict['teksti'], raportti_object.teksti),
        (string_to_float_or_zero(raportti_dict['matkat']), raportti_object.matkat),
        (string_to_float_or_zero(raportti_dict['tunnit']), raportti_object.tunnit),
        (string_to_float_or_zero(raportti_dict['muut']), raportti_object.muut)
    ))


def raportit_new_from_dict(raportti_dict, raportti_id, raportti_date):
    return Paivaraportti(id=int(raportti_id), date=raportti_date,
                         teksti=raportti_dict['teksti'],
                         matkat=string_to_float_or_zero(raportti_dict['matkat']),
                         tunnit=string_to_float_or_zero(raportti_dict['tunnit']),
                         muut=string_to_float_or_zero(raportti_dict['muut']))


def save_paivaraportit(request, tilaus):
    raportit_request = raportit_form_to_dict(request)

    raportit_new = []
    changes_done = False

    for raportti_id, raportti_new in raportit_request.items():
        for raportti_old in tilaus.paivaraportit:
            if int(raportti_old.id) == int(raportti_id):
                if raportit_check_difference_dict_object(raportti_new, raportti_old): # TODO: modify_from_dict()?
                    raportti_old.teksti = raportti_new['teksti']
                    raportti_old.matkat = string_to_float_or_zero(raportti_new['matkat'])
                    raportti_old.tunnit = string_to_float_or_zero(raportti_new['tunnit'])
                    raportti_old.muut = string_to_float_or_zero(raportti_new['muut'])
                    changes_done = True
                raportit_new.append(raportti_old)

    if changes_done:
        tilaus.paivaraportit = raportit_new


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


def tavarat_check_difference_dict_object(tavara_dict, tavara_object):
    return compare_sets((
        (tavara_dict['koodi'], tavara_object.koodi),
        (tavara_dict['nimi'], tavara_object.nimi),
        (tavara_dict['maara'], tavara_object.maara),
        (tavara_dict['hinta'], tavara_object.hinta)
    ))


def tavarat_new_from_dict(tavara_dict, tavara_id=None):
    if tavara_id is None:
        tavara_id = 0
        if DBSession.query(Tavara).count() > 0:
            tavara_id = DBSession.query(Tavara).order_by(Tavara.id.desc()).first().id + 1

    return Tavara(id=tavara_id, date=datetime.datetime.now(),
                  koodi=tavara_dict['koodi'], nimi=tavara_dict['nimi'],
                  maara=string_to_int_or_zero(tavara_dict['maara']), hinta=string_to_float_or_zero(tavara_dict['hinta']),
                  tyyppi=(
                      "" +
                      ('A' if ('A' in tavara_dict.keys()) else '') +
                      ('T' if ('T' in tavara_dict.keys()) else '')
                  )
  )


def save_tavarat(request, tilaus):
    tavarat = tavarat_form_to_dict(request)
    tavarat = remove_empty_tavarat(tavarat)

    tavarat_new = []
    for tavara_id, tavara in tavarat.items():  # Loop throug received list of items
        if 'n' in tavara_id:                        # If 'n' -> we are creating a new item
            tavara_new = tavarat_new_from_dict(tavara)
            DBSession.add(tavara_new)
            tavarat_new.append(tavara_new)
        else:                                       # Else look for an existing one
            for tavara_old in tilaus.tavarat: # TODO: Create modify_from_dict?
                if int(tavara_id) == int(tavara_old.id):
                    tavara_old.koodi = tavara['koodi']
                    tavara_old.nimi = tavara['nimi']
                    tavara_old.maara = string_to_int_or_zero(tavara['maara'])
                    tavara_old.hinta = string_to_float_or_zero(tavara['hinta'])
                    tavara_old.tyyppi = (
                        "" +
                        ('A' if ('A' in tavara.keys()) else '') +
                        ('T' if ('T' in tavara.keys()) else '')
                    )
                    tavarat_new.append(tavara_old)

    tilaus.tavarat = tavarat_new


@view_config(route_name='order_details', renderer='../templates/orders/order_details.pt')
def view_order_details(request):
    order_id = request.matchdict['id']
    tilaus = DBSession.query(Tilaus).filter_by(id=order_id).order_by(Tilaus.uuid.desc()).first()

    if 'data' in request.POST.keys():

        #########################################################
        # Form data sent for updating the basic order information
        #########################################################

        if request.POST['data'] == 'perustiedot':
            tilaus = update_perustiedot(request, tilaus)

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

    # Re-read the order to get possible changes
    tilaus = DBSession.query(Tilaus).filter_by(id=order_id).order_by(Tilaus.uuid.desc()).first()

    for x in tilaus.paivaraportit:
        print(str(x) + ", .date= " + str(x.date))

    return {'tilaus': tilaus, 'current_date': current_date}