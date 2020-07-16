import pytz

from django.utils import timezone


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # TODO change this the timezone from the request
        # https://docs.djangoproject.com/en/3.0/topics/i18n/timezones/
        # tzname = request.session.get('django_timezone')
        tzname = "US/Eastern"
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
        return self.get_response(request)
