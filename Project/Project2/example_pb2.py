# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: example.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='example.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n\rexample.proto\"T\n\x05\x45vent\x12\x11\n\tinterface\x18\x01 \x01(\t\x12\r\n\x05money\x18\x02 \x01(\x05\x12\x0e\n\x06result\x18\x03 \x01(\t\x12\n\n\x02id\x18\x04 \x01(\x05\x12\r\n\x05\x63lock\x18\x05 \x01(\x05\x32&\n\x03RPC\x12\x1f\n\x0bMsgDelivery\x12\x06.Event\x1a\x06.Event\"\x00\x62\x06proto3'
)




_EVENT = _descriptor.Descriptor(
  name='Event',
  full_name='Event',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='interface', full_name='Event.interface', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='money', full_name='Event.money', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='result', full_name='Event.result', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='id', full_name='Event.id', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='clock', full_name='Event.clock', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=17,
  serialized_end=101,
)

DESCRIPTOR.message_types_by_name['Event'] = _EVENT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Event = _reflection.GeneratedProtocolMessageType('Event', (_message.Message,), {
  'DESCRIPTOR' : _EVENT,
  '__module__' : 'example_pb2'
  # @@protoc_insertion_point(class_scope:Event)
  })
_sym_db.RegisterMessage(Event)



_RPC = _descriptor.ServiceDescriptor(
  name='RPC',
  full_name='RPC',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=103,
  serialized_end=141,
  methods=[
  _descriptor.MethodDescriptor(
    name='MsgDelivery',
    full_name='RPC.MsgDelivery',
    index=0,
    containing_service=None,
    input_type=_EVENT,
    output_type=_EVENT,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_RPC)

DESCRIPTOR.services_by_name['RPC'] = _RPC

# @@protoc_insertion_point(module_scope)