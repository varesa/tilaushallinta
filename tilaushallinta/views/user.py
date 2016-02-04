#
# This source code is licensed under the terms of the
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2016
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


@view_config(route_name='user_profile', renderer='tilaushallinta.templates:user_profile.pt')
def view_admin_users(request):
    email = authenticated_userid(request)
    user = DBSession.query(User).filter_by(email=email).first()

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
