from django.http.response import HttpResponse
from channel2.settings import MEDIA_URL, X_ACCEL


class HttpResponseXAccel(HttpResponse):
    """
    This is an Nginx specific response using header 'X-Accel-Redirect'. This
    response will serve static files that are normally protected.
    """

    def __init__(self, file, content_type, name=None):
        super(HttpResponseXAccel, self).__init__(content_type=content_type)

        if X_ACCEL:
            self['X-Accel-Redirect'] = MEDIA_URL + file.name
            self['X-Accel-Buffering'] = 'no'
            self['X-Accel-Limit-Rate'] = 2 * 1024 * 1024
        else:
            self.status_code = 302
            self['Location'] = file.url

        if name:
            self['Content-Disposition'] = 'filename="{}"'.format(name)

