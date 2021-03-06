## Using dependencies in pipeline functions

Pipelines functions can be injected with objects defined in the app:

```python
from databricksbundle.pipeline.decorator.loader import dataFrameLoader
from logging import Logger
from pyspark.sql.session import SparkSession

@dataFrameLoader()
def customers_table(spark: SparkSession, logger: Logger):
    logger.info('Reading my_crm.customers')

    return spark.read.table('my_crm.customers')
```

The common objects that can be injected are:

* `spark: SparkSession` (`from pyspark.sql.session import SparkSession`)  
The Databricks spark instance itself.

* `tableNames: TableNames` (`from datalakebundle.table.TableNames import TableNames`)  
The [DataLake bundle](https://github.com/bricksflow/datalake-bundle) 's TableNames object allows you to translate table identifiers to final tables names (prefixed with `dev/test/..`).

* `logger: Logger` (`from logging import Logger`)  
Logger instance for the given pipeline.

### (Expert) Passing explicitly defined services into pipeline functions

Services, which cannot be autowired (= classes with multiple instances), can be injected into the pipeline functions explicitly using the `@serviceName` notation:

```python
from databricksbundle.pipeline.decorator.loader import pipelineFunction

@pipelineFunction('@my.service')
def customers_table(myService: MyClass):
    myService.doSomething()
```

See [Injecta](https://github.com/pyfony/injecta)'s documentation for more details on the syntax.

___

Next section: [Configuring pipelines](configuration.md)
