import yaml

from utils import Utils, CDataTypes
from errors import MoreThanOneStructDeclared



class StructLoader:
    '''
    StructLoader is responsible for loading the yaml specified C/C++ Struct
    into a manajable python object to be used in the cookiecutter.
    '''

    def __init__(self, yaml_path):
        self.yaml_path = yaml_path
        self.struct = {}
        self._struct_dict = {}

        self.__read_yaml()
        self.parse_struct()


    def __read_yaml(self):
        '''
        Purely loads the yaml into a struct_dict.
        '''

        with open(self.yaml_path, mode='r', encoding='utf-8') as file:
            self._struct_dict = yaml.load(file, Loader=yaml.FullLoader)


    def parse_struct(self):
        '''
        '''

        # TODO: precisa criar metodo pra garantir que sao tipos existentes em C
        # TODO: instalar logger
        # TODO: comentar essa gorororba ai de baixo

        self.struct = {
            'name': '',
            'items': []
        }

        if len(self._struct_dict) > 1:
            raise MoreThanOneStructDeclared

        for k, _ in self._struct_dict.items():
            self.struct['name'] = k

        for item in self._struct_dict[self.struct['name']]:
            for k, v in item.items(): # noqua:C0103 # pylint: disable=C0103
                if isinstance(v, list): # if its a list, key gets passed as size of each element
                    for item_ in v:
                        self.struct['items'].append(
                            {k: item_}
                        )
                else:
                    if quant := Utils.is_number(k):
                        self.struct['items'].append(
                            {CDataTypes.byte_arr(quant): v}
                        )

                    else:
                        self.struct['items'].append(
                            {k: v}
                        )

        return self.struct
