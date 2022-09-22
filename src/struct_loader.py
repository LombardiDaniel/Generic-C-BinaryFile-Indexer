import yaml

from utils import Utils


class StructLoader:
    '''

    struct_dict: fixed k, v
    '''

    def __init__(self, yaml_path):
        self.yaml_path = yaml_path
        self._struct_dict_raw = None
        self.i_index = 0

        with open(self.yaml_path, mode='r', encoding='utf-8') as file:
            self._struct_dict_raw = yaml.load(file, Loader=yaml.FullLoader)

        self.struct_dict = Utils.fix_key_values(self._struct_dict_raw)

        for i, item in enumerate(self.struct_dict['value']):
            if isinstance(item, dict):
                self.struct_dict['value'][i] = Utils.fix_key_values(item)
                if self.struct_dict['value'][i]['value'].startswith('__index__'):
                    self.i_index = i

if __name__ == '__main__':
    from pprint import pprint
    a = StructLoader(yaml_path='../templateYaml.yaml')
    pprint(a.struct_dict)
