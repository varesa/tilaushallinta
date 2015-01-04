#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2015
#

from pyramid.view import view_config
from pyramid.response import Response

from tilaushallinta.models import DBSession, Tilaaja, Kohde


@view_config(route_name='update_tilaaja')
def view_update_tilaaja(request):
    id = request.matchdict['id']
    vals = request.POST

    if id != vals['tilaaja_id']:
        return Response("Error: id mismatch")

    tilaaja = DBSession.query(Tilaaja).filter_by(id=id).first()

    tilaaja.nimi = vals['tilaaja_nimi']
    tilaaja.yritys = vals['tilaaja_yritys']
    tilaaja.ytunnus = vals['tilaaja_ytunnus']
    tilaaja.osoite = vals['tilaaja_osoite']
    tilaaja.postinumero = vals['tilaaja_postinumero']
    tilaaja.postitoimipaikka = vals['tilaaja_postitoimipaikka']
    tilaaja.puhelin = vals['tilaaja_puhelin']
    tilaaja.email = vals['tilaaja_email']

    return Response('Ok')


@view_config(route_name='update_kohde')
def view_update_kohde(request):
    id = request.matchdict['id']
    vals = request.POST

    if id != vals['kohde_id']:
        return Response("Error: id mismatch")

    kohde = DBSession.query(Kohde).filter_by(id=id).first()

    kohde.nimi = vals['kohde_nimi']
    kohde.yritys = vals['kohde_yritys']
    kohde.ytunnus = vals['kohde_ytunnus']
    kohde.osoite = vals['kohde_osoite']
    kohde.postinumero = vals['kohde_postinumero']
    kohde.postitoimipaikka = vals['kohde_postitoimipaikka']
    kohde.puhelin = vals['kohde_puhelin']
    kohde.email = vals['kohde_email']

    return Response('Ok')