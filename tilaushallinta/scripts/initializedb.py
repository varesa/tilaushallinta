#
# This source code is licensed under the terms of the
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2015
#

import os
import sys
from datetime import datetime
import transaction

from sqlalchemy import engine_from_config

import db_env

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from tilaushallinta.models import (
    DBSession,
    User,
    Hintaluokka,
    Tavara,
    Base,
    Huolto
    )

from tilaushallinta.models.hintaluokka import HuoltoHintaluokka, LisatoimenpideHintaluokka


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    settings['sqlalchemy.url'] = db_env.substitute(settings['sqlalchemy.url'])
    
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    with transaction.manager:
        # Create admin user if it doesn't exist
        if DBSession.query(User).filter_by(name='admin').count() == 0:
            admin = User(date=datetime.now(),
                         name='Admin', email='admin', admin=True)
            admin.set_password('adminpwd123')
            DBSession.add(admin)

        # Create base rates if they don't exist
        if DBSession.query(Hintaluokka).count() == 0:
            DBSession.add(Hintaluokka(hintaluokka=1, tunnit=1, matkat=1, muut=1))
            DBSession.add(Hintaluokka(hintaluokka=2, tunnit=2, matkat=2, muut=2))
            DBSession.add(Hintaluokka(hintaluokka=3, tunnit=3, matkat=3, muut=3))

        if DBSession.query(HuoltoHintaluokka).count() == 0:
            DBSession.add(HuoltoHintaluokka(hintaluokka=1, ek=1, ke=1, sy=1, tk=1))
            DBSession.add(HuoltoHintaluokka(hintaluokka=2, ek=2, ke=2, sy=2, tk=2))
            DBSession.add(HuoltoHintaluokka(hintaluokka=3, ek=3, ke=3, sy=3, tk=3))

        if DBSession.query(LisatoimenpideHintaluokka).count() == 0:
            DBSession.add(LisatoimenpideHintaluokka(hintaluokka=1, tunnit=1, matkat=1, muut=1))
            DBSession.add(LisatoimenpideHintaluokka(hintaluokka=2, tunnit=2, matkat=2, muut=2))
            DBSession.add(LisatoimenpideHintaluokka(hintaluokka=3, tunnit=3, matkat=3, muut=3))

        # Set units for items that do not have them
        for tavara in DBSession.query(Tavara).all():
            if not tavara.yksikko or not len(tavara.yksikko):
                tavara.yksikko = "kpl"
        
        for huolto in DBSession.query(Huolto).all():
            if not huolto.hintaluokka:
                huolto.hintaluokka = DBSession.query(HuoltoHintaluokka).filter_by(hintaluokka=1).first()
