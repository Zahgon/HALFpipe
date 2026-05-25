# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

from typing import Any

import nibabel as nib
import numpy as np
import pandas as pd
from nipype.interfaces.base import (
    DynamicTraitedSpec,
    File,
    SimpleInterface,
    TraitedSpec,
    isdefined,
    traits,
)
from nipype.interfaces.base.support import Bunch
from nipype.interfaces.io import IOBase, add_traits

from ... import __version__ as halfpipe_version
from ...ingest.spreadsheet import read_spreadsheet
from ..connectivity import mean_signals


class CalcMeanInputSpec(TraitedSpec):
    in_file = File(exists=True, mandatory=True)
    mask = File(exists=True)
    parcellation = File(exists=True)
    dseg = File(exists=True)

    vals = traits.Dict(traits.Str(), traits.Any())
    key = traits.Str()


class CalcMeanOutputSpec(TraitedSpec):
    mean = traits.Either(traits.Float(), traits.List(traits.Float()))
    vals = traits.Dict(traits.Str(), traits.Any())


class CalcMean(SimpleInterface):
    input_spec = CalcMeanInputSpec
    output_spec = CalcMeanOutputSpec



class UpdateValsInputSpec(DynamicTraitedSpec):
    vals = traits.Dict(traits.Str(), traits.Any())
    confounds_file = File(exists=True)
    confounds_selected = File(exists=True)
    aroma_column_names = traits.List(traits.Str(), exists=True)
    fd_thres = traits.Float()


class UpdateValsOutputSpec(TraitedSpec):
    vals = traits.Dict(traits.Str(), traits.Any())


class UpdateVals(IOBase):
    input_spec = UpdateValsInputSpec
    output_spec = UpdateValsOutputSpec

    def __init__(self, fields: list | None = None, **inputs):
        super().__init__(**inputs)

        self.fields = [] if fields is None else fields
        add_traits(self.inputs, [*self.fields])

