import datetime
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.http.request import QueryDict
import pytz


def startswith(value, s):
    """
    returns if value starts with s, used for menu highlighting
    """

    if not value: return False
    return value.find(s) == 0


def exclude_keys(value, *exclude):
    """
    getquerydict returns a mutable copy of the querydict with exclude values
    removed.
    """

    if not isinstance(value, QueryDict):
        raise RuntimeError("getquerydict should be used with QueryDict instances only (e.g. request.GET)")

    value = value.copy()
    for key in exclude:
        if key in value: del value[key]
    return value


def date(value, format='%Y/%m/%d %H:%M'):
    return value.strftime(format)
