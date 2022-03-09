from django.core.validators import RegexValidator

characters_validator = RegexValidator(
    r'^[-a-zA-Z0-9_]+$',
    'Alphabetic characters, numbers and underscores only'
)


