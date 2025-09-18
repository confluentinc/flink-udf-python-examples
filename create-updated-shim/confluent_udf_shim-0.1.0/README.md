# Confluent UDF SHIM implementation for Python language

This module contains the implementation of the Confluent UDF SHIM for Python language.

## Setup Instructions

### Development prerequisites

- [`uv` Python project manager](https://docs.astral.sh/uv/)

- [`jq`](https://jqlang.org/),
  [`grpcurl`](https://github.com/fullstorydev/grpcurl), and `protoc` to help
  with crafting invoke commands locally.

### Installation

Install the above.

```shell
$ brew install uv jq grpcurl protoc
```

`uv` will ensure all dependencies are installed in and used from a virtualenv
automatically whenever you run any of the following `uv` commands.


## Running Tests

To run all the tests, use
[pytest](https://docs.pytest.org/en/stable/):

```shell
$ uv run pytest
```


## Formatter, Lints, and Type Checking

The [Ruff](https://docs.astral.sh/ruff/) formatter and linter, and the
[mypy](https://mypy.readthedocs.io/en/stable/index.html) type checker
should be run before committing any Python code. There is a
[tox](https://tox.wiki/) env to do this:

```shell
$ uv run tox run -e format,type
```

This is what I use in a loop while developing.

You can see the exact Ruff and mypy commands run by tox in
`pyproject.toml` under `[tool.tox]`.


## Preparing for CI

We have set up tox as a way to run tests against every version of
Python we support, run the linter, and run the type checker. This is
the exact command that is run in CI, so if you want to be sure you'll
pass CI, you can run it locally first.

```shell
$ uv run tox
```


## Protobuf Files

This shim requires the following protobuf definitions.

- The CC Flink Remote UDF interface, originally from the
  [`cc-flink-udf-adapter-api`
  module](https://github.com/confluentinc/flink/tree/release-2.0-confluent/cc-flink-extensions/cc-flink-udf-adapter-api/api/v1),
  now in `proto/`.

Any changes to the original sources should be copied into this project and then
the stubs re-compiled.

To compile all the Python stubs from the proto files in this directory and add
copyright headers, run the following command:

``` shell
$ ./compile_protobuf.sh
```


## Generating Shim Deployment Artifact

The provided script will build a `py_shim_artifact.zip` containing the correct
format for SCP.

``` shell
$ ./build_artifact_zip.sh
```


## Invoking a Python UdfTask on the secure platform

``` shell
# plugin zip must created without root dir
cd python_udfs
zip -r ../plugin_py.zip *

confluent login
confluent flink artifact create panos-python-test --cloud aws --region us-west-2 --environment $envId --artifact-file plugin_py.zip --runtime-language python --class extractor.ExtractionHandler
```


## Locally Manually Invoking Extraction

### Using Test Fixture UDFs

If you'd like to manually run an extraction against one of the test
fixures UDFs in `tests/udf_fixtures.py`, you can use the existing
project venv.

You'll need to setup an empty `scp_config` directory to make the SCP
server happy.

```shell
$ mkdir scp_config
```

Then in one shell, run this in the background. This starts up the SCP
server, the current version of the shim.

```shell
$ uv run \
  -m confluent_function_runtime_server \
  --handler_name confluent_udf_shim.extractor.ExtractionHandler \
  --config_override_dir scp_config
```

You can then run your `grpcurl` commands described below to request a
specific UDF is extracted.


### Using A Customer UDF Sdist

To use an arbitrary UDF sdist, you have to install it into the dev venv, but
also ignore its dependency on `apache-flink` (because we are vendoring the
module). You should change the path to the
customer UDF sdist you want to test.

```shell
$ uv pip install \
  --override <(echo "apache-flink ; sys_platform == 'never'") \
  ~/cflt/flink-udf-python-examples/dist/example_udf-0.1.0.tar.gz
```

Then run the `uv run` command in the previous section to start the SCP server.
You can then run your `grpcurl` commands described below. You should `uv sync`
to uninstall the UDF sdist from the dev venv when you are done.


### Extraction Locally

Then use [`grpcurl`](https://github.com/fullstorydev/grpcurl) to
invoke the extraction handler. You will need to change the UDF
qualified name below, or you can keep this one that is in the test
fixtures.

```shell
$ grpcurl -plaintext \
    -d '{"payload": "'$(echo 'class_name: "tests.udf_fixtures.add_one"' | protoc --encode=flink.udf.extractor.v1.ExtractionRequest proto/extractor.proto | base64)'"}' \
    localhost:50051 \
    secure.compute.function.runtime.v2.FunctionRuntime/Invoke \
  | jq -r .payload \
  | base64 -d \
  | protoc --decode=flink.udf.extractor.v1.ExtractionResponse proto/extractor.proto
signatures {
  argumentTypes: "BIGINT"
  argumentTypes: "BIGINT"
  returnType: "BIGINT"
  argumentNames: "i"
  argumentNames: "j"
}
is_deterministic: true
function_kind: "SCALAR"
```

If you get an error response it will be in the `"payload"` key at the
top level, and is not a nested protobuf message, just a string error.
Rerun with the following instead to see the error in plaintext.

```shell
$ grpcurl ... \
  | jq -r .payload \
  | base64 -d
```


## Locally Manually Invoking Execution

Execution is similar to extraction, you can install an arbitrary UDF
sdist into the dev venv using the command above, or you can use the
test fixture UDFs. In either case, execution is different in that the
"UDF Spec" which is an SCP env config var is what determines which UDF
is actually used.

We have some spec tools to help prepare that config var. Specify the
UDF qualified name you want to execute and use the `gen_spec`
subcommand, then write it to the `scp_config` directory.

```shell
$ mkdir scp_config
$ uv run -m tests.spec_tools tests.udf_fixtures.add_one gen-spec > scp_config/spec_base64
```

Now that the config dir `scp_config` is prepared, you can run the
server with the execution handler.

```shell
$ uv run \
  -m confluent_function_runtime_server \
  --handler_name confluent_udf_shim.executor.ExecutionHandler \
  --config_override_dir scp_config
```

Now we can invoke the handler. Another extra complication here is that
the encoding format for arguments is custom binary. Again you can use
the spec tools to encode the arguments and decode the result.

```shell
$ grpcurl -plaintext \
    -d '{"payload": "'$(uv run -m tests.spec_tools tests.udf_fixtures.add_one encode-args 1 2)'"}' \
    localhost:50051 \
    secure.compute.function.runtime.v2.FunctionRuntime/Invoke \
    | jq -r .payload \
    | uv run -m tests.spec_tools tests.udf_fixtures.add_one decode-result -
3
```
