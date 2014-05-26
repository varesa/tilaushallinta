import datetime

from pyramid.response import Response
from pyramid.view import view_config

from .models import (
    DBSession,

    Tilaus,
    Tilaaja,
    Kohde,

    Paivaraportti,
    Tavara
)

from sqlalchemy.exc import DBAPIError


@view_config(route_name='home', renderer='templates/home.pt')
def view_home(request):
    return {}


@view_config(route_name='order_list', renderer='templates/order_list.pt')
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

@view_config(route_name='order_details', renderer='templates/order_details.pt')
def order_details(request):
    id = request.matchdict['id']
    tilaus = DBSession.query(Tilaus).filter(Tilaus.id == id).order_by(Tilaus.uuid.desc()).first()

    if 'data' in request.POST.keys():
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
    return {'tilaus': tilaus}


@view_config(route_name='tilaus', renderer='templates/tilauslomake.pt')
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
                          osoite1=request.POST['tilaaja_osoite1'],
                          osoite2=request.POST['tilaaja_osoite2'],
                          puhelin=request.POST['tilaaja_puh'],
                          email=request.POST['tilaaja_email'])
        DBSession.add(tilaaja)

        next_id = 0
        if DBSession.query(Kohde).count() > 0:
            next_id = DBSession.query(Kohde).order_by(Kohde.id.desc()).first().id+1

        kohde = Kohde(id=next_id, date=datetime.datetime.now(),
                          nimi=request.POST['kohde_nimi'],
                          yritys=request.POST['kohde_yritys'],
                          osoite1=request.POST['kohde_osoite1'],
                          osoite2=request.POST['kohde_osoite2'],
                          puhelin=request.POST['kohde_puh'],
                          email=request.POST['kohde_email'])
        DBSession.add(kohde)

        next_id = 0
        if DBSession.query(Tilaus).count() > 0:
            next_id = DBSession.query(Tilaus).order_by(Tilaus.id.desc()).first().id+1

        tilaus = Tilaus(id=next_id, date=datetime.datetime.now(),
                        tilaaja=tilaaja, kohde=kohde,
                        muut_yhteysh=request.POST['muut_yhteysh'],
                        tyo=request.POST['tyo'])
        DBSession.add(tilaus)

        return Response(str(request.POST))
    except KeyError:
        return Response("Virheellinen lomake")