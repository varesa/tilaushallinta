from pyramid.response import Response
from pyramid.view import view_config

from ..models import DBSession, Tilaaja, Kohde

from .utils import get_latest_ids

@view_config(route_name='json_newest_tilaajat', renderer='json')
def view_newest_tilaajat(request):
    tilaajat = get_latest_ids(DBSession.query(Tilaaja).all())
    tilaajat_list = []

    for tilaaja in tilaajat:
        tilaajat_list.append({'uuid': tilaaja.uuid, 'id': tilaaja.id,
                              'nimi': tilaaja.nimi, 'yritys': tilaaja.yritys, 'ytunnus': tilaaja.ytunnus,
                              'osoite': tilaaja.osoite, 'postinumero': tilaaja.postinumero,
                              'postitoimipaikka': tilaaja.postitoimipaikka,
                              'puhelin': tilaaja.puhelin, 'email': tilaaja.email})
    return tilaajat_list


@view_config(route_name='json_newest_kohteet', renderer='json')
def view_newest_kohteet(request):
    kohteet = get_latest_ids(DBSession.query(Kohde).all())
    kohteet_list = []

    for kohde in kohteet:
        kohteet_list.append({'uuid': kohde.uuid, 'id': kohde.id,
                             'nimi': kohde.nimi, 'yritys': kohde.yritys, 'ytunnus': kohde.ytunnus,
                             'osoite': kohde.osoite, 'postinumero': kohde.postinumero,
                             'postitoimipaikka': kohde.postitoimipaikka,
                             'puhelin': kohde.puhelin, 'email': kohde.email})
    return kohteet_list