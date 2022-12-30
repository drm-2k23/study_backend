from django.core.validators import RegexValidator

DECIMAL_VALIDATOR = RegexValidator(
    r'^[0-9]{1,}(,[0-9]{3})*(([\\.,]{1}[0-9]*)|())$',
    'Money must be entered in valid format.')
