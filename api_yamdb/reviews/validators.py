from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


characters_validator = RegexValidator(
    r'^[-a-zA-Z0-9_]+$',
    'Please only use alphabetic characters, numbers and underscores'
)


def validate_username(usename):
    if usename == 'me':
        raise ValidationError(
            'Нельзя создать пользователя с username "me"'
        )
