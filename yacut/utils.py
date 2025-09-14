import re
import random
import string

from .models import URLMap

MAX_SHORT_LENGTH = 6


def generate_short_id():
    while True:
        short_id = ''.join(random.choice(string.ascii_letters + string.digits)
                           for _ in range(MAX_SHORT_LENGTH))
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id


def check_short_id(short_id):
    return bool(re.match(r'^[a-zA-Z0-9]+$', short_id))