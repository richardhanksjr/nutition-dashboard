from django.http import HttpResponse
from django.views import View
from django.views.generic.base import TemplateView



class TestPath(View):
    def get(self, request):
        return HttpResponse("works")


class PERatio(TemplateView):
    template_name = 'api/snippets/pe_ratio.html'
