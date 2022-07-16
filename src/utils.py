
class CDataTypes:
    '''
    Default data types available in C/C++.
    '''

    int = 'int'
    float = 'float'
    double = 'double'
    long = 'long'
    char = 'char'


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

        if type_name not in vars():
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
