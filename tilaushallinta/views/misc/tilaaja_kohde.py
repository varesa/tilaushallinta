#
# This source code is licensed under the terms of the
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2016
#

import datetime

from pyramid.response import Response

from tilaushallinta.models import DBSession
from tilaushallinta.models.tilaaja import Tilaaja
from tilaushallinta.models.kohde import Kohde


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
    if prefix == 'kohde':
        object.slaskutus = data[prefix + '_slaskutus']


def get_tilaaja_from_r(request):
    """
    Get a Tilaaja object from a request, either by creating a new object or reusing an existin one
    :param request: Request to extract the parameters from
    :type request: pyramid.request.Request
    :return: Instance of Tilaaja
    :rtype: tilaushallinta.models.tilaaja.Tilaaja
    """
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
    return tilaaja


def get_kohde_from_r(request):
    """
    Get a Kohde object from a request, either by creating a new object or reusing an existin one
    :param request: Request to extract the parameters from
    :type request: pyramid.request.Request
    :return: Instance of Kohde
    :rtype: tilaushallinta.models.Kohde.Kohde
    """
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
                      email=request.POST['kohde_email'],
                      slaskutus=request.POST['kohde_slaskutus'])
        DBSession.add(kohde)
    return kohde
