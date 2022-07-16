
class CDataTypes:
    '''
    Default data types available in C/C++.
    '''

    flags           =    ['signed', 'unsigned']
    types_dict = {
        'int':           [      1,           1],
        'size_t':        [      0,           0],
        'float':         [      0,           0],
        'double':        [      0,           0],
        'long double':   [      1,           1],
        'short':         [      0,           0],
        'long':          [      1,           1],
        'long long':     [      1,           1],
        'char':          [      1,           1],
        'std_string':    [      0,           0],
    }

    # Generates complete types list
    types_list = []
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
