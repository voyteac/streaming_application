# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: event_notification.proto
# Protobuf Python Version: 5.28.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    0,
    '',
    'event_notification.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x18\x65vent_notification.proto\x12\x07\x65xample\"\xc7\x02\n\x11\x45ventNotification\x12\x18\n\x10unique_client_id\x18\x01 \x01(\x05\x12\x11\n\ttimestamp\x18\x02 \x01(\x01\x12\x16\n\x0emessage_number\x18\x03 \x01(\x05\x12\x13\n\x0b\x63lient_name\x18\x04 \x01(\t\x12\x10\n\x08metric_0\x18\x05 \x01(\x01\x12\x10\n\x08metric_1\x18\x06 \x01(\x01\x12\x10\n\x08metric_2\x18\x07 \x01(\x01\x12\x10\n\x08metric_3\x18\x08 \x01(\x01\x12\x10\n\x08metric_4\x18\t \x01(\x01\x12\x10\n\x08metric_5\x18\n \x01(\x01\x12\x10\n\x08metric_6\x18\x0b \x01(\x01\x12\x10\n\x08metric_7\x18\x0c \x01(\x01\x12\x10\n\x08metric_8\x18\r \x01(\x01\x12\x10\n\x08metric_9\x18\x0e \x01(\x01\x12\x11\n\tmetric_10\x18\x0f \x01(\x01\x12\x11\n\tmetric_11\x18\x10 \x01(\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'event_notification_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_EVENTNOTIFICATION']._serialized_start=38
  _globals['_EVENTNOTIFICATION']._serialized_end=365
# @@protoc_insertion_point(module_scope)
