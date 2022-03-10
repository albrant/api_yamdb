import datetime

from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


characters_validator = RegexValidator(
    r'^[-a-zA-Z0-9_]+$',
    'Alphabetic characters, numbers and underscores only'
)


def year_validator(value):
    if value > datetime.datetime.now().year:
        raise ValidationError(
            'Please enter correct year!'
        )
