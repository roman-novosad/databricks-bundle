from logging import Logger
from pathlib import Path
from databricksbundle.notebook.function.service.ServiceResolverInterface import ServiceResolverInterface
from databricksbundle.notebook.NotebookLoggerFactory import NotebookLoggerFactory

class NotebookLoggerResolver(ServiceResolverInterface):

    def __init__(
        self,
        notebookLoggerFactory: NotebookLoggerFactory,
    ):
        self.__notebookLoggerFactory = notebookLoggerFactory

    def resolve(self, notebookPath: Path) -> Logger:
        return self.__notebookLoggerFactory.create(notebookPath)
