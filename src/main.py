from os import path
import click

from struct_loader import StructLoader

# @click.group()
# def loader_cli():
#     pass


# @loader_cli.command()
@click.command()
@click.argument('yaml_path', type=click.Path(exists=True))
@click.option('-v', '--verbose', is_flag=True, default=False)
def load_struct(yaml_path, verbose):
    '''
    Loads and parses the struct.

    Args:
        - yaml_path (str): path to the yaml struct configuration file.
    '''
    yaml_path = path.abspath(yaml_path)

    if verbose:
        click.echo(f'Loading YAML file from: "{yaml_path}"')

    struct = StructLoader(yaml_path).generate_struct()

    if verbose:
        click.echo('\nStruct:\n')
        click.echo(struct.c_struct)

        click.echo('\nStruct Head:\n')
        click.echo(struct.c_struct_head)





# loader_cli.add_command(load_struct)

if __name__ == '__main__':
    load_struct()
# python main.py "../templateYaml.yaml" -v
