from django.middleware.http import ConditionalGetMiddleware
from django.middleware.common import CommonMiddleware

def compat_middleware_factory(klass):
    """
    Class wrapper that only executes `process_response`
    if `streaming` is not set on the `HttpResponse` object.
    Django has a bad habbit of looking at the content,
    which will prematurely exhaust the data source if we're
    using generators or buffers.
    """
    class compatwrapper(klass):
        def process_response(self, req, resp):
            if not hasattr(resp, 'streaming'):
                return klass.process_response(self, req, resp)
            return resp
    return compatwrapper

ConditionalMiddlewareCompatProxy = compat_middleware_factory(ConditionalGetMiddleware)
CommonMiddlewareCompatProxy = compat_middleware_factory(CommonMiddleware)

class ContentTypeMiddleware(object):
    def process_request(self, request):
        if request.method in ('POST', 'PUT') and request.META['CONTENT_TYPE'] > 0:
            request.META['CONTENT_TYPE'] = [c.strip() for c in request.META['CONTENT_TYPE'].split(';')][0]
