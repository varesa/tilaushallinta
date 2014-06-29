from pyramid.view import view_config

@view_config(route_name='home', renderer='../templates/home.pt')
def view_home(request):
    return {}