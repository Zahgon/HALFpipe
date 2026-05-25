# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import re
from pathlib import Path
from typing import Any

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
from nipype.interfaces.io import IOBase, add_traits

from ...ingest.spreadsheet import read_spreadsheet
from ...logging import logger
from ...utils.ops import ravel

pandas_tocsv_kwargs: dict[str, Any] = {"sep": "\t", "na_rep": "n/a"}


class FillNAInputSpec(TraitedSpec):
    in_tsv = File(exists=True, desc="input tsv file")


class TsvOutputSpec(TraitedSpec):
    out_with_header = File(exists=True, desc="output tsv file with a header")
    out_no_header = File(exists=True, desc="output tsv file without header")
    column_names = traits.List(traits.Str, desc="list of column names in order")


class FillNA(SimpleInterface):
    """
    Remove NA values
    """

    input_spec = FillNAInputSpec
    output_spec = TsvOutputSpec



class MergeColumnsInputSpec(DynamicTraitedSpec):
    row_index = traits.Any(default=False, usedefault=True)


class MergeColumns(IOBase):
    input_spec = MergeColumnsInputSpec
    output_spec = TsvOutputSpec

    def __init__(self, numinputs=0, **inputs):
        super(MergeColumns, self).__init__(**inputs)
        self._numinputs = numinputs
        if numinputs >= 1:
            input_names = ["in%d" % (i + 1) for i in range(numinputs)]
            add_traits(self.inputs, input_names, trait_type=File)
            input_names = ["column_names%d" % (i + 1) for i in range(numinputs)]
            add_traits(self.inputs, input_names)
        else:
            input_names = []



class SelectColumnsInputSpec(TraitedSpec):
    in_file = File(exists=True, desc="input tsv file")
    column_names = traits.List(traits.Str, desc="list of column names, can be regular expressions")


class SelectColumns(SimpleInterface):
    """
    Select columns to make a design matrix
    """

    input_spec = SelectColumnsInputSpec
    output_spec = TsvOutputSpec

