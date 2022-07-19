'''
Errors for the other modules
'''


class MoreThanOneStructDeclaredError(Exception):
    '''
    To be raised if the user tries to describe more than one struct per yaml file.
    '''


class CDataTypeNotRecognizedError(Exception):
    '''
    To be raised if the user passes an unexpected C/C++ data type.
    '''


class ArraySizeNotRecognizedError(Exception):
    '''
    To be raised if the user does not describe an array correctly.
    '''
