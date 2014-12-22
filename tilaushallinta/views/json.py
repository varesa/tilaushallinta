from pyramid.view import view_config

from ..models import DBSession, Tilaaja, Kohde


@view_config(route_name='json_tilaajat', renderer='json')
def view_json_tilaajat(request):
    tilaajat = DBSession.query(Tilaaja).all()
    tilaajat_list = []

    for tilaaja in tilaajat:
        tilaajat_list.append({'id': tilaaja.id,
                              'nimi': tilaaja.nimi, 'yritys': tilaaja.yritys, 'ytunnus': tilaaja.ytunnus,
                              'osoite': tilaaja.osoite, 'postinumero': tilaaja.postinumero,
                              'postitoimipaikka': tilaaja.postitoimipaikka,
                              'puhelin': tilaaja.puhelin, 'email': tilaaja.email})
    return tilaajat_list


@view_config(route_name='json_kohteet', renderer='json')
def view_json_kohteet(request):
    kohteet = []
    if 'tilaaja_id' in request.GET.keys():
        tilaaja = DBSession.query(Tilaaja).filter_by(id=int(request.GET['tilaaja_id'])).first()

        for tilaus in tilaaja.tilaukset:
            if tilaus.kohde not in kohteet:
                kohteet.append(tilaus.kohde)
    else:
        kohteet = DBSession.query(Kohde).all()

    kohteet_list = []
    for kohde in kohteet:
        kohteet_list.append({'id': kohde.id,
                             'nimi': kohde.nimi, 'yritys': kohde.yritys, 'ytunnus': kohde.ytunnus,
                             'osoite': kohde.osoite, 'postinumero': kohde.postinumero,
                             'postitoimipaikka': kohde.postitoimipaikka,
                             'puhelin': kohde.puhelin, 'email': kohde.email})
    return kohteet_list