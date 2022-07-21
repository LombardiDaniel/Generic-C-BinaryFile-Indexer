
from utils import Utils, CDataTypes
from c_data_types import (
    NEXT_FIELD_SIZE_DIRECTIVE,
    STRUCT_SIZE_DIRECTIVE
)


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
    '''

    def __init__(self, parsed_struct_as_dict):
        self.__iterator_counter = 0
        self.struct_dict = self.__fix_dict(parsed_struct_as_dict)
        self.struct_head = self.__get_struct_head()
        self.struct_name = self.struct_dict['name']
        self.struct_head_name = f"{self.struct_dict['name']}_HEAD"

    def __fix_dict(self, parsed_struct_as_dict):
        '''
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
