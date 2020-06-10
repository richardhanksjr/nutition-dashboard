from django.http import HttpResponse
from django.views import View


class TestPath(View):
    def get(self, request):
        return HttpResponse("works")
