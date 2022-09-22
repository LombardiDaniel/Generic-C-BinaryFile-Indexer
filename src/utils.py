'''
Utilities to be used in the rest of the module.
'''

from c_data_types import (
    TYPES_DICT,
    SIGN_FLAGS,
    ACCEPTED_STRING_REPRESENTATIONS,
    STRUCT_SIZE_DIRECTIVE,
    NEXT_FIELD_SIZE_DIRECTIVE,
    C_TYPE_FOR_VARIABLE_SIZE,
    VALID_ENTRY_DIRECTIVE
)


class CDataTypes:
    '''
    Default data types available in C/C++.
    '''

    flags = SIGN_FLAGS
    TYPES_DICT = TYPES_DICT

    # Generates complete types list
    types_list = []  # -> this is the one that will be used
    for k, v in TYPES_DICT.items():
        types_list.append(k)
        for i in range(2):
            if v[i]:
                types_list.append(f'{flags[i]} {k}')

    @staticmethod
    def byte_arr(ammount: int) -> str:
        '''
        Returns the equivalent byte (char[N]) string for the template.
        '''

        return f'char[{ammount}]'

    @staticmethod
    def valid_c_type(type_name: str) -> bool:
        '''
        Validates the type in C/C++ for the cookiecutter.
        '''

        if type_name not in CDataTypes.types_list:
            return False

        return True

    @staticmethod
    def is_str(var_type):
        '''
        Checks that the var_type is a supported variable size field (char arr or std::string)
        Returns the 'std::string' or False.

        Args:
            - var_type (str): str to be checked.
        Returns:
            - var (str | bool): if valid, returns 'std::string' else, returns False
        '''

        if var_type in ACCEPTED_STRING_REPRESENTATIONS:
            return 'std::string'

        return False

    @staticmethod
    def is_size_indicator(field_name):
        '''
        Returns if the field is a size indicator.
        '''

        return (
            field_name.startswith(STRUCT_SIZE_DIRECTIVE) or field_name.startswith(NEXT_FIELD_SIZE_DIRECTIVE)
        )

    @staticmethod
    def is_valid_indicator(field_name):
        '''
        Returns if the field is a size indicator.
        '''

        return field_name.startswith(VALID_ENTRY_DIRECTIVE)

    @staticmethod
    def is_struct_size(field_name):
        '''
        Checks if the field name has the directive to be the struct size.
        '''

        if field_name.startswith(STRUCT_SIZE_DIRECTIVE):
            return True

        return False

    @staticmethod
    def is_field_size(field_name):
        '''
        Checks if the field name has the directive to be a field size.
        '''

        if field_name.startswith(NEXT_FIELD_SIZE_DIRECTIVE):
            return True

        return False

    @staticmethod
    def is_variable_size(field_type):
        '''
        Checks if the field type is the one accepted as variable size.
        '''

        return field_type == C_TYPE_FOR_VARIABLE_SIZE


class Utils:
    '''
    Utilities used in the rest of the module.
    '''

    @staticmethod
    def is_number(string):
        '''
        Checks that the string can be converted into a number (int).
        Returns the number or False.

        Args:
            - string (str): str to be checked.
        Returns:
            - num (int | bool): if conversion was successfull, returns the number
                else, returns False
        '''

        try:
            num = int(string)
            return num
        except ValueError:
            return False

    @staticmethod
    def is_size_indicator(string):
        return string.startswith('__size__') or string.startswith('_size_')
