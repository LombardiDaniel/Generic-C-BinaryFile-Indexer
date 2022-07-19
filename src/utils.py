'''
Utilities to be used in the rest of the module.
'''

from c_data_types import types_dict, sign_flags, accepted_string_representations


class CDataTypes:
    '''
    Default data types available in C/C++.
    '''

    flags = sign_flags
    types_dict = types_dict

    # Generates complete types list
    types_list = [] # -> this is the one that will be used
    for k, v in types_dict.items():
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

        if var_type in accepted_string_representations:
            return 'std::string'

        return False


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
