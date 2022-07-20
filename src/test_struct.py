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


class TestStruct(unittest.TestCase):
    '''
    Tests struct loader methods.
    '''

    def test_c_struct(self):
        '''
        Tests the c_struct method.
        '''

        expected_struct_str = ""
        expected_struct_str += "typedef struct {\n"
        expected_struct_str += "\tsize_t __size__myStructSize;\n"
        expected_struct_str += "\tunsigned long long id;\n"
        expected_struct_str += "\tchar[80] myCustomClass;\n"
        expected_struct_str += "\tsize_t classBloat;\n"
        expected_struct_str += "\tsize_t secondClassBloat;\n"
        expected_struct_str += "\tfloat price;\n"
        expected_struct_str += "\tchar grade;\n"
        expected_struct_str += "\tstd::string description;\n"
        expected_struct_str += "} myStruct;"

        tmp = StructLoader(yaml_path="../templateYaml.yaml").generate_struct()

        self.assertEqual(tmp.c_struct, expected_struct_str)

    def test_c_struct_head(self):
        '''
        Tests the c_struct_head method.
        '''

        expected_struct_head_str = ""
        expected_struct_head_str += "typedef struct {\n"
        expected_struct_head_str += "\tsize_t __size__myStructSize;\n"
        expected_struct_head_str += "\tunsigned long long id;\n"
        expected_struct_head_str += "\tchar[80] myCustomClass;\n"
        expected_struct_head_str += "\tsize_t classBloat;\n"
        expected_struct_head_str += "\tsize_t secondClassBloat;\n"
        expected_struct_head_str += "\tfloat price;\n"
        expected_struct_head_str += "\tchar grade;\n"
        expected_struct_head_str += "} myStruct;"

        tmp = StructLoader(yaml_path="../templateYaml.yaml").generate_struct()

        self.assertEqual(tmp.c_struct_head, expected_struct_head_str)
