from django.core.validators import MinLengthValidator, MaxLengthValidator, ValidationError
from django.test import TestCase

from django_cl_patente.fields import CLPatenteField


class CLPatenteFieldTest(TestCase):
    def test_field(self):
        """ Tests that the field validates input"""
        invalid_min_length_data = 'p'
        invalid_max_length_data = 'pcpcpcpc'

        error_invalid = [CLPatenteField().default_error_messages['invalid']]

        error_min_length = [MinLengthValidator.message %
                            {'limit_value': CLPatenteField().min_length,
                             'show_value': len(invalid_min_length_data)}]

        error_max_length = [MaxLengthValidator.message %
                            {'limit_value': CLPatenteField().max_length,
                             'show_value': len(invalid_max_length_data)}]

        valid = {
        # Valid new style
            'rrwr56': 'RRWR-56',
            'rrwr-56': 'RRWR-56',
        # Valid old style
            'aa6056': 'AA-6056',
            'aa-6056': 'AA-6056'
        }
        invalid = {
            invalid_min_length_data: error_min_length,
            invalid_max_length_data: error_max_length,
            'ppppcpc': error_invalid,
            'cpcpcp': error_invalid,
            'cpcpc0': error_invalid,
            'cpc606': error_invalid,
            'c60606': error_invalid,
            '606060': error_invalid,
            # Can't contain 'm'
            'mttt12': error_invalid,
            # Can't contain 'n'
            'nttt34': error_invalid,
            # Can't contain 'q'
            'qttt56': error_invalid,
            # Can't contain vowel
            # 'a'
            'attt67': error_invalid,
            # 'e'
            'ettt67': error_invalid,
            # 'i'
            'ittt89': error_invalid,
            # 'o'
            'ottt01': error_invalid,
            # 'u'
            'uttt23': error_invalid
        }

        for value in valid.keys():
            self.assertEqual(CLPatenteField().clean(value), valid[value])

        for value in invalid.keys():
            self.assertRaises(ValidationError, CLPatenteField().clean, value)
