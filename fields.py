from django.core.validators import EMPTY_VALUES
from django.forms import ValidationError
from django.forms.fields import CharField
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_unicode

OLD_CAR_PLATE_STYLE = 0
NEW_CAR_PLATE_STYLE = 1


class CLPatenteField(CharField):
    """
    Chilean "Patente", Placa Patente Field, support old LL-NNNN and new LLLL-NN
    type, where L in new can't be vowel or m,n and q.
    """
    default_error_messages = {
        'invalid': _("Enter a valid Chilean Car Plate."),
    }

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 7
        kwargs['min_length'] = 6
        if not 'label' in kwargs:
            kwargs['label'] = _("Car plate")
        if not 'help_text' in kwargs:
            kwargs['help_text'] = _("Chilean car plate as LL-NNNN or LLLL-NN")

        super(CLPatenteField, self).__init__(*args, **kwargs)

    def clean(self, value):
        """
        Check and clean the field for length and type.
        """
        super(CLPatenteField, self).clean(value)

        if value in EMPTY_VALUES:
            return u''

        value = smart_unicode(value.lower())
        value_length = len(value)

        if self.max_length is not None and value_length > self.max_length:
            raise ValidationError(self.error_messages['max_length'] %
                                  {'max': self.max_length,
                                   'length': value_length})

        if self.min_length is not None and value_length < self.min_length:
            raise ValidationError(self.error_messages['min_length'] %
                                  {'min': self.min_length,
                                   'length': value_length})

        value = self._canonify(value)
        _type = self._algorithm(value)

        if _type not in (OLD_CAR_PLATE_STYLE, NEW_CAR_PLATE_STYLE):
            raise ValidationError(self.error_messages['invalid'])

        return self._format(value.upper(), _type)

    def _algorithm(self, value):
        """
        Takes Car Plate in canonical form and verify if it is valid.
        Returns the type or None if it is not valid.
        """
        import re
        # Old card plate patern
        op = '^[a-z]{2,2}\d{4,4}$'
        op = re.compile(op)
        # New card plate patern
        np = '^[bcdfghjklprstvwxyz]{4,4}\d{2,2}$'
        np = re.compile(np)
        if re.search(op, value):
            return OLD_CAR_PLATE_STYLE
        elif re.search(np, value):
            return NEW_CAR_PLATE_STYLE
        else:
            return None

    def _canonify(self, patente):
        """
        Turns the Car Plate into one normalized format.
        """
        return patente.replace(' ', '').replace('-', '')

    def _format(self, value, _type):
        """
        Formats the Car Plate from canonical form to the common string
        representation. LL-DDDD or LLLL-DD
        """
        if _type == OLD_CAR_PLATE_STYLE:
            return u'-'.join((value[:2], value[2:]))
        if _type == NEW_CAR_PLATE_STYLE:
            return u'-'.join((value[:4], value[4:]))
