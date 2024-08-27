from django.core import signing
from django.conf import settings

def generate_token(attendance_id):
    return signing.dumps(attendance_id, salt=settings.SECRET_KEY)

def validate_token(token):
    try:
        attendance_id = signing.loads(token, salt=settings.SECRET_KEY, max_age=60*60*24*7)  # Token valid for 7 days
        return attendance_id
    except signing.BadSignature:
        return None