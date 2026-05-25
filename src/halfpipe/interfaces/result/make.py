# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import re
from collections import defaultdict
from typing import Any

from nipype.interfaces.base import DynamicTraitedSpec, isdefined, traits
from nipype.interfaces.io import IOBase, add_traits

from ...model.resultdict import ResultdictSchema
from ...model.utils import get_schema_entities
from ...result.base import ResultDict, ResultKey
from ...utils.copy import deepcopy
from ...utils.ops import ravel
from .base import ResultdictsOutputSpec

resultdict_schema = ResultdictSchema()
resultdict_entities = set(get_schema_entities(resultdict_schema))

composite_attr = re.compile(r"(?P<tag>[a-z]+)_(?P<attr>[a-z]+)")


class MakeResultdictsOutputSpec(ResultdictsOutputSpec):
    vals = traits.Dict(traits.Str(), traits.Any())


class MakeResultdicts(IOBase):
    input_spec = DynamicTraitedSpec
    output_spec = MakeResultdictsOutputSpec

    def __init__(
        self,
        dictkeys: list[str] | None = None,
        tagkeys: list[str] | None = None,
        valkeys: list[str] | None = None,
        imagekeys: list[str] | None = None,
        reportkeys: list[str] | None = None,
        metadatakeys: list[str] | None = None,
        nobroadcastkeys: list[str] | None = None,
        deletekeys: list[str] | None = None,
        missingvalues: list[Any] | None = None,
        **inputs,
    ):
        super(MakeResultdicts, self).__init__(**inputs)

        if dictkeys is None:
            dictkeys = ["tags", "metadata", "vals"]
        if tagkeys is None:
            tagkeys = list()
        if valkeys is None:
            valkeys = list()
        if imagekeys is None:
            imagekeys = list()
        if reportkeys is None:
            reportkeys = list()
        if metadatakeys is None:
            metadatakeys = list()
        if nobroadcastkeys is None:
            nobroadcastkeys = list()
        if deletekeys is None:
            deletekeys = list()
        if missingvalues is None:
            missingvalues = [None]

        add_traits(
            self.inputs,
            [*tagkeys, *valkeys, *imagekeys, *reportkeys, *metadatakeys, *dictkeys],
        )
        self._dictkeys = dictkeys
        self._keys: dict[ResultKey, list[str]] = {
            "tags": tagkeys,
            "vals": valkeys,
            "images": imagekeys,
            "reports": reportkeys,
            "metadata": metadatakeys,
        }
        self._nobroadcastkeys = nobroadcastkeys
        self._deletekeys = deletekeys
        self._missingvalues = missingvalues

