#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014
#

from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
from pyramid.security import authenticated_userid
from ..models import DBSession, User
from datetime import datetime


msg_oldpassword = "Salasanaa ei vaihdettu"
msg_tooshort = "Salanaa ei vaihdettu: Uusi salasana liian lyhyt"
msg_changed = "Salasana vaihdettu"


def change_password(user, newpassword):
    if newpassword == ';notapassword;':
        return msg_oldpassword
    elif len(newpassword) < 5:
        return msg_tooshort

    user.set_password(newpassword)

    return msg_changed


@view_config(route_name='user_profile', renderer='../templates/user_profile.pt')
def view_admin_users(request):
    email = authenticated_userid(request)
    user = DBSession.query(User).filter_by(email=email).order_by(User.uuid.desc()).first()

    if 'data' in request.POST.keys():
        if request.POST['data'] == 'user_info':
            pass # TODO #0182
        if request.POST['data'] == 'user_password':
            msg = change_password(user, request.POST['password']) # TODO #0183
            print(msg)

    if user is None:
        return Response('Virheellinen käyttäjä') # TODO #0181
    return {'user': user}

err_missing_name = "Käyttäjän nimi puuttuu"
err_missing_email = "Käyttäjän sähköpostiosoite puuttuu"
err_missing_pass = "Käyttäjän salasana puuttuu"


"""@view_config(route_name='admin_users_new', renderer='../templates/admin_users_new.pt')
def view_admin_users_new(request):
    errors = ""

    post = request.POST
    keys = list(post.keys())

    if 'data' in keys:
        if not 'name' in keys or len(post['name']) == 0:
            errors += err_missing_name
        if not 'email' in keys or len(post['email']) == 0:
            errors += err_missing_email
        if not 'password' in keys or len(post['password']) == 0:
            errors += err_missing_pass

        if 'admin' in keys:
            admin = True
        else:
            admin = False

        if 'vuosihuoltosopimukset' in keys:
            vhs = True
        else:
            vhs = False

        if not errors:
            next_id = 0
            if DBSession.query(User).count() > 0:
                next_id = DBSession.query(User).order_by(User.id.desc()).first().id+1

            user = User(id=next_id, date=datetime.now(),
                        email=post['email'], name=post['name'],
                        admin=admin, vuosihuoltosopimukset=vhs)
            user.set_password(post['password'])

            DBSession.add(user)

            return HTTPFound(request.route_url('admin_users'))
        else:
            return {'errors': errors}

    return {}


@view_config(route_name='admin_users_edit', renderer='../templates/admin_users_edit.pt')
def view_admin_users_edit(request):
    user = DBSession.query(User).filter_by(id=request.matchdict['id']).order_by(User.date.desc()).first()

    locked = True if user.email == "admin" else False
    return {'user': user, 'locked': locked}"""