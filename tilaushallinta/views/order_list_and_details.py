#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Author: Esa Varemo
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

@view_config(route_name='order_details', renderer='../templates/order_details.pt')
def view_order_details(request):
    id = request.matchdict['id']
    tilaus = DBSession.query(Tilaus).filter_by(id=id).order_by(Tilaus.uuid.desc()).first()

    if 'data' in request.POST.keys():
        if request.POST['data'] == 'perustiedot':
            tilaus_uuid = request.POST['tilaus_uuid']
            tilaaja_uuid = request.POST['tilaaja_uuid']
            kohde_uuid = request.POST['kohde_uuid']

            # Check for differences in "Tilaaja" model

            tilaaja_old = DBSession.query(Tilaaja).filter_by(uuid=tilaaja_uuid).first()
            tilaaja_differs = compare_sets(
                ((tilaaja_old.nimi, request.POST['tilaaja_nimi']),
                (tilaaja_old.yritys, request.POST['tilaaja_yritys']),
                (tilaaja_old.osoite1, request.POST['tilaaja_osoite1']),
                (tilaaja_old.osoite2, request.POST['tilaaja_osoite2']),
                (tilaaja_old.puhelin, request.POST['tilaaja_puh']),
                (tilaaja_old.email, request.POST['tilaaja_email']))
            )
            
            tilaaja = None
            if tilaaja_differs:
                tilaaja = Tilaaja(id=tilaaja_old.id, date=datetime.datetime.now(),
                                  nimi=request.POST['tilaaja_nimi'],
                                  yritys=request.POST['tilaaja_yritys'],
                                  osoite1=request.POST['tilaaja_osoite1'],
                                  osoite2=request.POST['tilaaja_osoite2'],
                                  puhelin=request.POST['tilaaja_puh'],
                                  email=request.POST['tilaaja_email'])
                DBSession.add(tilaaja)

            # Check for differences in "Kohde" model

            kohde_old = DBSession.query(Kohde).filter_by(uuid=kohde_uuid).first()
            kohde_differs = compare_sets(
                ((kohde_old.nimi, request.POST['kohde_nimi']),
                (kohde_old.yritys, request.POST['kohde_yritys']),
                (kohde_old.osoite1, request.POST['kohde_osoite1']),
                (kohde_old.osoite2, request.POST['kohde_osoite2']),
                (kohde_old.puhelin, request.POST['kohde_puh']),
                (kohde_old.email, request.POST['kohde_email']))
            )

            kohde = None
            if kohde_differs:
                kohde = Kohde(id=kohde_old.id, date=datetime.datetime.now(),
                              nimi=request.POST['kohde_nimi'],
                              yritys=request.POST['kohde_yritys'],
                              osoite1=request.POST['kohde_osoite1'],
                              osoite2=request.POST['kohde_osoite2'],
                              puhelin=request.POST['kohde_puh'],
                              email=request.POST['kohde_email'])
                DBSession.add(kohde)

            # Check for differences in the "Tilaus" model

            tilaus_old = DBSession.query(Tilaus).filter_by(uuid=tilaus_uuid).first()
            tilaus_differs = compare_sets(
                ((tilaus_old.muut_yhteysh, request.POST['muut_yhteysh']),
                (tilaus_old.tyo, request.POST['tyo']),
                (tilaus_old.maksuaika, request.POST['maksuaika']))
            )

            if (tilaaja is not None) or (kohde is not None) or tilaus_differs:
                tilaaja = DBSession.query(Tilaaja).filter_by(id=tilaaja_old.id).order_by(Tilaaja.uuid.desc()).first()
                kohde = DBSession.query(Kohde).filter_by(id=kohde_old.id).order_by(Kohde.uuid.desc()).first()

                tilaus_uusi = Tilaus(id=tilaus_old.id, date=datetime.datetime.now(),
                                tilaaja=tilaaja, kohde=kohde,
                                muut_yhteysh=request.POST['muut_yhteysh'],
                                tyo=request.POST['tyo'],
                                maksuaika=request.POST['maksuaika'])
                DBSession.add(tilaus_uusi)

                tilaus = DBSession.query(Tilaus).order_by(Tilaus.uuid.desc()).first()


        if request.POST['data'] == 'paivaraportti':
            next_id = 0
            if DBSession.query(Paivaraportti).count() > 0:
                next_id = DBSession.query(Paivaraportti).order_by(Paivaraportti.id.desc()).first().id+1

            tilaus.paivaraportit.append(Paivaraportti(id=next_id, date=datetime.datetime.now(),
                                                      teksti=request.POST['kuvaus'],
                                                      tunnit=request.POST['tunnit'],
                                                      matkat=request.POST['matkat'],
                                                      muut=request.POST['muut']))
        if request.POST['data'] == 'tavara':
            next_id = 0
            if DBSession.query(Tavara).count() > 0:
                next_id = DBSession.query(Tavara).order_by(Tavara.id.desc()).first().id+1
            tilaus.tavarat.append(Tavara(id=next_id, date=datetime.datetime.now(),
                                         koodi=request.POST['koodi'],
                                         nimi=request.POST['nimi'],
                                         tyyppi="" +
                                                ('A' if ('A' in request.POST.keys()) else '') +
                                                ('T' if ('T' in request.POST.keys()) else ''),
                                         maara=request.POST['maara']))

    current_date = datetime.datetime.now()

    return {'tilaus': tilaus, 'tilaus_uuid': tilaus.uuid, 'current_date': current_date}