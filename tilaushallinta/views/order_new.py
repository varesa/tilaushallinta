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


@view_config(route_name='order_new', renderer='../templates/orders/order_new.pt')
def view_order_new(request):
    return {}


@view_config(route_name='order_submit')
def view_order_submit(request):
    try:
        if len(request.POST['tilaaja_id']):
            tilaaja = DBSession.query(Tilaaja).filter_by(id=int(request.POST['tilaaja_id'])).first()
            if not tilaaja:
                return Response('Virhe ladatessa aikaisemman tilauksen tietoja')
        else:
            tilaaja = Tilaaja(date=datetime.datetime.now(),
                              nimi=request.POST['tilaaja_nimi'],
                              yritys=request.POST['tilaaja_yritys'],
                              ytunnus=request.POST['tilaaja_ytunnus'],
                              osoite=request.POST['tilaaja_osoite'],
                              postitoimipaikka=request.POST['tilaaja_postitoimipaikka'],
                              postinumero=request.POST['tilaaja_postinumero'],
                              puhelin=request.POST['tilaaja_puhelin'],
                              email=request.POST['tilaaja_email'])
            DBSession.add(tilaaja)

        if len(request.POST['kohde_id']):
            kohde = DBSession.query(Kohde).filter_by(id=int(request.POST['kohde_id'])).first()
            if not kohde:
                return Response('Virhe ladatessa aikaisemman tilauksen tietoja')
        else:
            kohde = Kohde(date=datetime.datetime.now(),
                          nimi=request.POST['kohde_nimi'],
                          yritys=request.POST['kohde_yritys'],
                          ytunnus=request.POST['kohde_ytunnus'],
                          osoite=request.POST['kohde_osoite'],
                          postitoimipaikka=request.POST['kohde_postitoimipaikka'],
                          postinumero=request.POST['kohde_postinumero'],
                          puhelin=request.POST['kohde_puhelin'],
                          email=request.POST['kohde_email'])
            DBSession.add(kohde)

        maksuaika = None
        if (not 'maksuaika' in request.POST.keys()) or int(request.POST['maksuaika']) != 7:
            maksuaika = 14
        else:
            maksuaika = int(request.POST['maksuaika'])

        tilaus = Tilaus(date=datetime.datetime.now(),
                        tilaaja=tilaaja, kohde=kohde,
                        muut_yhteysh=request.POST['muut_yhteysh'],
                        tyo=request.POST['tyo'],
                        maksuaika=maksuaika,
                        viitenumero=request.POST['viitenumero'])
        DBSession.add(tilaus)

        return HTTPFound('/texts/tilattu')
    except KeyError:
        return Response("Virhe käsiteltäessä lomaketta")