from django.http import response

def Home(request):
    return response.HttpResponse(f'<h1>{request.user.name()}</h1><a href="/api/v1/googlelogin/">login</a>')