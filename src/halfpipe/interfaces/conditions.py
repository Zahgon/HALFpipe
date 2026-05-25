# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

from math import isclose

from nipype.interfaces.base import (
    Bunch,
    SimpleInterface,
    TraitedSpec,
    isdefined,
    traits,
)

from ..ingest.events import ConditionFile
from ..logging import logger


class ApplyConditionOffsetInputSpec(TraitedSpec):
    subject_info = traits.Any()
    scan_start = traits.Float()


class ApplyConditionOffsetOutputSpec(TraitedSpec):
    subject_info = traits.Any()


class ApplyConditionOffset(SimpleInterface):
    input_spec = ApplyConditionOffsetInputSpec
    output_spec = ApplyConditionOffsetOutputSpec



class ParseConditionFileInputSpec(TraitedSpec):
    in_any = traits.Any(
        mandatory=True,
    )

    condition_names = traits.List(traits.Str(), desc="filter conditions")

    contrasts = traits.List(
        traits.Tuple(
            traits.Str,
            traits.Enum("T"),
            traits.List(traits.Str),
            traits.List(traits.Float),
        ),
    )


class ParseConditionFileOutputSpec(TraitedSpec):
    subject_info = traits.Any()

    contrasts = traits.List(
        traits.Tuple(
            traits.Str,
            traits.Enum("T"),
            traits.List(traits.Str),
            traits.List(traits.Float),
        ),
    )

    condition_names = traits.List(traits.Str)
    contrast_names = traits.List(traits.Str)


class ParseConditionFile(SimpleInterface):
    input_spec = ParseConditionFileInputSpec
    output_spec = ParseConditionFileOutputSpec

