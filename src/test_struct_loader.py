'''
unittests for struct_loader
'''

import unittest

from struct_loader import StructLoader
from errors import CDataTypeNotRecognizedError, ArraySizeNotRecognizedError


class TestStructLoader(unittest.TestCase):
    '''
    Tests struct loader methods.
    '''

    def test_parse_struct(self):
        '''
        Tests using the templateYaml.yaml
        '''

        tmp = StructLoader(yaml_path="../templateYaml.yaml")

        expected_dict = {
            'name': 'myStruct',
            'items': [
                {'size_t': 'size'},
                {'unsigned long long': 'id'},
                {'char[80]': 'myCustomClass'},
                {'size_t': 'classBloat'},
                {'size_t': 'secondClassBloat'},
                {'float': 'price'},
                {'char': 'grade'},
                {'std_string': 'description'}
            ],
        }

        self.assertEqual(tmp.parse_struct(), expected_dict)


        raise_CDataTypeNotRecognizedError_dict = { # pylint: disable=C0103
            'name': 'myStruct',
            'items': [
                {'NOT_A_C_DATA_TYPE': 'size'},
                {'unsigned long long': 'id'},
                {'char[80]': 'myCustomClass'}
            ],
        }

        self.assertRaises(
            CDataTypeNotRecognizedError,
            StructLoader.verify_struct,
            raise_CDataTypeNotRecognizedError_dict
        )

        raise_ArraySizeNotRecognizedError_dict = { # pylint: disable=C0103
            'name': 'myStruct',
            'items': [
                {'size_t': 'size'},
                {'unsigned long long': 'id'},
                {'char[80': 'myCustomClass'}
            ],
        }

        self.assertRaises(
            ArraySizeNotRecognizedError,
            StructLoader.verify_struct,
            raise_ArraySizeNotRecognizedError_dict
        )

        raise_TypeError_dict = { # pylint: disable=C0103
            'name': 'myStruct',
            'items': [
                {'size_t': 'size'},
                {'unsigned long long': 'id'},
                {'char[NOT_A_VALID_INT]': 'myCustomClass'}
            ],
        }

        self.assertRaises(
            TypeError,
            StructLoader.verify_struct,
            raise_TypeError_dict
        )
