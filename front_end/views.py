from django.views.generic.base import TemplateView


class Index(TemplateView):
    template_name = 'front_end/index.html'


class PERatio(TemplateView):
    template_name = 'front_end/snippets/pe_ratio.html'
