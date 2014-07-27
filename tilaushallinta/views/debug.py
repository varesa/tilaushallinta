from pyramid.view import view_config

@view_config(route_name='assertfail')
def view_assertfail(request):
    assert False