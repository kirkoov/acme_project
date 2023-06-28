from datetime import date

from django.core.exceptions import ValidationError


def real_age(value: date) -> None:
    age = (date.today() - value).days / 365
    if age < 1 or age > 220:  # For the artists' pix sake
        raise ValidationError('Ожидается возраст от 1 года до 220 лет')
