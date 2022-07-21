'''
Contains the struct loader class.
'''
import yaml

from struct import Struct
from utils import Utils, CDataTypes
from errors import (
    MoreThanOneStructDeclaredError,
    ArraySizeNotRecognizedError,
    CDataTypeNotRecognizedError,
    UnmatchedSizeDirectivesError
)


class StructLoader:
    '''
    StructLoader is responsible for loading the yaml specified C/C++ Struct
    into a manajable python object to be used in the cookiecutter.

    Attributes:
        - self.yaml_path (str) : yaml file path
        - self._struct_dict (dict) : dict loaded directly from yaml_path
        - self.struct (dict) : parsed dict ready to be rendered
        - self.c_struct (str) : redered version of self.struct (keeps name directives
            so that it may be used in the renderer)

    Methods:

    '''

    def __init__(self, yaml_path=None, *args, **kwargs):
        self.yaml_path = yaml_path
        self.struct = {}
        self._struct_dict = {}

        self.__iterator_counter = 0

        if self.yaml_path is None:  # test cases:
            if 'test_struct_dict' in kwargs:
                self._struct_dict = kwargs['test_struct_dict']
                self.parse_struct()
                self.verify_size_logic()

            elif 'test_struct' in kwargs:
                self.struct = kwargs['test_struct']

            return

        # methods run to guarantee user has c_struct ready
        self.__read_yaml()
        self.parse_struct()
        self.verify_size_logic()

    def get_struct_obj(self):
        '''
        Generates the Struct object to be used in the renderer.
        '''

        return Struct(self.struct)

    def generate_struct(self):
        '''
        Generates the Struct object to be used in the renderer.
        '''

        return Struct(self.struct)

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
            for k, v in item.items():
                # k => c data type
                # v => attribute name | list of attributes of that size

                if isinstance(v, list):  # if its a list, key gets passed as size of each element
                    for item_ in v:
                        self.struct['items'].append(
                            {k: item_}
                        )

                elif quant := Utils.is_number(k):  # is a number (ammount of bytes)
                    self.struct['items'].append(
                        {CDataTypes.byte_arr(quant): v}
                    )

                elif std_string := CDataTypes.is_str(k):
                    self.struct['items'].append(
                        {std_string: v}
                    )

                else:  # is a regular str, c data type
                    # removes last 'int' if data type is more complex
                    if len(k) > 4 and k[-3::] == 'int':  # 'unsigned int' -> 'unsigned', etc
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
        Gets the str representation of the parsed struct.

        this:

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
           {'std::string': 'description'}
          ],
        }

        becomes:

        typedef struct {
            size_t size;
            unsigned long long id;
            char[80] myCustomClass;
            size_t classBloat;
            size_t secondClassBloat;
            float price;
            char grade;
            std::string description;
        } myStruct;

        '''

        struct_str = ''

        struct_str += "typedef struct {\n"

        for item in self.struct['items']:
            for type, var_name in item.items():  # should have only one iteration
                struct_str += f"\t{type} {var_name};\n"

        struct_str += "}" + f" {self.struct['name']};"

        return struct_str

    def verify_size_logic(self, test_struct=None):
        '''
        Verifies that for every size directive, there is a variable sized field.

        Input example:
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
               {'std::string': 'description'}
              ],
            }
        '''

        if test_struct is None:
            test_struct = self.struct
        # test_struct = self.struct if test_struct is None else test_struct

        undefined_size_needed = False
        variable_size_field_count = 0
        size_directive_count = 0

        seeking_variable_size = False
        for type, name in test_struct['items'][0].items():  # checks first element
            if CDataTypes.is_struct_size(name):
                undefined_size_needed = True  # User may wish to use field size for faster sequential seek

            if CDataTypes.is_field_size(name):
                seeking_variable_size = True
                size_directive_count += 1

            elif CDataTypes.is_variable_size(type):
                variable_size_field_count += 1

        for item in test_struct['items'][1:]:
            if not seeking_variable_size:
                for type, name in item.items():

                    if CDataTypes.is_field_size(name):
                        seeking_variable_size = True
                        size_directive_count += 1

                    elif CDataTypes.is_variable_size(type):
                        variable_size_field_count += 1

            else:
                for type, name in item.items():
                    seeking_variable_size = False
                    variable_size_field_count += 1
                    if not CDataTypes.is_variable_size(type):
                        raise UnmatchedSizeDirectivesError(
                            'Opened size directives are not closed with correct number of undefined field sizes.',
                            f'Error Found on "{type}": "{name}"'
                        )

        if undefined_size_needed and variable_size_field_count == 0:
            raise UnmatchedSizeDirectivesError(
                'Struct size (__size__) specified on constant size struct.',
                'If this is correct, remove directive from field name.'
            )

    @property
    def c_struct(self):
        '''
        Returns the struct used in the C/C++ program.
        '''

        return self.__str__()

    def __iter__(self):
        return self

    def __next__(self):
        try:
            self.__iterator_counter += 1
            for k, v in self.struct['items'][self.__iterator_counter].items():
                return (k, v)

        except IndexError:
            self.__iterator_counter = 0
            raise StopIteration


# tmp = StructLoader(yaml_path='../templateYaml.yaml')
#
# for type, name in tmp:
#     print(type, name)
