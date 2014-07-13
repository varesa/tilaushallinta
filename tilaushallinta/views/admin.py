from pyramid.view import view_config

@view_config(route_name='admin', renderer='../templates/admin.pt')
def view_admin(request):
    return {}

@view_config(route_name='admin_users', renderer='../templates/admin_users.pt')
def view_admin_users(request):
    return {}
