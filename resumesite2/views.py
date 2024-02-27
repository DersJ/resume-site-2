from django.http import HttpResponse
from django.views.decorators.http import require_GET
import json

@require_GET
def nostr(request):
    response = HttpResponse(json.dumps({ "names": { "anders": "d0ea1c340ebf6464809e91a3a7e5133794c5900a664243442672fea59c84dc37"}}), content_type="application/json")
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET"
    return response
