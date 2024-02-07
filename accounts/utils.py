from django.forms import ValidationError

def validate_phone(phone: str):
    if ' ' in phone:
        raise ValidationError('Номер не может содержать пробелы!')
    if not phone.startswith('+7'):
        raise ValidationError('Неверный формат номера')
    elif len(phone) != 12:
        raise ValidationError('Длина номера должен состоять из 12 цифр')
    else:
        for i in phone[1:]:
            if not i.isdigit():
                raise ValidationError(f'Номер не может включать {i}')


def validate_email(email: str):
    if " " in email:
        raise ValidationError('Нельзя ставить пробелы !')
    if not email.startswith('mar'):
        raise ValidationError('Email должен начинаться на "mar"')
    else:
        print('Error')