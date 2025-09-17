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

from abc import ABC, abstractmethod
from typing import Union

from pyflink.fn_execution import coder_impl_slow as coder_impl


__all__ = ['FlattenRowCoder', 'RowCoder', 'BigIntCoder', 'TinyIntCoder', 'BooleanCoder',
           'SmallIntCoder', 'IntCoder', 'FloatCoder', 'DoubleCoder', 'BinaryCoder', 'CharCoder',
           'DateCoder', 'TimeCoder', 'TimestampCoder', 'LocalZonedTimestampCoder', 'InstantCoder',
           'GenericArrayCoder', 'PrimitiveArrayCoder', 'MapCoder', 'DecimalCoder',
           'BigDecimalCoder', 'TupleCoder', 'TimeWindowCoder', 'CountWindowCoder',
           'PickleCoder', 'CloudPickleCoder', 'DataViewFilterCoder']


#########################################################################
#             Top-level coder: ValueCoder & IterableCoder
#########################################################################

# LengthPrefixBaseCoder is the top level coder and the other coders will be used as the field coder
class LengthPrefixBaseCoder(ABC):
    def __init__(self, field_coder: 'FieldCoder'):
        self._field_coder = field_coder

    @abstractmethod
    def get_impl(self):
        pass

    @classmethod
    def from_coder_info_descriptor_proto(cls, coder_info_descriptor_proto):
        msg = "not vendored in cflt"
        raise NotImplementedError(msg)

    @classmethod
    def _to_field_coder(cls, coder_info_descriptor_proto):
        msg = "not vendored in cflt"
        raise NotImplementedError(msg)

    @classmethod
    def _to_arrow_schema(cls, row_type):
        msg = "not vendored in cflt"
        raise NotImplementedError(msg)

    @classmethod
    def _to_data_type(cls, field_type):
        msg = "not vendored in cflt"
        raise NotImplementedError(msg)

    @classmethod
    def _to_row_type(cls, row_schema):
        msg = "not vendored in cflt"
        raise NotImplementedError(msg)


class IterableCoder(LengthPrefixBaseCoder):
    """
    Coder for iterable data.
    """

    def __init__(self, field_coder: 'FieldCoder', separated_with_end_message):
        super(IterableCoder, self).__init__(field_coder)
        self._separated_with_end_message = separated_with_end_message

    def get_impl(self):
        return coder_impl.IterableCoderImpl(self._field_coder.get_impl(),
                                            self._separated_with_end_message)


class ValueCoder(LengthPrefixBaseCoder):
    """
    Coder for single data.
    """

    def __init__(self, field_coder: 'FieldCoder'):
        super(ValueCoder, self).__init__(field_coder)

    def get_impl(self):
        return coder_impl.ValueCoderImpl(self._field_coder.get_impl())


#########################################################################
#                         Low-level coder: FieldCoder
#########################################################################


class FieldCoder(ABC):

    def get_impl(self) -> coder_impl.FieldCoderImpl:
        pass

    def __eq__(self, other):
        return type(self) == type(other)


class FlattenRowCoder(FieldCoder):
    """
    Coder for Row. The decoded result will be flattened as a list of column values of a row instead
    of a row object.
    """

    def __init__(self, field_coders):
        self._field_coders = field_coders

    def get_impl(self):
        return coder_impl.FlattenRowCoderImpl([c.get_impl() for c in self._field_coders])

    def __repr__(self):
        return 'FlattenRowCoder[%s]' % ', '.join(str(c) for c in self._field_coders)

    def __eq__(self, other: 'FlattenRowCoder'):
        return (self.__class__ == other.__class__
                and len(self._field_coders) == len(other._field_coders)
                and [self._field_coders[i] == other._field_coders[i] for i in
                     range(len(self._field_coders))])

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self._field_coders)


class ArrowCoder(FieldCoder):
    """
    Coder for Arrow.
    """

    def __init__(self, schema, row_type, timezone):
        self._schema = schema
        self._row_type = row_type
        self._timezone = timezone

    def get_impl(self):
        return coder_impl.ArrowCoderImpl(self._schema, self._row_type, self._timezone)

    def __repr__(self):
        return 'ArrowCoder[%s]' % self._schema


class OverWindowArrowCoder(FieldCoder):
    """
    Coder for batch pandas over window aggregation.
    """

    def __init__(self, schema, row_type, timezone):
        self._arrow_coder = ArrowCoder(schema, row_type, timezone)

    def get_impl(self):
        return coder_impl.OverWindowArrowCoderImpl(self._arrow_coder.get_impl())

    def __repr__(self):
        return 'OverWindowArrowCoder[%s]' % self._arrow_coder


class RowCoder(FieldCoder):
    """
    Coder for Row.
    """

    def __init__(self, field_coders, field_names):
        self._field_coders = field_coders
        self._field_names = field_names

    def get_impl(self):
        return coder_impl.RowCoderImpl([c.get_impl() for c in self._field_coders],
                                       self._field_names)

    def __repr__(self):
        return 'RowCoder[%s]' % ', '.join(str(c) for c in self._field_coders)

    def __eq__(self, other: 'RowCoder'):
        return (self.__class__ == other.__class__
                and self._field_names == other._field_names
                and [self._field_coders[i] == other._field_coders[i] for i in
                     range(len(self._field_coders))])

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self._field_coders)


class CollectionCoder(FieldCoder):
    """
    Base coder for collection.
    """

    def __init__(self, elem_coder):
        self._elem_coder = elem_coder

    def is_deterministic(self):
        return self._elem_coder.is_deterministic()

    def __eq__(self, other: 'CollectionCoder'):
        return (self.__class__ == other.__class__
                and self._elem_coder == other._elem_coder)

    def __repr__(self):
        return '%s[%s]' % (self.__class__.__name__, repr(self._elem_coder))

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self._elem_coder)


class GenericArrayCoder(CollectionCoder):
    """
    Coder for generic array such as basic array or object array.
    """

    def __init__(self, elem_coder):
        super(GenericArrayCoder, self).__init__(elem_coder)

    def get_impl(self):
        return coder_impl.GenericArrayCoderImpl(self._elem_coder.get_impl())


class PrimitiveArrayCoder(CollectionCoder):
    """
    Coder for Primitive Array.
    """

    def __init__(self, elem_coder):
        super(PrimitiveArrayCoder, self).__init__(elem_coder)

    def get_impl(self):
        return coder_impl.PrimitiveArrayCoderImpl(self._elem_coder.get_impl())


class MapCoder(FieldCoder):
    """
    Coder for Map.
    """

    def __init__(self, key_coder, value_coder):
        self._key_coder = key_coder
        self._value_coder = value_coder

    def get_impl(self):
        return coder_impl.MapCoderImpl(self._key_coder.get_impl(), self._value_coder.get_impl())

    def is_deterministic(self):
        return self._key_coder.is_deterministic() and self._value_coder.is_deterministic()

    def __repr__(self):
        return 'MapCoder[%s]' % ','.join([repr(self._key_coder), repr(self._value_coder)])

    def __eq__(self, other: 'MapCoder'):
        return (self.__class__ == other.__class__
                and self._key_coder == other._key_coder
                and self._value_coder == other._value_coder)

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash([self._key_coder, self._value_coder])


class BigIntCoder(FieldCoder):
    """
    Coder for 8 bytes long.
    """

    def get_impl(self):
        return coder_impl.BigIntCoderImpl()


class TinyIntCoder(FieldCoder):
    """
    Coder for Byte.
    """

    def get_impl(self):
        return coder_impl.TinyIntCoderImpl()


class BooleanCoder(FieldCoder):
    """
    Coder for Boolean.
    """

    def get_impl(self):
        return coder_impl.BooleanCoderImpl()


class SmallIntCoder(FieldCoder):
    """
    Coder for Short.
    """

    def get_impl(self):
        return coder_impl.SmallIntCoderImpl()


class IntCoder(FieldCoder):
    """
    Coder for 4 bytes int.
    """

    def get_impl(self):
        return coder_impl.IntCoderImpl()


class FloatCoder(FieldCoder):
    """
    Coder for Float.
    """

    def get_impl(self):
        return coder_impl.FloatCoderImpl()


class DoubleCoder(FieldCoder):
    """
    Coder for Double.
    """

    def get_impl(self):
        return coder_impl.DoubleCoderImpl()


class DecimalCoder(FieldCoder):
    """
    Coder for Decimal.
    """

    def __init__(self, precision, scale):
        self.precision = precision
        self.scale = scale

    def get_impl(self):
        return coder_impl.DecimalCoderImpl(self.precision, self.scale)

    def __eq__(self, other: 'DecimalCoder'):
        return (self.__class__ == other.__class__ and
                self.precision == other.precision and
                self.scale == other.scale)


class BigDecimalCoder(FieldCoder):
    """
    Coder for Basic Decimal that no need to have precision and scale specified.
    """

    def get_impl(self):
        return coder_impl.BigDecimalCoderImpl()


class BinaryCoder(FieldCoder):
    """
    Coder for Byte Array.
    """

    def get_impl(self):
        return coder_impl.BinaryCoderImpl()


class CharCoder(FieldCoder):
    """
    Coder for Character String.
    """

    def get_impl(self):
        return coder_impl.CharCoderImpl()


class DateCoder(FieldCoder):
    """
    Coder for Date
    """

    def get_impl(self):
        return coder_impl.DateCoderImpl()


class TimeCoder(FieldCoder):
    """
    Coder for Time.
    """

    def get_impl(self):
        return coder_impl.TimeCoderImpl()


class TimestampCoder(FieldCoder):
    """
    Coder for Timestamp.
    """

    def __init__(self, precision):
        self.precision = precision

    def get_impl(self):
        return coder_impl.TimestampCoderImpl(self.precision)

    def __eq__(self, other: 'TimestampCoder'):
        return self.__class__ == other.__class__ and self.precision == other.precision


class LocalZonedTimestampCoder(FieldCoder):
    """
    Coder for LocalZonedTimestamp.
    """

    def __init__(self, precision, timezone):
        self.precision = precision
        self.timezone = timezone

    def get_impl(self):
        return coder_impl.LocalZonedTimestampCoderImpl(self.precision, self.timezone)

    def __eq__(self, other: 'LocalZonedTimestampCoder'):
        return (self.__class__ == other.__class__ and
                self.precision == other.precision and
                self.timezone == other.timezone)


class InstantCoder(FieldCoder):
    """
    Coder for Instant.
    """
    def get_impl(self) -> coder_impl.FieldCoderImpl:
        return coder_impl.InstantCoderImpl()


class CloudPickleCoder(FieldCoder):
    """
    Coder used with cloudpickle to encode python object.
    """

    def get_impl(self):
        return coder_impl.CloudPickleCoderImpl()


class PickleCoder(FieldCoder):
    """
    Coder used with pickle to encode python object.
    """

    def get_impl(self):
        return coder_impl.PickleCoderImpl()


class TupleCoder(FieldCoder):
    """
    Coder for Tuple.
    """

    def __init__(self, field_coders):
        self._field_coders = field_coders

    def get_impl(self):
        return coder_impl.TupleCoderImpl([c.get_impl() for c in self._field_coders])

    def __repr__(self):
        return 'TupleCoder[%s]' % ', '.join(str(c) for c in self._field_coders)

    def __eq__(self, other: 'TupleCoder'):
        return (self.__class__ == other.__class__ and
                [self._field_coders[i] == other._field_coders[i]
                 for i in range(len(self._field_coders))])


class TimeWindowCoder(FieldCoder):
    """
    Coder for TimeWindow.
    """

    def get_impl(self):
        return coder_impl.TimeWindowCoderImpl()


class CountWindowCoder(FieldCoder):
    """
    Coder for CountWindow.
    """

    def get_impl(self):
        return coder_impl.CountWindowCoderImpl()


class GlobalWindowCoder(FieldCoder):
    """
    Coder for GlobalWindow.
    """

    def get_impl(self):
        return coder_impl.GlobalWindowCoderImpl()


class DataViewFilterCoder(FieldCoder):
    """
    Coder for data view filter.
    """

    def __init__(self, udf_data_view_specs):
        self._udf_data_view_specs = udf_data_view_specs

    def get_impl(self):
        return coder_impl.DataViewFilterCoderImpl(self._udf_data_view_specs)


class AvroCoder(FieldCoder):

    def __init__(self, schema: Union[str, 'AvroSchema']):
        msg = "not vendored in cflt"
        raise NotImplementedError(msg)

    def get_impl(self):
        return coder_impl.AvroCoderImpl(self._schema_string)


class LocalDateCoder(FieldCoder):

    def get_impl(self):
        return coder_impl.LocalDateCoderImpl()


class LocalTimeCoder(FieldCoder):

    def get_impl(self):
        return coder_impl.LocalTimeCoderImpl()


class LocalDateTimeCoder(FieldCoder):

    def get_impl(self):
        return coder_impl.LocalDateTimeCoderImpl()


def from_proto(field_type):
    """
    Creates the corresponding :class:`Coder` given the protocol representation of the field type.

    :param field_type: the protocol representation of the field type
    :return: :class:`Coder`
    """
    msg = "not vendored in cflt"
    raise NotImplementedError(msg)


def from_type_info_proto(type_info):
    msg = "not vendored in cflt"
    raise NotImplementedError(msg)


def from_type_info(type_info: 'TypeInformation') -> FieldCoder:
    msg = "not vendored in cflt"
    raise NotImplementedError(msg)
