################################################################################
#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
# limitations under the License.
################################################################################

# THIS IS A VENDORED VERSION OF THIS MODULE FROM `apache-flink==2.0.0`.

"""
Common classes used by both Flink DataStream API and Table API:

    - :class:`Configuration`:
      Lightweight configuration object which stores key/value pairs.
    - :class:`ExecutionConfig`:
      A config to define the behavior of the program execution.
    - :class:`ExecutionMode`:
      Specifies how a batch program is executed in terms of data exchange: pipelining or batched.
    - :class:`TypeInformation`:
      TypeInformation is the core class of Flink's type system. FLink requires a type information
      for all types that are used as input or return type of a user function.
    - :class:`Types`:
      Contains utilities to access the :class:`TypeInformation` of the most common types for which
      Flink has provided built-in implementation.
    - :class:`WatermarkStrategy`:
      Defines how to generate Watermarks in the stream sources.
    - :class:`Row`:
      A row is a fixed-length, null-aware composite type for storing multiple values in a
      deterministic field order.
    - :class:`SerializationSchema`:
      Base class to describes how to turn a data object into a different serialized representation.
      Most data sinks (for example Apache Kafka) require the data to be handed to them in a specific
      format (for example as byte strings). See
      :class:`~pyflink.datastream.formats.json.JsonRowSerializationSchema`,
      :class:`~pyflink.datastream.formats.json.JsonRowDeserializationSchema`,
      :class:`~pyflink.datastream.formats.csv.CsvRowSerializationSchema`,
      :class:`~pyflink.datastream.formats.csv.CsvRowDeserializationSchema`,
      :class:`~pyflink.datastream.formats.avro.AvroRowSerializationSchema`,
      :class:`~pyflink.datastream.formats.avro.AvroRowDeserializationSchema`,
      :class:`~SimpleStringSchema` and
      :class:`~SimpleByteSchema` for more details.
"""
from pyflink.common.time import Duration, Instant, Time
from pyflink.common.types import Row, RowKind

__all__ = [
    "Row",
    "RowKind",
    "Duration",
    "Instant",
    "Time",
]


def _install():
    msg = "not vendored in cflt"
    raise NotImplementedError(msg)
