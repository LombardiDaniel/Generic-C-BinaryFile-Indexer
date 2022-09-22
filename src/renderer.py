'''
Generates the logic and renders the final C/C++ file.
'''
from os import path, system, makedirs
import resource
import subprocess

import jinja2

from struct import StructLoader, Struct
from errors import (
    DirectoryIsNotTemplateDir
)

# TODO: colocar um mecanismo para conferir os arquivos e diretórios


class Renderer:
    '''
    The renderer class is responsible for parsing all the metadata needed for the
    render, as well as actually rendering the needed C/C++ files.

    Attributes:
        - self.struct (Struct) : struct object that holds C struct and head struct.
        - self.page_size (int) : integer containing system page size in bytes.
        - self.__template_dir (str) : path to the templates directory.
        - self.target_dir (str) : path to the target directory for render.

    Methods:
        - self.render() :
        - self.make() :
    '''

    def __init__(self, struct: Struct, target_dir: str):
        self.struct = struct
        # self.
        self.page_size = resource.getpagesize()  # deprecated
        self.__template_dir = None
        self.target_dir = path.abspath(target_dir)

    def set_template_dir(self, templates_dir):
        '''
        Sets the self.__template_dir attribute, is not allowed to be set more than
        once.

        Args:
            - templates_dir (str) : directory to be set.
        '''

        if self.__template_dir is not None:
            raise DirectoryIsNotTemplateDir(
                'template_dir already set.'
            )

        templates_dir = path.abspath(templates_dir)

        if not path.isdir(self.__template_dir):
            raise DirectoryIsNotTemplateDir(
                f'{self.__template_dir} does not exist.'
            )

        self.__template_dir = templates_dir

    def render(self):
        '''
        Renders the files and copies them to the correct directory.
        '''

    def make(self):
        '''
        Compiles the C/C++ files.
        '''

        if not path.isdir(self.target_dir):
            makedirs(self.target_dir)



        out = subprocess.run(sh_script, shell=True)


    def make(self):
        '''
        Compiles using the subprocess module.
        '''

        if not path.isdir(self.target_dir):
            makedirs(self.target_dir)

        final_command = ''
        final_command += f'cd {self.target_dir} && make indexer'
        final_command += 'make indexer'

        try:
            subprocess.run(
                ['/bin/sh', '-c', final_command],
                check=True
            )
        except subprocess.CalledProcessError as exp:
            click.prompt(f'{exp}::Error in Creating Bucket from pipeline: "{self.pipeline_py}"')

# import subprocess
# out = subprocess.run('ld', shell=True)
# out
