from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from tasks.urls import PUBLIC_URLS

# Any class which implement __init__() and __call__() of django middleware implementation can be middleware
class AuthenticateAccessMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    # Must return response 
    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view, *view_args, **view_kwargs):
        # Process view is just called before actual view supposed to be called
        # It should either return None (if all normal) or HttpResponse (if you don't want view to be called)
        # when __call__() of middleware called, URL for view hasn't been resolved that time,
        # so request.resolver_match not available that time

        # List of public urls
        public_urls = PUBLIC_URLS

        # Allow view to execute if either user is authenticated or
        # requested url is of Public Pages such as login, regsiter, forgot password etc
        if request.user.is_authenticated or request.resolver_match.url_name in public_urls:
            return None
        else:
            return HttpResponseRedirect(reverse_lazy("tasks:url-login"))