from pyramid.view import view_config

@view_config(route_name='admin', renderer='../templates/admin.pt')
def view_admin(request):
    return {}