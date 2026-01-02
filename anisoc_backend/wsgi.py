"""
WSGI config for anisoc_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import socket  # <--- 1. Import socket
from django.core.wsgi import get_wsgi_application

# --- 2. PASTE THE IPv4 PATCH HERE ---
# This forces Django to use IPv4 to prevent Gmail timeouts on Railway
try:
    orig_getaddrinfo = socket.getaddrinfo

    def getaddrinfo_ipv4(host, port, family=0, type=0, proto=0, flags=0):
        if family == 0:
            family = socket.AF_INET  # Force IPv4
        return orig_getaddrinfo(host, port, family, type, proto, flags)

    socket.getaddrinfo = getaddrinfo_ipv4
except Exception:
    pass
# ------------------------------------

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anisoc_backend.settings')

application = get_wsgi_application()