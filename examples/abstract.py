"""Demonstrates how to combine Struct with abstract base classes."""

from abc import ABCMeta, abstractmethod
from simplestruct import Struct, Field, MetaStruct

class Abstract(metaclass=ABCMeta):
    @abstractmethod
    def foo(self):
        pass

# If we ran this code
#
#     class Concrete(Abstract, Struct):
#         f = Field
#         def foo(self):
#             return self.f ** 2
#
# we would get the following error:
#
#     TypeError: metaclass conflict: the metaclass of a derived class
#     must be a (non-strict) subclass of the metaclasses of all its bases
#
# So let's make a trivial subclass of ABCMeta and MetaStruct.

class ABCMetaStruct(MetaStruct, ABCMeta):
    pass

class Concrete(Abstract, Struct, metaclass=ABCMetaStruct):
    f = Field
    def foo(self):
        return self.f ** 2

c = Concrete(5)
print(c.foo())      # 25

# For convenience we can also do

class ABCStruct(Struct, metaclass=ABCMetaStruct):
    pass

# and then

class Concrete(Abstract, ABCStruct):
    f = Field
    def foo(self):
        return self.f ** 2

c = Concrete(5)
print(c.foo())      # 25
