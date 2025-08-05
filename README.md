# Example Customer UDF

Here are some example Python UDFs packaged for Confluent Cloud.

## Deployment

Once you have updated your UDF code and you would like to deploy it.

### Create Zip

A "source distribution" in Zip format is the deployable artifact.

```shell
example_udf $ uv build --sdist
Successfully built dist/example_udf-0.1.0.tar.gz
example_udf $ ./targz2zip.sh dist/example_udf-0.1.0.tar.gz
Extracting dist/example_udf-0.1.0.tar.gz
Writing /dist/example_udf-0.1.0.zip
```

This creates `dist/example_udf-0.1.0.zip`.

### Upload

TODO

## Testing

You can follow the [testing instructions in the PyFlink
documentation](https://nightlies.apache.org/flink/flink-docs-release-2.1/docs/dev/python/table/udfs/overview/#testing-user-defined-functions).

TODO: Checking types, etc.


## Creating from Scratch

The process for making a new UDF Python project using
[uv](https://docs.astral.sh/uv/) is as follows.


### Init Repo

Create a new "library" project with your desired name.

```shell
$ uv init --lib example_udf
$ cd example_udf
```


### Add Environment Constraints

Append this to `example_udf/pyproject.toml`. This ensures that your
local dependencies are compatible with those available.

```toml
[tool.uv]
constraint-dependencies = [
    "apache-flink>=2.1.0",
    "confluent-function-runtime-core>=0.161.0",
    "protobuf>=5.29.0",
    "click>=8.2.0",
    "confluent-function-runtime-core>=0.161.0",
    "grpc-interceptor>=0.15.0",
    "grpcio-health-checking>=1.59.0",
    "grpcio-reflection>=1.59.0",
    "grpcio>=1.59.0",
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

This will error out if uv cannot reconcile your dependencies with the
constraints in the runtime.


### Add Modules

Add your UDF code within the `example_udf/src/example_udf/`. This is a
standard Python module, so make as much nested structure as you need.
