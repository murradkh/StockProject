from django.shortcuts import render


def page_not_found(request):
    status_code = 404
    response = render(request, "exception.html", {'error_message': "Page Not Found!", "status_code": status_code})
    response.status_code = status_code
    return response
