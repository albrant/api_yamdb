from django.core.validators import RegexValidator

characters_validator = RegexValidator(
    r'^[-a-zA-Z0-9_]+$',
    'Please only use alphabetic characters, numbers and underscores'
)

