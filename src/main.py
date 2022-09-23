import argparse
from os import path

from struct_loader import StructLoader
from renderer import Renderer

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--yaml')
    parser.add_argument('--db')
    args = parser.parse_args()

    loader = StructLoader(args.yaml)
    renderer = Renderer(
        loader.struct_dict,
        loader.indexer_c_type,
        loader.i_index,
    )

    renderer.render(args.db, loader.struct_head, loader.indexer_c_name)

    renderer.make()

# python main.py --yaml ../templateYaml.yaml --db /Users/daniellombardi/Desktop/UFSCar/_current.nosync/ORI/TRAB/Generic-C-BinaryFile-Indexer/descricao.txt
