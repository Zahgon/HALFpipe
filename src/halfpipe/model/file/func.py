# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

from pathlib import Path

from marshmallow import fields, pre_load, validate
from marshmallow_oneofschema import OneOfSchema

from ...ingest.metadata.direction import (
    canonicalize_direction_code,
    parse_direction_str,
)
from ...logging import logger
from ...utils.path import exists
from ..metadata import BoldMetadataSchema, EventsMetadataSchema, PEDirMetadataSchema
from ..tags import BoldTagsSchema, FuncTagsSchema, TxtEventsTagsSchema
from .base import BaseFileSchema, File


class BoldFileSchema(BaseFileSchema):
    datatype = fields.Str(dump_default="func", validate=validate.Equal("func"))
    suffix = fields.Str(dump_default="bold", validate=validate.Equal("bold"))
    extension = fields.Str(validate=validate.OneOf([".nii", ".nii.gz"]))

    tags = fields.Nested(BoldTagsSchema(), dump_default=dict())
    metadata = fields.Nested(BoldMetadataSchema(), dump_default=dict())



class SBRefFileSchema(BoldFileSchema):
    suffix = fields.Str(dump_default="sbref", validate=validate.Equal("sbref"))
    metadata = fields.Nested(PEDirMetadataSchema(), dump_default=dict())


class BaseEventsFileSchema(BaseFileSchema):
    datatype = fields.Str(dump_default="func", validate=validate.Equal("func"))
    suffix = fields.Str(dump_default="events", validate=validate.Equal("events"))

    tags = fields.Nested(FuncTagsSchema(), dump_default=dict())


class MatEventsFileSchema(BaseEventsFileSchema):
    extension = fields.Str(validate=validate.OneOf([".mat"]))

    metadata = fields.Nested(EventsMetadataSchema())


class TsvEventsFileSchema(BaseEventsFileSchema):
    extension = fields.Str(validate=validate.OneOf([".tsv"]))

    metadata = fields.Nested(EventsMetadataSchema(), dump_default={"units": "seconds"})


class TxtEventsFileSchema(BaseEventsFileSchema):
    extension = fields.Str(validate=validate.OneOf([".txt"]))

    tags = fields.Nested(TxtEventsTagsSchema(), dump_default=dict())
    metadata = fields.Nested(EventsMetadataSchema(), dump_default={"units": "seconds"})


class EventsFileSchema(OneOfSchema):
    type_field = "extension"
    type_field_remove = False
    type_schemas = {
        ".tsv": TsvEventsFileSchema,
        ".mat": MatEventsFileSchema,
        ".txt": TxtEventsFileSchema,
    }



class FuncFileSchema(OneOfSchema):
    type_field = "suffix"
    type_field_remove = False
    type_schemas = {
        "bold": BoldFileSchema,
        "sbref": SBRefFileSchema,
        "events": EventsFileSchema,
    }

