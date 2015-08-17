#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2015
#

import datetime

from pyramid.view import view_config

from tilaushallinta.models import DBSession
from tilaushallinta.models import Tilaaja
from tilaushallinta.models import Kohde
from tilaushallinta.models.huoltosopimus import Huoltosopimus

def update_perustiedot(request, sopimus):
    sopimus_id = request.POST['huoltosopimus_id']
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
    tilaaja.slaskutus = request.POST['tilaaja_slaskutus']


    kohde = DBSession.query(Kohde).filter_by(id=kohde_id).first()

    kohde.nimi = request.POST['kohde_nimi']
    kohde.yritys = request.POST['kohde_yritys']
    kohde.ytunnus = request.POST['kohde_ytunnus']
    kohde.osoite = request.POST['kohde_osoite']
    kohde.postitoimipaikka = request.POST['kohde_postitoimipaikka']
    kohde.postinumero = request.POST['kohde_postinumero']
    kohde.puhelin = request.POST['kohde_puhelin']
    kohde.email = request.POST['kohde_email']

    sopimus.muut_yhteysh = request.POST['muut_yhteysh']

    return sopimus


@view_config(route_name='huoltosopimus_details', renderer='../../templates/huoltosopimus/huoltosopimus_details.pt')
def view_huoltosopimus_details(request):
    sopimus_id = request.matchdict['sopimus']
    sopimus = DBSession.query(Huoltosopimus).filter_by(id=sopimus_id).first()

    if 'data' in request.POST.keys():
        if request.POST['data'] == 'perustiedot':
            update_perustiedot(request, sopimus)

    return {'huoltosopimus': sopimus}
