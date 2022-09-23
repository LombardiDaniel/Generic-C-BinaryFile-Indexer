'''
Generates the logic and renders the final C/C++ file.
'''
from os import path, system, makedirs
import os
import resource
import subprocess

from jinja2 import Environment, FileSystemLoader

from struct_loader import StructLoader


class Renderer:
    '''
    The renderer class is responsible for parsing all the metadata needed for the
    render, as well as actually rendering the needed C/C++ files.

    Attributes:
        - self.struct (Struct) : struct object that holds C struct and head struct.
        - self.__template_dir (str) : path to the templates directory.
        - self.target_dir (str) : path to the target directory for render.
        - self.indexer_c_type (str) : C data type of the indexed field.

    Methods:
        - self.render() :
        - self.make() :
    '''

    @staticmethod
    def size_or_size(c_type):
        '''
        returns sizeof() or int(size).
        '''

        if isinstance(c_type, int):
            return c_type

        return f"sizeof({c_type})"

    @staticmethod
    def make_field_name_in_struct(c_type_dict):
        if isinstance(c_type_dict['key'], int):
            return f"char {c_type_dict['value']}[{c_type_dict['key']}]"

        return f"{c_type_dict['key']} {c_type_dict['value']}"

    def __init__(self, struct, indexer_c_type: str, i_index: int, target_dir: str = None):
        self.struct = struct
        self.indexer_c_type = indexer_c_type
        self.__template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates/')
        self.target_dir = target_dir
        self.i_index = i_index

    def render(self, user_file_path, struct_head, indexer_c_name):
        '''
        Renders the files and copies them to the correct directory.
        '''

        env = Environment(loader=FileSystemLoader(self.__template_dir))
        main_template = env.get_template('main_TEMPLATE.cpp.j2')
        env.globals['size_or_size'] = Renderer.size_or_size
        env.globals['make_field_name_in_struct'] = Renderer.make_field_name_in_struct
        rendered_main = main_template.render(
            struct_lst=self.struct['value'],
            indexer_c_type=self.indexer_c_type,
            i_index=self.i_index,
            sum_str=self.get_size_before_index_sum(),
            user_file_path=user_file_path,
            struct_head_lst=struct_head,
            indexer_c_name=indexer_c_name
        )

        with open(os.path.join(self.__template_dir, 'main_rendered.cpp'), 'w', encoding='UTF-8') as file:
            file.write(rendered_main)

    def get_size_before_index_sum(self):
        nw_l = []
        for item in self.struct['value']:
            if not item['value'].startswith('__index__'):
                nw_l.append(str(Renderer.size_or_size(item['key'])))

            else:
                break

        return ' + '.join(nw_l)

    def make(self):
        '''
        Compiles using the subprocess module.
        '''

        final_command = ''
        final_command += f'cd {self.__template_dir} && make indexer'

        try:
            subprocess.run(
                ['/bin/sh', '-c', final_command],
                check=True
            )
        except subprocess.CalledProcessError as exp:
            print('ERROR in compilation')


if __name__ == '__main__':
    pass
