from pathlib import Path
from typing import List
from inspect import signature as createInspectSignature
from injecta.container.ContainerInterface import ContainerInterface
from injecta.dtype.AbstractType import AbstractType
from injecta.dtype.classLoader import loadClass
from databricksbundle.pipeline.function.service.ServiceResolverInterface import ServiceResolverInterface

class AutowiringResolver:

    def __init__(
        self,
        serviceResolvers: List[ServiceResolverInterface],
        container: ContainerInterface
    ):
        self.__serviceResolvers = serviceResolvers or []
        self.__container = container

    def resolve(self, argumentType: AbstractType, notebookPath: Path):
        for serviceResolver in self.__serviceResolvers:
            signature = createInspectSignature(getattr(serviceResolver, 'resolve'))
            returnAnnotation = signature.return_annotation

            if returnAnnotation.__module__ == argumentType.moduleName and returnAnnotation.__name__ == argumentType.className:
                return serviceResolver.resolve(notebookPath)

        class_ = loadClass(argumentType.moduleName, argumentType.className) # pylint: disable = invalid-name

        return self.__container.get(class_)
