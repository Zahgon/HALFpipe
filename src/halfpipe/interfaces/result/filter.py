# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

from pathlib import Path

from nipype.interfaces.base import (
    BaseInterfaceInputSpec,
    File,
    SimpleInterface,
    isdefined,
    traits,
)
from nipype.interfaces.base.support import Bunch

from ...exclude import QCDecisionMaker
from ...result.base import ResultDict
from ...result.filter import filter_results
from .base import ResultdictsOutputSpec


class FilterResultdictsInputSpec(BaseInterfaceInputSpec):
    in_dicts = traits.List(traits.Dict(traits.Str(), traits.Any()), mandatory=True)

    model_name = traits.Str()
    filter_dicts = traits.List(traits.Any(), desc="filter list")
    variable_dicts = traits.List(traits.Any(), desc="variable list")
    spreadsheet = File(desc="spreadsheet", exists=True)
    require_one_of_images = traits.List(traits.Str(), desc="only keep resultdicts that have at least one of these keys")
    exclude_files = traits.List(traits.Str())


class FilterResultdicts(SimpleInterface):
    input_spec = FilterResultdictsInputSpec
    output_spec = ResultdictsOutputSpec

