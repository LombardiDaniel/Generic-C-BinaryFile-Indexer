'''
Here the C data types are described to be used in the rest of the program.
If you have custom data types, you may describe them here. HOWEVER, a custom
import/include directive has not yet been created.
'''



sign_flags =         ['signed', 'unsigned'] # noqa:

types_dict = {
    'int':           [       1,          1],# noqa:
    'size_t':        [       0,          0],# noqa:
    'float':         [       0,          0],# noqa:
    'double':        [       0,          0],# noqa:
    'long double':   [       1,          1],# noqa:
    'short':         [       1,          1],# noqa:
    'long':          [       1,          1],# noqa:
    'long long':     [       1,          1],# noqa:
    'char':          [       1,          1],# noqa:
    'unsigned':      [       0,          0],# noqa:
    'signed':        [       0,          0],# noqa:
    'std::string':   [       0,          0],# noqa: # check `accepted_string_representations` for input options
}

# used in fields of variable lenght when inputting in yaml
accepted_string_representations = [
    '_',
    '*',
    'std::string',
    'std_string',
    'char *',
    'char*'
]
