from pyramid.view import view_config

@view_config(route_name='login', renderer='../templates/login.pt')
def view_login(request):
    return {}

@view_config(route_name='logout', renderer='../templates/login.pt')
def view_logout(request):
    return {}
