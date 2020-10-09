from logging import Logger
from pathlib import Path
from loggerbundle.LoggerFactory import LoggerFactory

class NotebookLoggerFactory:

    def __init__(
        self,
        loggerFactory: LoggerFactory,
    ):
        self.__loggerFactory = loggerFactory

    def create(self, notebookPath: Path) -> Logger:
        notebookName = f'{notebookPath.parent.parent.stem}.{notebookPath.parent.stem}'

        return self.__loggerFactory.create(notebookName)
