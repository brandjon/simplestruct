"""Demonstrates how to combine Struct with abstract base classes."""

from abc import ABCMeta, abstractmethod
from simplestruct import Struct, Field, MetaStruct


# A simple ABC. Subclasses must provide an override for foo().
class Abstract(metaclass=ABCMeta):
    @abstractmethod
    def foo(self):
        pass

# ABCs rely on a metaclass that conflicts with Struct's metaclass.
try:
    class Concrete(Abstract, Struct):
        f = Field
        def foo(self):
            return self.f ** 2

except TypeError as e:
    print(e)
    # metaclass conflict: the metaclass of a derived class must
    # be a (non-strict) subclass of the metaclasses of all its bases

# So let's make a trivial subclass of ABCMeta and MetaStruct.
class ABCMetaStruct(MetaStruct, ABCMeta):
    pass

class Concrete(Abstract, Struct, metaclass=ABCMetaStruct):
    f = Field
    def foo(self):
        return self.f ** 2

c = Concrete(5)
print(c.foo())      # 25


# For convenience we can make a version of Struct that
# incorporates the common metaclass.
class ABCStruct(Struct, metaclass=ABCMetaStruct):
    pass

# Now we only have to do:
class Concrete(Abstract, ABCStruct):
    f = Field
    def foo(self):
        return self.f ** 2

c = Concrete(5)
print(c.foo())      # 25
