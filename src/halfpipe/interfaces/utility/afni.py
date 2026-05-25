# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

from pathlib import Path

import numpy as np
import pandas as pd
from nipype.interfaces.base import File, SimpleInterface, TraitedSpec, isdefined, traits

from ...ingest.spreadsheet import read_spreadsheet
from ...utils.path import split_ext


class ToAFNIInputSpec(TraitedSpec):
    in_file = File(exists=True, mandatory=True)


class ToAFNIOutputSpec(TraitedSpec):
    out_file = File(exists=True)
    metadata = traits.Any()


class ToAFNI(SimpleInterface):
    """convert to afni 1d format if necessary"""

    input_spec = ToAFNIInputSpec
    output_spec = ToAFNIOutputSpec



class FromAFNIInputSpec(TraitedSpec):
    in_file = File(exists=True)
    metadata = traits.Any()


class FromAFNIOutputSpec(TraitedSpec):
    out_file = File(exists=True)


class FromAFNI(SimpleInterface):
    """convert from afni 1d format if necessary"""

    input_spec = FromAFNIInputSpec
    output_spec = FromAFNIOutputSpec

