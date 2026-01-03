#for templates .env access of frontend url
from django.conf import settings

def global_settings(request):
    # This makes FRONTEND_URL available in all templates
    return {
        'FRONTEND_URL': settings.FRONTEND_URL
    }