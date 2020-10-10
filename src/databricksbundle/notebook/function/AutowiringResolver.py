from typing import List
from injecta.container.ContainerInterface import ContainerInterface
from injecta.dtype.AbstractType import AbstractType
from injecta.dtype.classLoader import loadClass

class AutowiringResolver:

    def __init__(
        self,
        prioritizedServices: List[object],
        container: ContainerInterface
    ):
        self.__prioritizedServices = prioritizedServices or []
        self.__container = container

    def resolve(self, argumentType: AbstractType):
        for prioritizedService in self.__prioritizedServices:
            if prioritizedService.__module__ == argumentType.moduleName and prioritizedService.__class__.__name__ == argumentType.className:
                return prioritizedService

        class_ = loadClass(argumentType.moduleName, argumentType.className) # pylint: disable = invalid-name

        return self.__container.get(class_)
