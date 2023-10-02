import json

def filter_sensitive(request):
    if "api-access" in request.path:
        return None
    return request