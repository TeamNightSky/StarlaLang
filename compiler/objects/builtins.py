from .base_object import BaseObject

from functools import partial
from llvmlite import ir


class Int(BaseObject):
    TYPE = lambda : ir.IntType()


class Float(BaseObject):
    TYPE = lambda : ir.FloatType()


class Double(BaseObject):
    TYPE = lambda : ir.DoubleType()


class Char(BaseObject):
    TYPE = lambda : ir.FloatType()


class Array(BaseObject):
    TYPE = lambda arrtype, length : ir.ArrayType(arrtype, length)


class Vector(BaseObject):
    TYPE = lambda vectype, initlen : ir.VectorType(vectype, initlen)


class String(BaseObject):
    TYPE = lambda length : Array.TYPE(Char.TYPE(), length)


class Constant(BaseObject):
    TYPE = lambda subtype : partial(ir.Constant(), subtype())


class Function(BaseObject):
    TYPE = lambda ret_type, param_types: ir.FunctionType(ret_type, param_types)

