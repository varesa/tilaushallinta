#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014
#

import datetime

from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound


from ..models import DBSession
from ..models import Tilaaja
from ..models import Kohde
from ..models import Tilaus


@view_config(route_name='tilaus', renderer='../templates/tilauslomake.pt')
def view_tilaus(request):
    return {}


@view_config(route_name='tilaus_submit')
def view_tilaus_submit(request):
    try:

        next_id = 0
        if DBSession.query(Tilaaja).count() > 0:
            next_id = DBSession.query(Tilaaja).order_by(Tilaaja.id.desc()).first().id+1

        tilaaja = Tilaaja(id=next_id, date=datetime.datetime.now(),
                          nimi=request.POST['tilaaja_nimi'],
                          yritys=request.POST['tilaaja_yritys'],
                          ytunnus=request.POST['tilaaja_ytunnus'],
                          osoite=request.POST['tilaaja_osoite'],
                          postitoimipaikka=request.POST['tilaaja_postitoimipaikka'],
                          postinumero=request.POST['tilaaja_postinumero'],
                          puhelin=request.POST['tilaaja_puh'],
                          email=request.POST['tilaaja_email'])
        DBSession.add(tilaaja)

        next_id = 0
        if DBSession.query(Kohde).count() > 0:
            next_id = DBSession.query(Kohde).order_by(Kohde.id.desc()).first().id+1

        kohde = Kohde(id=next_id, date=datetime.datetime.now(),
                          nimi=request.POST['kohde_nimi'],
                          yritys=request.POST['kohde_yritys'],
                          ytunnus=request.POST['kohde_ytunnus'],
                          osoite=request.POST['kohde_osoite'],
                          postitoimipaikka=request.POST['kohde_postitoimipaikka'],
                          postinumero=request.POST['kohde_postinumero'],
                          puhelin=request.POST['kohde_puh'],
                          email=request.POST['kohde_email'])
        DBSession.add(kohde)

        next_id = 0
        if DBSession.query(Tilaus).count() > 0:
            next_id = DBSession.query(Tilaus).order_by(Tilaus.id.desc()).first().id+1

        maksuaika = None
        if (not 'maksuaika' in request.POST.keys()) or int(request.POST['maksuaika']) != 7:
            maksuaika = 14
        else:
            maksuaika = int(request.POST['maksuaika'])

        tilaus = Tilaus(id=next_id, date=datetime.datetime.now(),
                        tilaaja=tilaaja, kohde=kohde,
                        muut_yhteysh=request.POST['muut_yhteysh'],
                        tyo=request.POST['tyo'],
                        maksuaika=maksuaika,
                        viitenumero=request.POST['viitenumero'])
        DBSession.add(tilaus)

        #return Response(str(request.POST))
        return HTTPFound('/texts/tilattu')
    except KeyError:
        return Response("Virheellinen käsiteltäessä lomaketta")