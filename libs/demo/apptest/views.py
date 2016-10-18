from django.shortcuts import render

# Create your views here.
from djangos.decorators import webservice_auth_required
from djangos import CommonStatus, ResponseContext
from djangos.gfw.filter import SensitiveFilter
from form import TestApi


# @webservice_auth_required(assign_list=['channel'], allow_anonymous=True)
def test_api(request):
    form = TestApi(**{
        'name': request.parameters.get('name'),
        'id': request.parameters.get('id'),
        'channel': request.parameters.get('channel')})
    valid = form.validate(quiet=True)
    error = []
    for v in valid:
        error.append(v.reason)

    filter = SensitiveFilter()
    result = filter.check("SB")
    print result
    return ResponseContext()(request, {'error': error}, CommonStatus.SUCCESS)
