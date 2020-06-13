from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from api.forms import NutritionEntryForm


class Index(LoginRequiredMixin, TemplateView):
    template_name = 'front_end/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = NutritionEntryForm
        return context

