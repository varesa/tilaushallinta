import os

from pyramid.view import view_config
from pyramid.response import Response

@view_config(route_name='show_text', renderer='../templates/show_text.pt')
def view_show_text(request):
    name = request.matchdict['name']
    if name and len(name) > 0:
        name.replace('..', '')
        filename = 'tilaushallinta/texts/' + name + '.txt'
        if os.path.exists(filename):
            file = open(filename, "r")
            return {'text': file.read()}
    return Response('Virheellinen tiedosto')