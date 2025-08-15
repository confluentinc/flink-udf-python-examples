# Example Apache Flink® Python User Defined Functions on Confluent Cloud

This repository contains example Python UDFs packaged for Confluent Cloud.


## Creating from Scratch

The process for making a new UDF Python project using
[uv](https://docs.astral.sh/uv/) is as follows.


### Init Repo

Create a new "library" project with your desired name and Python
version. Only Python versions 3.10-3.11 are currently supported.

```shell
$ uv init -p 3.11 --lib example_udf
$ cd example_udf
```


### Add Environment Constraints

Append this to `example_udf/pyproject.toml`. This ensures that your
local dependencies are compatible with those available.

TODO: Add a link to the constantly updated constraint list.

```toml
[tool.uv]
constraint-dependencies = [
    "apache-flink~=2.0.0",
    "click>=8.2.0",
    "confluent-function-runtime-core>=0.161.0",
    "grpc-interceptor>=0.15.0",
    "grpcio-health-checking>=1.65.0",
    "grpcio-reflection>=1.65.0",
    "grpcio>=1.65.0",
    "protobuf>=5.29.1",
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


## Deployment

Once you have updated your UDF code and you would like to deploy it.

### Create Zip

A "source distribution" (sdist) in zip format is the deployable
artifact.

First build the sdist using uv.

```shell
example_udf $ uv build --sdist
Successfully built dist/example_udf-0.1.0.tar.gz
```

Then re-package that as a zip.

```shell
example_udf $ cd dist
example_udf/dist $ zip -r example_udf-0.1.0.zip .
```

This creates `dist/example_udf-0.1.0.zip`.

You can also use the script included here
[`targz2zip.sh`](targz2zip.sh).

```shell
example_udf $ ./targz2zip.sh dist/example_udf-0.1.0.tar.gz
Writing dist/example_udf-0.1.0.zip
```


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

See [the `confluent flink artifact create`
documentation](https://docs.confluent.io/confluent-cli/current/command-reference/flink/artifact/confluent_flink_artifact_create.html#confluent-flink-artifact-create)
for more info.


## Testing

You can follow the [testing instructions in the PyFlink
documentation](https://nightlies.apache.org/flink/flink-docs-release-2.1/docs/dev/python/table/udfs/overview/#testing-user-defined-functions).

TODO: Checking types, etc.
