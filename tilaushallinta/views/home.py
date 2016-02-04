#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2016
#

from pyramid.view import view_config


@view_config(route_name='home', renderer='tilaushallinta.templates:home.pt', permission='open')
def view_home(request):
    return {}
