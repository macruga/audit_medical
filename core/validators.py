# Custom validator for models fields
# from rest_framework import serializers
import re 
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date

# Validate that value not containing spaces at start or end
def noSpacesStartEnd(value):
    long = len(value)
    first = value[0]
    last = value[long-1]
    if first.isspace() or last.isspace():
        raise ValidationError(
            _('%(value)s No se admiten espacios al inicio o final'),
            params={'value': value},
        )

# Validate that value not containing only letters
def onlyCharacters(value):
    if not value.isalpha():
        raise ValidationError(
            _('%(value)s Solo se admiten letras sin espacios'),
            params={'value': value},
        )

# Validate that value not containing only numbers or letters
def onlyAlphaNumeric(value):
    if not value.isalnum():
        raise ValidationError(
            _('%(value)s Solo se admiten letras y digitos sin espacios'),
            params={'value': value},
        )

# Validate that value not containing only letters and intermediate spaces
def onlyCharactersAndSpaces(value):
    long = len(value)
    if not re.fullmatch(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]{1,"+str(long)+"}", value):
        raise ValidationError(
            _('%(value)s Solo se admiten letras y espacios intermedios'),
            params={'value': value},
        )

# Validate that value not containing only letters and intermediate spaces
def onlyCharactersSpacesAndPunctuation(value):
    long = len(value)
    if not re.fullmatch(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ \-.()]{1,"+str(long)+"}", value):
        raise ValidationError(
            _('%(value)s Solo se admiten letras, espacios intermedios y los siguientes signos de puntuación . - ( )'),
            params={'value': value},
        )

# Validate that value not containing only letters and integers, A-Z and 0-9
def onlyCharactersAndDigits(value):
    long = len(value)
    if not re.fullmatch(r"[A-Z0-9]{1,"+str(long)+"}", value):
        raise ValidationError(
            _('%(value)s Solo se admiten letras en Mayuscula y digitos, sin espacios'),
            params={'value': value},
        )

# Validate that value not containing only digits
def onlyDigits(value):
    if not value.isdigit():
        raise ValidationError(
            _('%(value)s Solo se admiten Digitos sin espacios'),
            params={'value': value},
        )

# Validate that value not containing only digits
def onlyDigitsAndPoints(value):
    long = len(value)
    if not re.fullmatch(r"[0-9.]{1,"+str(long)+"}", value):
        raise ValidationError(
            _('%(value)s Solo se admiten letras en Mayuscula y digitos, sin espacios'),
            params={'value': value},
        )
        
def onlyDigitsAndDash(value):
    long = len(value)
    if not re.fullmatch(r"[0-9 \ -]", value):
        raise ValidationError(
            _('%(value)s Solo se admiten digitos y guiones - sin espacios'),
            params={'value': value},
        )

# Validate that value not containing only digits
def alphaNumericAndSpaces(value):
    long = len(value)
    if not re.fullmatch(r"[0-9A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]{1,"+str(long)+"}", value):
        raise ValidationError(
            _('%(value)s Solo se admiten letras digitos y espacios intermedios'),
            params={'value': value},
        )

#  Validate if the date is not greater than the current date (Only validate date formats)
def currentDate(value):
    dateNow = date.today()
    diff = (dateNow - value).days
    if diff < 0:
        raise ValidationError(
            _('%(value)s No puede ser mayor a la fecha actual'),
            params={'value': value},
        )


# Validate phone numbers
def phoneValidator(value):
    long = len(value)
    if not re.fullmatch(r"[0-9+]{1,"+str(long)+"}", value):
        raise ValidationError(
            _('%(value)s Solo se formato de telefono'),
            params={'value': value},
        )

# Validate date range
# Attrib date_start: date => fecha inicio
#        date_finish: date => fecha fin
def rangeDate( date_start, date_finish ):
    diff = (date_finish - date_start).days
    print(diff)
    return diff  



# Validate that value not containing only letters and integers, A-Z and 0-9
def facturaType(value):
    long = len(value)
    if not re.fullmatch(r"[A-Z0-9 \-]{1,"+str(long)+"}", value):
        raise ValidationError(
            _('%(value)s Solo se admiten letras en Mayuscula y digitos, sin espacios'),
            params={'value': value},
        )  


def rangeDate( date_start, date_finish ):
    # Validate age range
    # Attrib date_start: date => fecha inicio
    #        date_finish: date => fecha fin
    diff = (date_finish - date_start).days
    return diff