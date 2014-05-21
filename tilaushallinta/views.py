import datetime

from pyramid.response import Response
from pyramid.view import view_config

from .models import (
    Tilaus,
    Tilaaja,
    Kohde
)

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    )


@view_config(route_name='home', renderer='templates/home.pt')
def view_home(request):
    return {}


@view_config(route_name='tilaukset', renderer='templates/tilaukset_list.pt')
def view_tilaukset_list(request):
    tilaukset = DBSession.query(Tilaus).order_by(Tilaus.uuid.desc()).all()

    latest = []
    lastid = None

    for tilaus in tilaukset:
        if tilaus.id is not lastid:
            latest.append(tilaus)
    return {"tilaukset": latest}


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