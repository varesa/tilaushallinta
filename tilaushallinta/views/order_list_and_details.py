#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014
#

import datetime

from pyramid.view import view_config
from pyramid.request import Request
from pyramid.response import Response

from ..models import DBSession
from ..models import Tilaaja
from ..models import Kohde
from ..models import Tilaus
from ..models import Tavara
from ..models import Paivaraportti

@view_config(route_name='order_list', renderer='../templates/order_list.pt')
def view_tilaukset_list(request):
    tilaukset = DBSession.query(Tilaus).order_by(Tilaus.uuid.desc()).all()

    latest = []
    lastid = None

    for tilaus in tilaukset:
        if tilaus.id is not lastid:
            latest.append(tilaus)
            lastid = tilaus.id
    latest.reverse()
    return {"tilaukset": latest}

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
        tilaaja = Tilaaja(id=tilaaja_old.id, date=datetime.datetime.now(),
                          nimi=request.POST['tilaaja_nimi'],
                          yritys=request.POST['tilaaja_yritys'],
                          ytunnus=request.POST['tilaaja_ytunnus'],
                          osoite=request.POST['tilaaja_osoite'],
                          postitoimipaikka=request.POST['tilaaja_postitoimipaikka'],
                          postinumero=request.POST['tilaaja_postinumero'],
                          puhelin=request.POST['tilaaja_puh'],
                          email=request.POST['tilaaja_email'])
        DBSession.add(tilaaja)

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
        kohde = Kohde(id=kohde_old.id, date=datetime.datetime.now(),
                      nimi=request.POST['kohde_nimi'],
                      yritys=request.POST['kohde_yritys'],
                      ytunnus=request.POST['kohde_ytunnus'],
                      osoite=request.POST['kohde_osoite'],
                      postitoimipaikka=request.POST['kohde_postitoimipaikka'],
                      postinumero=request.POST['kohde_postinumero'],
                      puhelin=request.POST['kohde_puh'],
                      email=request.POST['kohde_email'])
        DBSession.add(kohde)

    # Check for differences in the "Tilaus" model
    tilaus_old = DBSession.query(Tilaus).filter_by(uuid=tilaus_uuid).first()
    tilaus_differs = compare_sets(
        ((tilaus_old.muut_yhteysh, request.POST['muut_yhteysh']),
         (tilaus_old.tyo, request.POST['tyo']),
         (tilaus_old.maksuaika, request.POST['maksuaika']),
         (tilaus.viitenumero, request.POST['viitenumero']))
    )
    if (tilaaja is not None) or (kohde is not None) or tilaus_differs:
        tilaaja = DBSession.query(Tilaaja).filter_by(id=tilaaja_old.id).order_by(Tilaaja.uuid.desc()).first()
        kohde = DBSession.query(Kohde).filter_by(id=kohde_old.id).order_by(Kohde.uuid.desc()).first()

        tilaus_uusi = Tilaus(id=tilaus_old.id, date=datetime.datetime.now(),
                             tilaaja=tilaaja, kohde=kohde,
                             muut_yhteysh=request.POST['muut_yhteysh'],
                             tyo=request.POST['tyo'],
                             maksuaika=request.POST['maksuaika'],
                             viitenumero=request.POST['viitenumero'],
                             tavarat=tilaus_old.tavarat, paivaraportit=tilaus_old.paivaraportit)
        DBSession.add(tilaus_uusi)

        tilaus = DBSession.query(Tilaus).order_by(Tilaus.uuid.desc()).first()

    return tilaus


def update_paivaraportit(request, tilaus):
    next_id = 0
    if DBSession.query(Paivaraportti).count() > 0:
        next_id = DBSession.query(Paivaraportti).order_by(Paivaraportti.id.desc()).first().id + 1
    tilaus.paivaraportit.append(Paivaraportti(id=next_id, date=datetime.datetime.now(),
                                              teksti=request.POST['kuvaus'],
                                              tunnit=request.POST['tunnit'],
                                              matkat=request.POST['matkat'],
                                              muut=request.POST['muut']))


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
                  maara=tavara_dict['maara'], hinta=tavara_dict['hinta'],
                  tyyppi=(
                      "" +
                      ('A' if ('A' in tavara_dict.keys()) else '') +
                      ('T' if ('T' in tavara_dict.keys()) else '')
                  )
    )


def update_tavarat(request, tilaus):
    tavarat = tavarat_form_to_dict(request)
    tavarat = remove_empty_tavarat(tavarat)

    tavarat_new = []
    for tavara_id, tavara in tavarat.items():  # Loop throug received list of items
        if 'n' in tavara_id:                        # If 'n' -> we are creating a new item
            tavara_new = tavarat_new_from_dict(tavara)
            DBSession.add(tavara_new)
            tavarat_new.append(tavara_new)
        else:                                       # Else look for an existing one
            for tavara_old in tilaus.tavarat:
                if tavara_id == tavara_old.id:
                    if tavarat_check_difference_dict_object(tavara, tavara_old):        # If different -> create new
                        tavara_new = tavarat_new_from_dict(tavara, tavara_id=tavara_id)
                        DBSession.add(tavara_new)
                        tavarat_new.append(tavara_new)
                    else:                                                               # If same -> reuse
                        tavarat_new.append(tavara_old)


    tilaus_uusi = Tilaus(id=tilaus.id, date=datetime.datetime.now(),
                         tilaaja=tilaus.tilaaja, kohde=tilaus.kohde,
                         muut_yhteysh=tilaus.muut_yhteysh,
                         tyo=tilaus.tyo, maksuaika=tilaus.maksuaika,
                         viitenumero=tilaus.viitenumero,
                         tavarat=tavarat_new, paivaraportit=tilaus.paivaraportit)
    DBSession.add(tilaus_uusi)
    import json

    print(json.dumps(tavarat, indent=4))


@view_config(route_name='order_details', renderer='../templates/order_details.pt')
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
            update_paivaraportit(request, tilaus)

        ############################################
        # Form data sent for updating the items list
        ############################################

        if request.POST['data'] == 'tavarat':
            update_tavarat(request, tilaus)

    current_date = datetime.datetime.now()

    # Re-read the order to get possible changes
    tilaus = DBSession.query(Tilaus).filter_by(id=order_id).order_by(Tilaus.uuid.desc()).first()

    return {'tilaus': tilaus, 'tilaus_uuid': tilaus.uuid, 'current_date': current_date}