from django.conf import settings
from django.core.mail.backends.smtp import EmailBackend as SMTPBackend


class GmailSMTPBackend(SMTPBackend):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('host', settings.EMAIL_HOST)
        kwargs.setdefault('port', settings.EMAIL_PORT)
        kwargs.setdefault('username', settings.DEFAULT_FROM_EMAIL)
        kwargs.setdefault('password', settings.EMAIL_HOST_PASSWORD)  # 16-digit app password
        kwargs.setdefault('use_tls', settings.EMAIL_USE_TLS)
        kwargs.setdefault('fail_silently', False)
        super().__init__(*args, **kwargs)
