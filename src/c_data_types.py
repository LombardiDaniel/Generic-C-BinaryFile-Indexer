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
    'short':         [       0,          0],
    'long':          [       1,          1],
    'long long':     [       1,          1],
    'char':          [       1,          1],
    'std_string':    [       0,          0],
}
