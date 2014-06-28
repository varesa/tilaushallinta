import datetime
import os.path

from pyramid.response import Response
from pyramid.request import Request
from pyramid.view import view_config

from pyramid.events import subscriber
from pyramid.events import BeforeRender

from sqlalchemy import Table
from sqlalchemy.exc import NoSuchTableError

from .models import (
    DBSession,
    Base,

    Tilaus,
    Tilaaja,
    Kohde,

    Paivaraportti,
    Tavara
)

from sqlalchemy.exc import DBAPIError

@subscriber(BeforeRender)
def add_login_status(event):
    event['logged_in'] = False

@view_config(route_name='home', renderer='templates/home.pt')
def view_home(request):
    return {}

@view_config(route_name='login', renderer='templates/login.pt')
def view_login(request):
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
    tilaus = DBSession.query(Tilaus).filter_by(id=id).order_by(Tilaus.uuid.desc()).first()

    if 'data' in request.POST.keys():
        if request.POST['data'] == 'perustiedot':
            tilaus_uuid = request.POST['tilaus_uuid']
            tilaaja_uuid = request.POST['tilaaja_uuid']
            kohde_uuid = request.POST['kohde_uuid']

            # Check for differences in "Tilaaja" model

            tilaaja_old = DBSession.query(Tilaaja).filter_by(uuid=tilaaja_uuid).first()
            tilaaja_differs = False
            for val1, val2 in (
                    (tilaaja_old.nimi,request.POST['tilaaja_nimi']),
                    (tilaaja_old.yritys, request.POST['tilaaja_yritys']),
                    (tilaaja_old.osoite1, request.POST['tilaaja_osoite1']),
                    (tilaaja_old.osoite2, request.POST['tilaaja_osoite2']),
                    (tilaaja_old.puhelin, request.POST['tilaaja_puh']),
                    (tilaaja_old.email, request.POST['tilaaja_email'])
            ):
                if val1 != val2:
                    tilaaja_differs = True
            
            tilaaja = None
            if tilaaja_differs:
                tilaaja = Tilaaja(id=tilaaja_old.id, date=datetime.datetime.now(),
                                  nimi=request.POST['tilaaja_nimi'],
                                  yritys=request.POST['tilaaja_yritys'],
                                  osoite1=request.POST['tilaaja_osoite1'],
                                  osoite2=request.POST['tilaaja_osoite2'],
                                  puhelin=request.POST['tilaaja_puh'],
                                  email=request.POST['tilaaja_email'])
                DBSession.add(tilaaja)

            # Check for differences in "Kohde" model

            kohde_old = DBSession.query(Kohde).filter_by(uuid=kohde_uuid).first()
            kohde_differs = False
            for val1, val2 in (
                    (kohde_old.nimi, request.POST['kohde_nimi']),
                    (kohde_old.yritys, request.POST['kohde_yritys']),
                    (kohde_old.osoite1, request.POST['kohde_osoite1']),
                    (kohde_old.osoite2, request.POST['kohde_osoite2']),
                    (kohde_old.puhelin, request.POST['kohde_puh']),
                    (kohde_old.email, request.POST['kohde_email'])
            ):
                if val1 != val2:
                    kohde_differs = True

            kohde = None
            if kohde_differs:
                kohde = Kohde(id=kohde_old.id, date=datetime.datetime.now(),
                              nimi=request.POST['kohde_nimi'],
                              yritys=request.POST['kohde_yritys'],
                              osoite1=request.POST['kohde_osoite1'],
                              osoite2=request.POST['kohde_osoite2'],
                              puhelin=request.POST['kohde_puh'],
                              email=request.POST['kohde_email'])
                DBSession.add(kohde)

            # Check for differences in the "Tilaus" model

            tilaus_old = DBSession.query(Tilaus).filter_by(uuid=tilaus_uuid).first()
            tilaus_differs = False
            for val1, val2 in (
                    (tilaus_old.muut_yhteysh, request.POST['muut_yhteysh']),
                    (tilaus_old.tyo, request.POST['tyo']),
                    (tilaus_old.maksuaika, request.POST['maksuaika'])
            ):
                if val1 != val2:
                    tilaus_differs = True

            if (tilaaja is not None) or (kohde is not None) or tilaus_differs:
                tilaaja = DBSession.query(Tilaaja).filter_by(id=tilaaja_old.id).order_by(Tilaaja.uuid.desc()).first()
                kohde = DBSession.query(Kohde).filter_by(id=kohde_old.id).order_by(Kohde.uuid.desc()).first()

                tilaus_uusi = Tilaus(id=tilaus_old.id, date=datetime.datetime.now(),
                                tilaaja=tilaaja, kohde=kohde,
                                muut_yhteysh=request.POST['muut_yhteysh'],
                                tyo=request.POST['tyo'],
                                maksuaika=request.POST['maksuaika'])
                DBSession.add(tilaus_uusi)

                tilaus = DBSession.query(Tilaus).order_by(Tilaus.uuid.desc()).first()


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


    print(tilaus.muut_yhteysh)
    return {'tilaus': tilaus, 'tilaus_uuid': tilaus.uuid}


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

        maksuaika = None
        if (not 'maksuaika' in request.POST.keys()) or int(request.POST['maksuaika']) != 7:
            maksuaika = 14
        else:
            maksuaika = int(request.POST['maksuaika'])

        tilaus = Tilaus(id=next_id, date=datetime.datetime.now(),
                        tilaaja=tilaaja, kohde=kohde,
                        muut_yhteysh=request.POST['muut_yhteysh'],
                        tyo=request.POST['tyo'],
                        maksuaika=maksuaika)
        DBSession.add(tilaus)

        #return Response(str(request.POST))
        return request.invoke_subrequest(Request.blank('/texts/tilattu'))
    except KeyError:
        return Response("Virheellinen käsiteltäessä lomaketta")

@view_config(route_name='show_text', renderer='templates/show_text.pt')
def show_text(request):
    name = request.matchdict['name']
    if name and len(name) > 0:
        name.replace('..', '')
        filename = 'tilaushallinta/texts/' + name + '.txt'
        if os.path.exists(filename):
            file = open(filename, "r")
            return {'text': file.read()}
    return Response('Virheellinen tiedosto')

@view_config(route_name='db', renderer='templates/db.pt')
def db(request):
    models = []
    for table in Base.metadata.tables.keys():
        count = DBSession.execute(Table(table, Base.metadata, autoload=True).count()).scalar()
        models.append({'name': table, 'count': count})
    return {'models': models}

@view_config(route_name='db_model', renderer='templates/db_model.pt')
def db_model(request):
    try:
        model = request.matchdict['name']

        table = Table(model, Base.metadata, autoload=True)
        select = table.select()

        rows = DBSession.execute(select).fetchall()

        return {'model': model, 'rows': rows}
    except NoSuchTableError:
        return Response("Virheellinen kysely")

@view_config(route_name='db_model_row', renderer='templates/db_model_row.pt')
def db_model_row(request):
    try:
        model = request.matchdict['name']
        id = request.matchdict['id']

        table = Table(model, Base.metadata, autoload=True)
        select = table.select('id='+id)

        rows = DBSession.execute(select).fetchall()

        return {'model': model, 'rows': rows}
    except NoSuchTableError:
        return Response("Virheellinen kysely")
