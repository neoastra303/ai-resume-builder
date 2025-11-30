from allauth.account.adapter import DefaultAccountAdapter
from django.http import HttpResponseRedirect
from django.urls import reverse
from django_otp import user_has_device


class OTPAccountAdapter(DefaultAccountAdapter):
    """
    Custom adapter to enforce 2FA for logged in users
    """
    
    def login(self, request, user):
        """
        Override login to redirect to 2FA setup if user doesn't have 2FA enabled
        """
        super().login(request, user)
        
        # Check if user has 2FA device
        if not user_has_device(user) and not request.session.get('otp_bypass', False):
            # Redirect to 2FA setup
            return HttpResponseRedirect(reverse('two_factor_setup'))
        
        return None