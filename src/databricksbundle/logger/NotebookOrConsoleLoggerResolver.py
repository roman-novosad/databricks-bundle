from logging import Logger
from consolebundle.detector import isRunningInConsole
from injecta.container.ContainerInterface import ContainerInterface
from databricksbundle.detector import isDatabricks

class NotebookOrConsoleLoggerResolver:

    def __init__(
        self,
        container: ContainerInterface,
    ):
        self.__container = container

    def resolve(self) -> Logger:
        if isDatabricks():
            return self.__container.get('databricksbundle.notebook.logger')

        if isRunningInConsole():
            return self.__container.get('consolebundle.logger')

        raise Exception('Not notebook or console')
