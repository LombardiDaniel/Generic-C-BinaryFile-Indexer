'''
Here the C data types are described to be used in the rest of the program.
If you have custom data types, you may describe them here. HOWEVER, a custom
import/include directive has not yet been created.
'''



sign_flags =         ['signed', 'unsigned']

types_dict = {
    'int':           [       1,          1],
    'size_t':        [       0,          0],
    'float':         [       0,          0],
    'double':        [       0,          0],
    'long double':   [       1,          1],
    'short':         [       1,          1],
    'long':          [       1,          1],
    'long long':     [       1,          1],
    'char':          [       1,          1],
    'unsigned':      [       0,          0],
    'signed':        [       0,          0],
    'std::string':   [       0,          0], # check `accepted_string_representations` for input options
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
