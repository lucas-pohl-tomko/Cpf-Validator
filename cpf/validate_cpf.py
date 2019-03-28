import re

from django.core.validators import EMPTY_VALUES
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _

# error_messages = {
#     'invalid': _("Invalid CPF number."),
#     'digits_only': _("This field requires only numbers."),
#     'max_digits': _("This field requires exactly 11 digits."),
# }


def DV_maker(v):
    if v >= 2:
        return 11 - v
    return 0


def validate_CPF(value):
    
    if value in EMPTY_VALUES:
        return u''
    if not value.isdigit():
        value = re.sub("[-\.]", "", value)
    orig_value = value[:]
    try:
        int(value)
    except ValueError:
        return ' :ops? algo errado, cpf tem apenas Digitos'
    if len(value) != 11:
        return ' :ops? algo errado, cpf tem 11 digitos'
    orig_dv = value[-2:]

    new_1dv = sum([i * int(value[idx]) for idx, i in enumerate(range(10, 1, -1))])
    new_1dv = DV_maker(new_1dv % 11)
    value = value[:-2] + str(new_1dv) + value[-1]
    new_2dv = sum([i * int(value[idx]) for idx, i in enumerate(range(11, 1, -1))])
    new_2dv = DV_maker(new_2dv % 11)
    value = value[:-1] + str(new_2dv)
    if value[-2:] != orig_dv:
        return ' :ops? algo errado,{} eh invalido'.format(value)

    return ' eh Valido'

def gera_CPF(formato=True):
    import random
    cpf = "".join([str(random.randint(0,9))for x in range(9)])
    for i in range(100):
        tentativa = cpf+ str("%02d" %i)
        if validate_CPF(tentativa) == ' eh Valido':
            if formato: return "%s.%s.%s-%s" %(tentativa[0:3],tentativa[3:6],tentativa[6:9],tentativa[9:])
            else: return tentativa

def gera_lista_CPFs(n=10, formato=True):
    cpfs = []
    for i in range(n):
        cpfs.append(gera_CPF(formato))
    return cpfs

# def validate_CNPJ(value):

#     value = str(value)
#     if value in EMPTY_VALUES:
#         return u''
#     if not value.isdigit():
#         value = re.sub("[-/\.]", "", value)
#     orig_value = value[:]
#     try:
#         int(value)
#     except ValueError:
#         raise ValidationError(error_messages['digits_only'])
#     if len(value) > 14:
#         raise ValidationError(error_messages['max_digits'])
#     orig_dv = value[-2:]

#     new_1dv = sum([i * int(value[idx]) for idx, i in enumerate(list(range(5, 1, -1)) + list(range(9, 1, -1)))])
#     new_1dv = DV_maker(new_1dv % 11)
#     value = value[:-2] + str(new_1dv) + value[-1]
#     new_2dv = sum([i * int(value[idx]) for idx, i in enumerate(list(range(6, 1, -1)) + list(range(9, 1, -1)))])
#     new_2dv = DV_maker(new_2dv % 11)
#     value = value[:-1] + str(new_2dv)
#     if value[-2:] != orig_dv:
#         raise ValidationError(error_messages['invalid'])

#     return orig_value
