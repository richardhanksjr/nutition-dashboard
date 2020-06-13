from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class Index(LoginRequiredMixin, TemplateView):
    template_name = 'front_end/index.html'

