from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    

    
    def populate_user(self, request, sociallogin, response):
        user = super().populate_user(request, sociallogin, response)
        user.is_active = True  # Automatically activate user
        return user