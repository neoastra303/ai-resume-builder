from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import redirect


class RateLimitedLoginView(LoginView):
    """
    Login view
    """
    
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)