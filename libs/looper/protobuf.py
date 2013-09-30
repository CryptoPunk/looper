#!/usr/bin/env python

import json
import sys,os
from google.protobuf.descriptor import FieldDescriptor as FD

import sys
sys.path.append('libs/pb2')
for i in os.listdir('libs/pb2'):
    if i[-2:] == "py":
        print "importing", i[:-3]
        exec("from %s import *" % i[:-3])

from pprint import pprint
import types


used_types = [] # Protobuf types

modules = [] # protobuf modules

int_types = [
    FD.TYPE_DOUBLE,
    FD.TYPE_FLOAT,
    FD.TYPE_UINT32,
    FD.TYPE_UINT64,
    FD.TYPE_INT32,
    FD.TYPE_INT64,
    FD.TYPE_FIXED32,
    FD.TYPE_FIXED64,
    FD.TYPE_SFIXED32,
    FD.TYPE_SFIXED64,
    FD.TYPE_SINT32,
    FD.TYPE_SINT64]

bool_types = [
    FD.TYPE_BOOL]
 
str_types = [
    FD.TYPE_STRING,
    FD.TYPE_BYTES]

message_types = [
    FD.TYPE_MESSAGE]

enum_types = [
    FD.TYPE_ENUM]

def message(class_name, **kwargs):
    def get_enum(message,value):
        if types.StringType == type(value) or types.UnicodeType == type(value):
            return getattr(message,value)
        return value

    cont = True
    while cont:       
        try:
            return_message = None
            for module in modules:
                #print module
                if hasattr(module,class_name):
                    return_message = getattr(module, class_name)()
    
            if None == return_message:
                raise Exception("Couldn't find class: "+class_name)
                
            for field in return_message.DESCRIPTOR.fields:
    
                if FD.LABEL_REQUIRED == field.label and field.name not in kwargs:
                    if not field.has_default_value:
                        raise Exception(field.name + " required but not in kwargs")
                    else:
                        setattr(return_message,field.name,field.default_value)
                elif field.name in kwargs:
                    if FD.LABEL_REPEATED == field.label:
                        if   (type(kwargs[field.name]) == types.GeneratorType):
                            raise Exception("repeated_generator not supported")
                        elif (type(kwargs[field.name]) == types.ListType):
                            for sub_item in kwargs[field.name]:
               #                 print class_name +"."+field.name
                                msg_item = getattr(return_message,field.name)

                                if(hasattr(sub_item,'next')):
                                    next_val = sub_item.next()
                                    msg_item.extend([next_val])
                                else:
                                    msg_item.extend([sub_item])
                    else:
                        if(hasattr(kwargs[field.name],'next')):
                #            print class_name +"."+field.name
                            next_val = kwargs[field.name].next()
                            if field.type in message_types:
                                getattr(return_message,field.name).CopyFrom(next_val)
                            elif field.type in enum_types:
                                int_val = get_enum(return_message,next_val)
                                setattr(return_message,field.name,int_val)
                            else:
                                setattr(return_message,field.name,next_val)
                        else:
                 #           print class_name +"."+field.name
                            if field.type in message_types:
                                getattr(return_message,field.name).CopyFrom(kwargs[field.name])
                            elif field.type in enum_types:
                                int_val = get_enum(return_message,kwargs[field.name])
                                setattr(return_message,field.name,int_val)
                            else:
                                setattr(return_message,field.name,kwargs[field.name])
            yield return_message

        except StopIteration:
            print "StopIteration received!"
            cont = False

