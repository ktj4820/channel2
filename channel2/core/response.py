from django.http.response import HttpResponse

from channel2.settings import MEDIA_URL, X_ACCEL


class HttpResponseXAccel(HttpResponse):
    """
    This is an Nginx specific response using header 'X-Accel-Redirect'. This
    response will serve static files that are normally protected.
    """

    def __init__(self, file, content_type, name=None, attachment=False):
        super(HttpResponseXAccel, self).__init__(content_type=content_type)

        if X_ACCEL:
            self['X-Accel-Redirect'] = MEDIA_URL + file.name
        else:
            self.status_code = 302
            self['Location'] = file.url

        if not name:
            name = file.name

        self['Content-Disposition'] = '{disposition}; filename="{filename}"'.format(
            disposition=attachment and 'attachment' or 'inline',
            filename=name,
        )
