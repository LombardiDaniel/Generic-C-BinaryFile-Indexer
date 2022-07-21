'''
unittests for struct_loader
'''

import unittest

from struct_loader import StructLoader
from errors import (
    CDataTypeNotRecognizedError,
    ArraySizeNotRecognizedError,
    UnmatchedSizeDirectivesError
)


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
                {'size_t': '__size__myStructSize'},
                {'bool': '__valid__isValid'},
                {'unsigned long long': 'id'},
                {'char[80]': 'myCustomClass'},
                {'size_t': 'classBloat'},
                {'size_t': 'secondClassBloat'},
                {'float': 'price'},
                {'char': 'grade'},
                {'std::string': 'description'}
            ],
        }

        self.assertEqual(tmp.parse_struct(), expected_dict)

        raise_CDataTypeNotRecognizedError_dict = {  # noqa: N806
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

        raise_ArraySizeNotRecognizedError_dict = {  # noqa: N806
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

        raise_TypeError_dict = {  # noqa: N806
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

        all_default_data_types_yaml = {  # got from: https://en.wikipedia.org/wiki/C_data_types
            'myStruct': [
                {'char': 'a'},
                {'signed char': 'a'},
                {'unsigned char': 'a'},

                {'short': 'a'},
                {'short int': 'a'},
                {'signed short': 'a'},
                {'signed short int': 'a'},

                {'unsigned short': 'a'},
                {'unsigned short int': 'a'},

                {'signed': 'a'},
                {'signed int': 'a'},
                {'int': 'a'},

                {'unsigned int': 'a'},
                {'unsigned': 'a'},

                {'long': 'a'},
                {'long int': 'a'},
                {'signed long': 'a'},
                {'signed long int': 'a'},

                {'unsigned long int': 'a'},
                {'unsigned long': 'a'},

                {'long long': 'a'},
                {'long long int': 'a'},
                {'signed long long': 'a'},
                {'signed long long int': 'a'},

                {'unsigned long long': 'a'},
                {'unsigned long long int': 'a'},

                {'float': 'a'},

                {'double': 'a'},

                {'long double': 'a'},

                # non defaults:
                {'std::string': 'a'},
            ],
        }

        tmp = StructLoader(
            yaml_path=None,
            test_struct_dict=all_default_data_types_yaml
        )

        self.assertTrue(tmp.verify_struct(tmp.struct))

    def test_str_conversion(self):
        '''
        Tests the __str__() dunder method.
        '''

        expected_struct_str = ""
        expected_struct_str += "typedef struct {\n"
        expected_struct_str += "\tsize_t __size__myStructSize;\n"
        expected_struct_str += "\tbool __valid__isValid;\n"
        expected_struct_str += "\tunsigned long long id;\n"
        expected_struct_str += "\tchar[80] myCustomClass;\n"
        expected_struct_str += "\tsize_t classBloat;\n"
        expected_struct_str += "\tsize_t secondClassBloat;\n"
        expected_struct_str += "\tfloat price;\n"
        expected_struct_str += "\tchar grade;\n"
        expected_struct_str += "\tstd::string description;\n"
        expected_struct_str += "} myStruct;"

        tmp = StructLoader(yaml_path="../templateYaml.yaml")

        self.assertEqual(tmp.__str__(), expected_struct_str)

    def test_verify_size_logic(self):
        '''
        Tests logic for size directives.
        '''

        raise_UnmatchedSizeDirectivesErrorError_dict = {  # noqa: N806
            'name': 'myStruct',
            'items': [
                {'size_t': '__size__size'},
                {'unsigned long long': 'id'},
                {'char[80]': 'myCustomClass'}
            ],
        }

        tmp = StructLoader(test_struct=raise_UnmatchedSizeDirectivesErrorError_dict)

        self.assertRaises(
            UnmatchedSizeDirectivesError,
            tmp.verify_size_logic,
        )

        raise_UnmatchedSizeDirectivesErrorError_dict = {  # noqa: N806
            'name': 'myStruct',
            'items': [
                {'unsigned long long': '_size_sizeOfChar'},
                {'char[80]': 'myCustomClass'}
            ],
        }

        tmp = StructLoader(test_struct=raise_UnmatchedSizeDirectivesErrorError_dict)

        self.assertRaises(
            UnmatchedSizeDirectivesError,
            tmp.verify_size_logic
        )
