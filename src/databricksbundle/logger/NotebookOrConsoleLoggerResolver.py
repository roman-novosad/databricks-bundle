from logging import Logger
from consolebundle.detector import isRunningInConsole
from databricksbundle.detector import isDatabricks
from databricksbundle.notebook.function.service.NotebookLoggerResolver import NotebookLoggerResolver
from databricksbundle.notebook.NotebookPathResolver import NotebookPathResolver

class NotebookOrConsoleLoggerResolver:

    def __init__(
        self,
        consoleLogger: Logger,
        notebookPathResolver: NotebookPathResolver,
        notebookLoggerResolver: NotebookLoggerResolver,
    ):
        self.__consoleLogger = consoleLogger
        self.__notebookPathResolver = notebookPathResolver
        self.__notebookLoggerResolver = notebookLoggerResolver

    def resolve(self) -> Logger:
        if isDatabricks():
            notebookPath = self.__notebookPathResolver.resolve()
            return self.__notebookLoggerResolver.resolve(notebookPath)

        if isRunningInConsole():
            return self.__consoleLogger

        raise Exception('Not notebook or console')
