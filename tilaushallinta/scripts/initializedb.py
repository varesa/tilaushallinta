#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014
#

import os
import sys
from datetime import datetime
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models import (
    DBSession,
    User,
    Base,
    )


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

    if '<password>' in settings['sqlalchemy.url']:
        with open('dbpassword') as pwd:
            settings['sqlalchemy.url'] = settings['sqlalchemy.url'].replace('<password>', pwd.readline().strip())
    
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    with transaction.manager:
        if DBSession.query(User).count() == 0:
            id = 0
        else:
            id = DBSession.query(User).order_by(User.id.desc()).first().id +1
        if DBSession.query(User).filter_by(name='admin').count() == 0:
            admin = User(id=id, date=datetime.now(),
                         name='Admin', email='admin', admin=True)
            admin.set_password('adminpwd123')
            DBSession.add(admin)
