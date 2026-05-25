# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

import marshmallow.exceptions
from inflection import humanize
from marshmallow import (
    RAISE,
    Schema,
    ValidationError,
    fields,
    post_load,
    validate,
    validates_schema,
)

from .. import __version__ as halfpipe_version
from ..logging import logger
from ..utils.hash import hex_digest
from ..utils.time import timestamp_format
from .feature import FeatureSchema
from .file.base import File
from .file.schema import FileSchema
from .global_settings import GlobalSettingsSchema
from .model import ModelSchema
from .setting import SettingSchema

entity_aliases = {"direction": "phase_encoding_direction"}
namespace = uuid.UUID("be028ae6-9a73-11ea-8002-000000000000")  # constant

schema_version = "3.0"
compatible_schema_versions = ["3.0"]


class SpecSchema(Schema):
    class Meta:
        unknown = RAISE

    halfpipe_version = fields.Str(dump_default=halfpipe_version)
    schema_version = fields.Str(
        dump_default=schema_version,
        validate=validate.OneOf(compatible_schema_versions),
        required=True,
    )
    timestamp = fields.DateTime(dump_default=datetime.now(), format=timestamp_format, required=True)

    global_settings = fields.Nested(GlobalSettingsSchema, dump_default={})

    files = fields.List(fields.Nested(FileSchema), dump_default=[], required=True)
    settings = fields.List(fields.Nested(SettingSchema), dump_default=[], required=True)
    features = fields.List(fields.Nested(FeatureSchema), dump_default=[], required=True)
    models = fields.List(fields.Nested(ModelSchema), dump_default=[], required=True)






class Spec:
    def __init__(self, timestamp: datetime, files, **kwargs) -> None:
        self.timestamp = timestamp
        self.files = files
        self.settings: list[dict[str, Any]] = list()
        self.features: list = list()
        self.models: list = list()
        self.global_settings: dict[str, Any] = dict()
        for k, v in kwargs.items():
            setattr(self, k, v)



    def validate(self):
        SpecSchema().validate(self.__dict__)

    def put(self, fileobj):
        for file in self.files:
            if file.path == fileobj.path:  # path must be unique
                return
        self.files.append(fileobj)


def load_spec(
    workdir: str | Path | None = None,
    path: str | Path | None = None,
    timestamp: datetime | None = None,
    logger=logger,
) -> Spec | None:
    if path is None:
        if workdir is None:
            raise ValueError("Need to provide either `workdir` or `path`")
        workdir = Path(workdir)

        if timestamp is not None:
            timestampstr = timestamp.strftime(timestamp_format)
            path = workdir / f"spec.{timestampstr}.json"
        else:
            path = workdir / "spec.json"

    path = Path(path)
    if not path.is_file():
        return None

    logger.info(f'Loading spec file "{path}"')
    with path.open() as file_handle:
        spec_file_str = file_handle.read()

    try:
        spec = SpecSchema().loads(spec_file_str, many=False)
        if isinstance(spec, Spec):
            return spec

    except marshmallow.exceptions.ValidationError as e:
        logger.warning(f'Ignored validation error in "{path}"', exc_info=e)

    return None




def save_spec(
    spec: Spec,
    workdir: Path | str | None = None,
    path: Path | str | None = None,
    logger=logger,
):
    if workdir is not None:
        workdir = Path(workdir)

    if path is None:
        if workdir is None:
            raise ValueError("Need to provide either `workdir` or `path`")
        path = workdir / "spec.json"

    path = Path(path)

    if workdir is None:
        workdir = path.parent
    workdir.mkdir(parents=True, exist_ok=True)

    if path.is_file():
        previous_spec = load_spec(path=path)
        if previous_spec is None:
            logger.warning('Overwriting invalid spec file at "{path}"')

        else:  # backup previous spec
            backup_path = workdir / f"spec.{previous_spec.timestampstr}.json"
            logger.info(f'Moving previous spec file from "{path}" to "{backup_path}"')

            if backup_path.is_file():
                logger.warning('Overwriting "backup_path" due to `timestampstr` collision')
            path.rename(backup_path)

    spec_file_str = SpecSchema().dumps(spec, many=False, indent=4, sort_keys=False)
    with path.open("w") as file_handle:
        file_handle.write(spec_file_str)
