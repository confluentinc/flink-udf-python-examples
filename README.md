# Example Apache Flink® Python User Defined Functions on Confluent Cloud

This repository contains example Python UDFs packaged for Confluent
Cloud.

Please install [uv](https://docs.astral.sh/uv/) to work with the
examples in this repo.


## Creating from Scratch

The process for making a new UDF Python project using
[uv](https://docs.astral.sh/uv/) is as follows. This is if you want to
make a new repository, if you want to modify this repository in-place,
you can skip to [Writing UDFs](#writing-udfs).


### Init Repo

Create a new "library" project with your desired name and Python
version. Only Python versions 3.10-3.11 are currently supported.

```shell
$ uv init -p 3.11 --lib example_udf
$ cd example_udf
```


### Add Environment Constraints

Append this to `example_udf/pyproject.toml`. This ensures that your
local dependencies are compatible with those available in the
Confluent Cloud environment.

TODO: Add a link to the constantly updated constraint list.

```toml
[tool.uv]
constraint-dependencies = [
    "apache-flink==2.0.0",
    "click>=8.2.0",
    "confluent-function-runtime-core>=0.181.0",
    "grpc-interceptor>=0.15.0",
    "grpcio-health-checking>=1.65.0",
    "grpcio-reflection>=1.65.0",
    "grpcio>=1.65.0",
    "protobuf>=5.29.1",
    "psutil>=5.9.0",
    "pyparsing>=3.2.5",
    "typing_extensions>=4.4.0",
]
```


### Add User Dependencies

Add any Python dependencies you need. You will always need to add
`apache-flink` to have access to the [PyFlink UDF
API](https://nightlies.apache.org/flink/flink-docs-release-2.1/docs/dev/python/table/udfs/overview/).

```shell
example_udf $ uv add apache-flink grpcio
```

uv will find a version which works with the runtime constraints and
will error out if it cannot reconcile the two.


### Add Modules and Define UDFs

Add your UDF code within the `example_udf/src/example_udf/`. This is a
standard Python module, so make as much nested structure as you need.

A single UDF function can go in
`example_udf/src/example_udf/__init__.py`, but you can create as much
module structure as you want.

In this repo, we have a buffet of example UDF types in the
[`src/example_udf`](src/example_udf) directory, separated out by UDF
shape. (E.g. scalars in
[`src/example_udf/scalar.py`](src/example_udf/scalar.py).


## Writing UDFs

See the [Apache Flink
Documentation](https://nightlies.apache.org/flink/flink-docs-release-2.0/docs/dev/python/table/udfs/overview/)
for the Flink Python UDF API. Confluent Cloud supports that API.

A quick summary:

Write your UDF logic first as a separate bare Python function with
type annotations.

```python
def _f_int_add(i: int, j: int) -> int:
    return i + j
```

Then prepare `pyflink.table.types.DataType`s defining the SQL types of
the arguments and return value of your UDF. Then call
`pyflink.table.udf.udf` to create the UDF and save the UDF in a global
variable.


```python
_int_add_inp_types: list[DataType] = [
    DataTypes.INT(nullable=False),
    DataTypes.INT(nullable=False),
]
int_add = udf(
    _f_int_add,
    input_types=_int_add_inp_types,
    result_type=DataTypes.INT(nullable=False),
)
```

This two part definition allows you to easily unit test the function
locally first without loading it into Confluent Cloud or a Flink
environment.

The **qualified name** (import path and variable name) of the result
of `udf` will be the way you reference that specific UDF in Flink SQL
in Confluent Cloud. E.g. in this example repo, there is a UDF located
in the [`src/example_udf/scalar.py`](src/example_udf/scalar.py) module
named `int_add`; this results in a qualified name of
`example_udf.scalar.int_add`.


## Local Testing

You should test your UDF against known values locally via unit tests
first. You can call the bare Python function with example values and
assert the return value.

```python
from example_udf.scalar import _f_int_add


def test_int_add() -> None:
    found = _f_int_add(1, 2)
    assert found == 3
```

[pytest](https://docs.pytest.org/en/stable/) is the de-facto Python
test running framework. You can use it to run the example unit tests
of the example UDFs in this repo.

```shell
example_udf $ uv run pytest tests/test_scalar.py
example_udf $ uv run pytest
```

There is further information in the [testing instructions in the
PyFlink
documentation](https://nightlies.apache.org/flink/flink-docs-release-2.0/docs/dev/python/table/udfs/overview/#testing-user-defined-functions).


## Deployment

Once you have updated your UDF code and you would like to deploy it.

### Create Zip

A **source distribution** (sdist) in zip format is the deployable
artifact.

First build the sdist using uv.

```shell
example_udf $ uv build --sdist
Successfully built dist/example_udf-0.1.0.tar.gz
```

Then re-package the sdist into a zip.

```shell
example_udf $ zip -FS dist/example_udf-0.1.0.zip dist/example_udf-0.1.0.tar.gz
```

This creates `dist/example_udf-0.1.0.zip`.


### Upload

Use the `confluent` command line tool to upload this zip as a Flink
Python artifact.

```shell
example_udf $ confluent flink artifact create my-flink-artifact \
    --artifact-file dist/example_udf-0.1.0.zip \
    --runtime-language python \
    --cloud aws \
    --region us-west-2 \
    --environment env-123456
```

Take note of the resulting **artifact ID**.

See [the `confluent flink artifact create`
documentation](https://docs.confluent.io/confluent-cli/current/command-reference/flink/artifact/confluent_flink_artifact_create.html#confluent-flink-artifact-create)
for more info.


### Create Function

Before you can call a UDF in Flink SQL, you need to register the UDF
using [`CREATE
FUNCTION`](https://docs.confluent.io/cloud/current/flink/reference/statements/create-function.html),
where you specify the SQL function name, the qualified name of the UDF
in the package, and the artifact ID.

```sql
CREATE FUNCTION str_concat AS 'example_udf.scalar.str_concat' LANGUAGE PYTHON
USING JAR 'confluent-artifact://cfa-devcq2yx3m';
```

Execute this in isolation, and if it succeeds, you can call your UDF
in followup SQL by the SQL function name, in this case `str_concat`.
This name might be the same as the variable name in your Python
project, but `CREATE FUNCTION` can give it an arbitrary name.
