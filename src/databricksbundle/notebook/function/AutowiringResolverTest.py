import unittest
from logging import getLogger, Logger
from box import Box
from injecta.container.ContainerInterface import ContainerInterface
from injecta.dtype.DType import DType
from databricksbundle.notebook.function.AutowiringResolver import AutowiringResolver
from databricksbundle.spark.ScriptSessionFactory import ScriptSessionFactory

class AutowiringResolverTest(unittest.TestCase):

    def setUp(self):
        self.__autowiringResolver = AutowiringResolver(
            [
                getLogger('test_logger'),
            ],
            self.__createDummyContainer()
        )

    def test_resolvedService(self):
        argumentType = DType('logging', 'Logger')

        resolvedLogger = self.__autowiringResolver.resolve(argumentType)

        self.assertIsInstance(resolvedLogger, Logger)
        self.assertEqual('test_logger', resolvedLogger.name)

    def test_generalService(self):
        argumentType = DType(ScriptSessionFactory.__module__, 'ScriptSessionFactory')

        resolvedSparkSessionFactory = self.__autowiringResolver.resolve(argumentType)

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
