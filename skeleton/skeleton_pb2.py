# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: skeleton.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='skeleton.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n\x0eskeleton.proto\"\x1d\n\nMsgRequest\x12\x0f\n\x07message\x18\x01 \x01(\t\"\x1e\n\x0bMsgResponse\x12\x0f\n\x07message\x18\x01 \x01(\t26\n\x08Skeleton\x12*\n\x0bMsgTransfer\x12\x0b.MsgRequest\x1a\x0c.MsgResponse\"\x00\x62\x06proto3'
)




_MSGREQUEST = _descriptor.Descriptor(
  name='MsgRequest',
  full_name='MsgRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='MsgRequest.message', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=18,
  serialized_end=47,
)


_MSGRESPONSE = _descriptor.Descriptor(
  name='MsgResponse',
  full_name='MsgResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='MsgResponse.message', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=49,
  serialized_end=79,
)

DESCRIPTOR.message_types_by_name['MsgRequest'] = _MSGREQUEST
DESCRIPTOR.message_types_by_name['MsgResponse'] = _MSGRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MsgRequest = _reflection.GeneratedProtocolMessageType('MsgRequest', (_message.Message,), {
  'DESCRIPTOR' : _MSGREQUEST,
  '__module__' : 'skeleton_pb2'
  # @@protoc_insertion_point(class_scope:MsgRequest)
  })
_sym_db.RegisterMessage(MsgRequest)

MsgResponse = _reflection.GeneratedProtocolMessageType('MsgResponse', (_message.Message,), {
  'DESCRIPTOR' : _MSGRESPONSE,
  '__module__' : 'skeleton_pb2'
  # @@protoc_insertion_point(class_scope:MsgResponse)
  })
_sym_db.RegisterMessage(MsgResponse)



_SKELETON = _descriptor.ServiceDescriptor(
  name='Skeleton',
  full_name='Skeleton',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=81,
  serialized_end=135,
  methods=[
  _descriptor.MethodDescriptor(
    name='MsgTransfer',
    full_name='Skeleton.MsgTransfer',
    index=0,
    containing_service=None,
    input_type=_MSGREQUEST,
    output_type=_MSGRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_SKELETON)

DESCRIPTOR.services_by_name['Skeleton'] = _SKELETON

# @@protoc_insertion_point(module_scope)
