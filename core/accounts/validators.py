
import re
from django.core.exceptions import ValidationError

def validate_iranian_phone_number(value):
    pattern = r'^(0)?9\d{9}$'
    if not re.match(pattern, value):
        raise ValidationError('Invalid Iranian phone number')
