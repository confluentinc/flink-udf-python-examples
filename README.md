# Example Customer UDF

Here are some example Python UDFs packaged for Confluent Cloud.

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
example_udf/dist $ mkdir tmp
example_udf/dist $ tar -xvf example_udf-0.1.0.tar.gz -C tmp
x example_udf-0.1.0/PKG-INFO
x example_udf-0.1.0/
x example_udf-0.1.0/README.md
x example_udf-0.1.0/pyproject.toml
x example_udf-0.1.0/src
x example_udf-0.1.0/src/example_udf
x example_udf-0.1.0/src/example_udf/__init__.py
x example_udf-0.1.0/src/example_udf/py.typed
example_udf/dist $ cd tmp
example_udf/dist/tmp $ zip -r ../example_udf-0.1.0.zip .
  adding: example_udf-0.1.0/ (stored 0%)
  adding: example_udf-0.1.0/PKG-INFO (deflated 55%)
  adding: example_udf-0.1.0/pyproject.toml (deflated 49%)
  adding: example_udf-0.1.0/README.md (deflated 55%)
  adding: example_udf-0.1.0/src/ (stored 0%)
  adding: example_udf-0.1.0/src/example_udf/ (stored 0%)
  adding: example_udf-0.1.0/src/example_udf/__init__.py (deflated 37%)
  adding: example_udf-0.1.0/src/example_udf/py.typed (stored 0%)
example_udf/dist/tmp $ cd ..
example_udf/dist $ rm -rf tmp
```

This creates `dist/example_udf-0.1.0.zip`.

You can also use the script included here
[`targz2zip.sh`](targz2zip.sh).

```shell
example_udf $ ./targz2zip.sh dist/example_udf-0.1.0.tar.gz
Extracting dist/example_udf-0.1.0.tar.gz
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
    "click>=8.2.0",
    "confluent-function-runtime-core>=0.161.0",
    "grpc-interceptor>=0.15.0",
    "grpcio-health-checking>=1.59.0",
    "grpcio-reflection>=1.59.0",
    "grpcio>=1.59.0",
    "protobuf>=5.29.0",
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
