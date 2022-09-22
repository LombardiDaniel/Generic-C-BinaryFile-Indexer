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
    def char_arr_if_int(c_type):
        if isinstance(c_type, int):
            return f'char[{c_type}]'

    def __init__(self, struct, indexer_c_type: str, i_index: int, target_dir: str):
        self.struct = struct
        self.indexer_c_type = indexer_c_type
        self.__template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates/')
        self.target_dir = path.abspath(target_dir)
        self.i_index = i_index

    def render(self):
        '''
        Renders the files and copies them to the correct directory.
        '''

        env = Environment(loader=FileSystemLoader(self.__template_dir))
        main_template = env.get_template('main_TEMPLATE.cppp.j2')
        env.globals['size_or_size'] = Renderer.size_or_size
        env.globals['char_arr_if_int'] = Renderer.char_arr_if_int
        rendered_main = main_template.render(
            struct_lst=self.struct['value'],
            indexer_c_type=self.indexer_c_type,
            i_index=self.i_index,
            sum_str=self.get_size_before_index_sum()
        )

        with open(os.path.join(self.__template_dir, 'main.cpp'), 'w', encoding='UTF-8') as file:
            file.write(rendered_main)

    def get_size_before_index_sum(self):
        nw_l = []
        for item in self.struct['value']:
            if not item['value'].startswith('__index__'):
                nw_l.append(Renderer.size_or_size(item['key']))

        return ' + '.join(nw_l)

    def make(self):
        '''
        Compiles using the subprocess module.
        '''

        if not path.isdir(self.target_dir):
            makedirs(self.target_dir)

        final_command = ''
        final_command += f'cd {self.target_dir} && make indexer'

        try:
            subprocess.run(
                ['/bin/sh', '-c', final_command],
                check=True
            )
        except subprocess.CalledProcessError as exp:
            print('ERROR in compilation')
