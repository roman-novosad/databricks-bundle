from logging import Logger
from pathlib import Path
from loggerbundle.LoggerFactory import LoggerFactory

class NotebookLoggerFactory:

    def __init__(
        self,
        notebookPath: Path,
        loggerFactory: LoggerFactory,
    ):
        self.__notebookPath = notebookPath
        self.__loggerFactory = loggerFactory

    def create(self) -> Logger:
        notebookName = f'{self.__notebookPath.parent.parent.stem}.{self.__notebookPath.parent.stem}'

        return self.__loggerFactory.create(notebookName)
