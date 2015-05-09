from django.http.response import HttpResponse

from channel2.settings import X_ACCEL


class HttpResponseXAccel(HttpResponse):
    """
    This is an Nginx specific response using header 'X-Accel-Redirect'. This
    response will serve static files that are normally protected.
    """

    def __init__(self, url, name, content_type, attachment=False):
        super(HttpResponseXAccel, self).__init__(content_type=content_type)

        if X_ACCEL:
            self['X-Accel-Redirect'] = url
        else:
            self.status_code = 302
            self['Location'] = url

        if not name:
            name = name

        self['Content-Disposition'] = '{disposition}; filename="{filename}"'.format(
            disposition=attachment and 'attachment' or 'inline',
            filename=name,
        )
