'''
Contains the struct loader class.
'''

import yaml

from utils import Utils, CDataTypes
from errors import (
    MoreThanOneStructDeclaredError,
    ArraySizeNotRecognizedError,
    CDataTypeNotRecognizedError
)


class StructLoader:
    '''
    StructLoader is responsible for loading the yaml specified C/C++ Struct
    into a manajable python object to be used in the cookiecutter.
    '''

    def __init__(self, yaml_path=None, **kwargs):
        self.yaml_path = yaml_path
        self.struct = {}
        self._struct_dict = {}

        if self.yaml_path is not None:
            self.__read_yaml()

        elif 'test_struct_dict' in kwargs:
            self._struct_dict = kwargs['test_struct_dict']

        self.parse_struct()


    def __read_yaml(self):
        '''
        Purely loads the yaml into a struct_dict.
        '''

        with open(self.yaml_path, mode='r', encoding='utf-8') as file:
            self._struct_dict = yaml.load(file, Loader=yaml.FullLoader)


    def parse_struct(self):
        '''
        This method is responsible to generate the metadata that will be converted
        to a string to be used in the cookiecutter to create the final C/C++ file.

        Example struct input:
        {'myStruct': [{'size_t': 'size'},
                      {'unsigned long long': 'id'},
                      {80: 'myCustomClass'},
                      {'size_t': ['classBloat', 'secondClassBloat']},
                      {'float': 'price'},
                      {'char': 'grade'},
                      {'std_string': 'description'}]}

        Output of that input struct:
        self.struct = {'name': 'myStruct',
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
        '''

        # TODO: instalar logger

        self.struct = {
            'name': '',
            'items': []
        }

        if len(self._struct_dict) > 1:
            raise MoreThanOneStructDeclaredError

        # We search for the __one and only__ key, that contains the name of the struct
        for k, _ in self._struct_dict.items():
            self.struct['name'] = k

        for item in self._struct_dict[self.struct['name']]:
            for k, v in item.items(): # pylint: disable=C0103
                # k => c data type
                # v => attribute name | list of attributes of that size

                if isinstance(v, list): # if its a list, key gets passed as size of each element
                    for item_ in v:
                        self.struct['items'].append(
                            {k: item_}
                        )

                elif quant := Utils.is_number(k): # is a number (ammount of bytes)
                    self.struct['items'].append(
                        {CDataTypes.byte_arr(quant): v}
                    )

                else: # is a regular str, c data type
                    # removes last 'int' if data type is more complex
                    if len(k) > 4 and k[-3::] == 'int': # 'unsigned int' -> 'unsigned', etc
                        k = k[:-4]

                    self.struct['items'].append(
                        {k: v}
                    )

        StructLoader.verify_struct(self.struct)

        return self.struct


    @staticmethod
    def verify_struct(struct):
        '''
        Iterates through self.struct['items'], checks if the keys are valid data
        types. Also checks if arrays are correctly defined.
        '''

        for item in struct['items']:
            for k, _ in item.items():
                if '[' in k or ']' in k:
                    k, k_other = k.split('[', maxsplit=1)

                    num = k_other.split(']', maxsplit=1)[0]
                    if not Utils.is_number(num):
                        raise TypeError(
                            f'Array size not defined. Could not convert string "{num}" to type int.'
                        )

                    if k_other[-1] != ']':
                        raise ArraySizeNotRecognizedError('"]" not found, check YAML file.')

                if not CDataTypes.valid_c_type(k):
                    raise CDataTypeNotRecognizedError(
                        f'Could not find "{k}" in C/C++ DataType table.'
                    )

        return True


    def __str__(self):
        '''

        self.struct = {
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
        '''

        struct_str = ''

        struct_str += "typedef struct {\n"

        for item in self.struct['items']:
            for type, var_name in item.items(): # should have only one iteration
                struct_str += f"\t{type} {var_name};\n"

        struct_str += "}" + f" {self.struct['name']};"

        return struct_str
