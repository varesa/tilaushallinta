#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2015
#

import datetime

from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound


from tilaushallinta.models import DBSession
from tilaushallinta.models import Tilaaja
from tilaushallinta.models import Kohde
from tilaushallinta.models import Tilaus


@view_config(route_name='order_new', renderer='../../templates/orders/order_new.pt')
def view_order_new(request):
    """
    View method that shows the ordering form
    :param request: pyramid request
    :return: None
    """
    return {}


def update_object(prefix, object, data):
    """
    Modify the data of an object from form data
    :param prefix: prefix of the form fields, e.g. tilaaja/kohde
    :type prefix: str
    :param object: object to modify
    :type object: Tilaaja or Kohde
    :param data: form data to pull new values from
    :type data: dict
    :return: None
    """
    object.nimi = data[prefix + '_nimi']
    object.yritys = data[prefix + '_yritys']
    object.ytunnus = data[prefix + '_ytunnus']
    object.osoite = data[prefix + '_osoite']
    object.postitoimipaikka = data[prefix + '_postitoimipaikka']
    object.postinumero = data[prefix + '_postinumero']
    object.puhelin = data[prefix + '_puhelin']
    object.email = data[prefix + '_email']


@view_config(route_name='order_submit')
def view_order_submit(request):
    """
    View method that the ordering form is POSTed to
    :param request: Pyramid request
    :return: None
    """
    try:
        if len(request.POST['tilaaja_id']):  # Reusing existing object
            tilaaja = DBSession.query(Tilaaja).filter_by(id=int(request.POST['tilaaja_id'])).first()
            if not tilaaja:
                return Response('Virhe ladatessa aikaisemman tilauksen tietoja')
            if request.POST['tilaaja_edit'] == '1':  # Edit existing object?
                update_object('tilaaja', tilaaja, request.POST)
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

        if len(request.POST['kohde_id']):  # Reusing existing object
            kohde = DBSession.query(Kohde).filter_by(id=int(request.POST['kohde_id'])).first()
            if not kohde:
                return Response('Virhe ladatessa aikaisemman tilauksen tietoja')
            if request.POST['kohde_edit'] == '1':  # Edit existing object?
                update_object('kohde', kohde, request.POST)
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

        if ('maksuaika' not in request.POST.keys()) or int(request.POST['maksuaika']) != 7:
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