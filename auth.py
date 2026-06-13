import os
import sys


DEFAULT_ADMIN_EMAIL = 'gustavo'
DEFAULT_ADMIN_PASSWORD = '123'


def get_admin_credentials() -> tuple[str, str]:
    email = os.getenv('ADAPTAESCOLA_ADMIN_EMAIL', DEFAULT_ADMIN_EMAIL)
    password = os.getenv('ADAPTAESCOLA_ADMIN_PASSWORD', DEFAULT_ADMIN_PASSWORD)
    return email, password


def get_storage_secret() -> str:
    return os.getenv('ADAPTAESCOLA_STORAGE_SECRET', 'troque-este-segredo-em-producao')


def get_app_port() -> int:
    if len(sys.argv) > 1:
        return int(sys.argv[1])
    return int(os.getenv('ADAPTAESCOLA_PORT', '8080'))
