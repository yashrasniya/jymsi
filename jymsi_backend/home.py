from django.http import response

def Home(request):
    return response.HttpResponse(f'<h1>{request.user.name()}</h1><a href="/accounts/google/login/">login</a>')