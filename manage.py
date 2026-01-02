#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import socket  # <--- 1. Import socket

# --- 2. THIS BLOCK TO FORCE IPV4 ---
# This forces Django to use IPv4 (Standard Internet) instead of IPv6
# to prevent Gmail timeouts on Railway.
try:
    orig_getaddrinfo = socket.getaddrinfo

    def getaddrinfo_ipv4(host, port, family=0, type=0, proto=0, flags=0):
        if family == 0:
            family = socket.AF_INET  # Force IPv4
        return orig_getaddrinfo(host, port, family, type, proto, flags)

    socket.getaddrinfo = getaddrinfo_ipv4
except Exception:
    pass
#---------------------------------------------------


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anisoc_backend.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
