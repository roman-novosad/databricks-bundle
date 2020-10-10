from pathlib import Path
from injecta.container.ContainerInterface import ContainerInterface
from injecta.dtype.AbstractType import AbstractType
from injecta.parameter.allPlaceholdersReplacer import replaceAllPlaceholders, findAllPlaceholders
from injecta.service.class_.InspectedArgument import InspectedArgument
from databricksbundle.notebook.function.service.AutowiringResolver import AutowiringResolver

class ArgumentResolver:

    def __init__(
        self,
        container: ContainerInterface,
        autowiringResolver: AutowiringResolver,
    ):
        self.__container = container
        self.__autowiringResolver = autowiringResolver

    def resolve(self, functionArgument: InspectedArgument, decoratorArgument, notebookPath: Path):
        argumentType = functionArgument.dtype

        if decoratorArgument is not None:
            if isinstance(decoratorArgument, str):
                output = self.__resolveStringArgument(decoratorArgument)
                return self.__checkType(output, argumentType, functionArgument.name)

            return self.__checkType(decoratorArgument, argumentType, functionArgument.name)

        if functionArgument.hasDefaultValue():
            return self.__checkType(functionArgument.defaultValue, argumentType, functionArgument.name)

        if not argumentType.isDefined():
            raise Exception(f'Argument "{functionArgument.name}" must either have explicit value, default value or typehint defined')

        return self.__autowiringResolver.resolve(functionArgument.dtype, notebookPath)

    def __resolveStringArgument(self, decoratorArgument):
        if decoratorArgument[0:1] == '@':
            return self.__container.get(decoratorArgument[1:])

        matches = findAllPlaceholders(decoratorArgument)

        if not matches:
            return decoratorArgument

        parameters = self.__container.getParameters()

        return replaceAllPlaceholders(decoratorArgument, matches, parameters, decoratorArgument)

    def __checkType(self, value, expectedType: AbstractType, argumentName: str):
        valueTypeStr = value.__class__.__module__ + '.' + value.__class__.__name__
        expectedTypeStr = str(expectedType)

        if expectedType.isDefined() and valueTypeStr != expectedTypeStr:
            expectedTypeStr = expectedTypeStr.replace('builtins.', '')
            valueTypeStr = valueTypeStr.replace('builtins.', '')
            raise Exception(f'Argument "{argumentName}" is defined as {expectedTypeStr}, {valueTypeStr} given instead')

        return value
