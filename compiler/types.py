from llvmlite import ir
from .typebase import TypeBase


class Params:
    params = {
        'LIST': 'elements'
    }

    def p_elements(json):
        ...


class Types(TypeBase):
    types = (
        'int',
        'float',
        'double',
        'array'
    )
    

    class t_int:
        def TYPE():
            '''int32'''
            return ir.IntType(32)

    class t_float:
        def TYPE():
            '''float'''
            return ir.FloatType()

    class t_double:
        def TYPE():
            '''double'''
            return ir.DoubleType()

    class t_array:
        '''
        elements
        length
        '''
        @staticmethod
        def TYPE(elements, length):
            '''array'''
            return ir.ArrayType(elements, length)

