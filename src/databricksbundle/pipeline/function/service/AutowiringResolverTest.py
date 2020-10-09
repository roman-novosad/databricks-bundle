import unittest
from logging import getLogger, Logger
from pathlib import Path
from box import Box
from injecta.container.ContainerInterface import ContainerInterface
from injecta.dtype.DType import DType
from databricksbundle.pipeline.function.service.AutowiringResolver import AutowiringResolver
from databricksbundle.pipeline.function.service.ServiceResolverInterface import ServiceResolverInterface
from databricksbundle.spark.ScriptSessionFactory import ScriptSessionFactory

class AutowiringResolverTest(unittest.TestCase):

    def setUp(self):
        class DummyLoggerResolver(ServiceResolverInterface):

            def resolve(self, notebookPath: Path) -> Logger:
                return getLogger('test_logger')

        self.__autowiringResolver = AutowiringResolver(
            [
                DummyLoggerResolver()
            ],
            self.__createDummyContainer()
        )

    def test_resolvedService(self):
        argumentType = DType('logging', 'Logger')

        resolvedLogger = self.__autowiringResolver.resolve(argumentType, Path('.'))

        self.assertIsInstance(resolvedLogger, Logger)
        self.assertEqual('test_logger', resolvedLogger.name)

    def test_generalService(self):
        argumentType = DType(ScriptSessionFactory.__module__, 'ScriptSessionFactory')

        resolvedSparkSessionFactory = self.__autowiringResolver.resolve(argumentType, Path('.'))

        self.assertIsInstance(resolvedSparkSessionFactory, ScriptSessionFactory)

    def __createDummyContainer(self):
        class DummyContainer(ContainerInterface):

            def getParameters(self) -> Box:
                return Box({
                    'name': 'Peter',
                    'surname': 'Novak'
                })

            def get(self, ident):
                if ident == ScriptSessionFactory.__module__ or ident.__module__ == ScriptSessionFactory.__module__:
                    return ScriptSessionFactory()

                raise Exception(f'Unexpected service {ident}')

        return DummyContainer()

if __name__ == '__main__':
    unittest.main()
