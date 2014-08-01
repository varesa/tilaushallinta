#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Author: Esa Varemo
#

from pyramid.view import view_config, forbidden_view_config
from pyramid.security import remember, forget
from pyramid.httpexceptions import HTTPFound
from ..models import DBSession, User

err_no_username = "Anna sähköposti/tunnus\n"
err_no_password = "Anna salasana\n"
err_invalid_login = "Virheellinen sähköposti/salasana\n"

@forbidden_view_config(renderer='../templates/login.pt')
@view_config(route_name='login', renderer='../templates/login.pt', permission='open')
def view_login(request):
    print(request.matched_route)
    errors = ""
    if 'login' in request.POST.keys():
        if not 'email' in request.POST.keys() or len(request.POST['email']) == 0:
            errors += err_no_username
        if not 'password' in request.POST.keys() or len(request.POST['password']) == 0:
            errors += err_no_password

        user = DBSession.query(User).filter_by(email=request.POST['email']).order_by(User.uuid.desc()).first()
        if not user:
            errors += err_invalid_login

            if not user.verify_password(request.POST['password']):
                errors += err_invalid_login

        if not errors:
            headers = remember(request, request.POST['email'])
            return HTTPFound("/", headers=headers)

    return {}

@view_config(route_name='logout')
def view_logout(request):
    headers = forget(request)
    return HTTPFound('/', headers=headers)

