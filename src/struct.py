import yaml

from utils import Utils, CDataTypes
from c_data_types import (
    NEXT_FIELD_SIZE_DIRECTIVE,
    STRUCT_SIZE_DIRECTIVE
)
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
        - get_struct_obj() : Returns Struct
        - generate_struct() : Returns Struct
        - __read_yaml() : reads the .yaml file
        - parse_struct() : parses the yaml file into the self.struct attribute
        - verify_struct() : validates C data types
        - verify_size_logic() : verifies the logic for size derivatives

    '''

    @property
    def c_struct(self):
        '''
        Returns the struct used in the C/C++ program.
        '''

        return self.__str__()

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


class Struct:
    '''
    This class is returned by the StructLoader class to be used in the renderer.
    In this Struct Class, we do NOT use dictionaty keys to store information.

    Attributes:
        - self.struct_dict (dict) : dict containing all info, including size directives.
        - self.struct_head (list) : list containing dict of fields excluding first
            variable sized field and others, example:
                {'myStruct':[
                    {'size_t': '__size__myStructSize'},
                    {'std::string': 'description'}
                ]}

                becomes:
                [
                    {
                        'type': size_t,
                        'name': myStructSize
                    }
                ]
        - self.struct_name (str) : name of the struct defined by the user
        - self.struct_head_name (str) : name of the struct head used in the program
        - self.is_variable_size (bool) : True if struct contains a variable size field

    Methods:
        - __fix_dict() : fixes the "keys contain info" problem
        - __get_struct_head() : Gets head of struct until first variable field
        -
    '''

    @property
    def c_struct(self):
        '''
        Returns the struct used in the C/C++ program.
        '''

        return self.__str__()

    @property
    def c_struct_head(self):
        '''
        Returns the head/input struct used in the C/C++ program.
        '''

        struct_str = ''

        struct_str += 'typedef struct {\n'

        for item in self.struct_head:
            struct_str += f"\t{item['type']} {item['name']};\n"

        struct_str += '} ' + f"{self.struct_dict['name']};"

        return struct_str

    @property
    def is_variable_size(self):
        '''
        Returns True if the struct is of variable size.
        '''

        for type, name in self:
            if Utils.is_size_indicator(name):
                return True

        return False

    def __iter__(self):
        return self

    def __next__(self):
        try:
            field = self.struct_dict['fields'][self.__iterator_counter]
            self.__iterator_counter += 1
            return (
                field['type'], field['name']
            )

        except IndexError:
            self.__iterator_counter = 0
            raise StopIteration


    def __init__(self, parsed_struct_as_dict):
        self.__iterator_counter = 0
        self.struct_dict = self.__fix_dict(parsed_struct_as_dict)
        self.struct_head = self.__get_struct_head()
        self.struct_name = self.struct_dict['name']
        self.struct_head_name = f"{self.struct_dict['name']}_HEAD"

    def __fix_dict(self, parsed_struct_as_dict):
        '''
        Fixes the "keys contain info" problem.
        Args:
            - parsed_struct_as_dict (dict) : struct imput from StructParser

        Returns:
            - struct_dict (dict) : dict using "type" and "name" keys for C atributes
        '''

        fields_list = []
        for field in parsed_struct_as_dict['items']:
            for type, name in field.items():
                fields_list.append({
                    'type': type,
                    'name': name
                })

        struct_dict = {
            'name': parsed_struct_as_dict['name'],
            'fields': fields_list
        }

        return struct_dict

    def __get_struct_head(self):
        '''
        Returns part of struct that does NOT have variable size elements.

        Returns list containing dict of fields excluding first
            variable sized field and others, example:
                {'myStruct':[
                    {'size_t': '__size__myStructSize'},
                    {'std::string': 'description'}
                ]}

                becomes:
                [
                    {
                        'type': size_t,
                        'name': myStructSize
                    }
                ]
        '''

        struct_head = []

        for type, name in self:
            if not CDataTypes.is_variable_size(type):
                struct_head.append({
                    'type': type,
                    'name': name
                })

            else:
                return struct_head

        return struct_head

    def __len__(self):
        '''
        Returns the ammount of fields in the struct.
        '''

        return len(self.struct_dict['items'])

    def __str__(self):
        '''
        Gets the str representation of the parsed struct.

        this:

        self.struct_dict = {
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

        for field in self.struct_dict['fields']:
            struct_str += f"\t{field['type']} {field['name']};\n"

        struct_str += "}" + f" {self.struct_dict['name']};"

        return struct_str
