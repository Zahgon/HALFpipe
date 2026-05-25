# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

from math import prod
from pathlib import Path

import nibabel as nib
import numpy as np
import pandas as pd
from nilearn.image import new_img_like
from nipype.interfaces.base import File, SimpleInterface, TraitedSpec, isdefined, traits
from numpy import typing as npt

from ..ingest.spreadsheet import read_spreadsheet
from ..utils.path import split_ext


class ArrayTransformInputSpec(TraitedSpec):
    in_file = File(desc="File to filter", exists=True, mandatory=True)
    mask = File(desc="mask to use for volumes", exists=True)

    write_header = traits.Bool(default_value=True, usedefault=True)


class ArrayTransformOutputSpec(TraitedSpec):
    out_file = File()


class ArrayTransform(SimpleInterface):
    """
    Interface that takes any kind of array input and applies a function to it
    """

    input_spec = ArrayTransformInputSpec
    output_spec = ArrayTransformOutputSpec

    suffix = "transformed"

    def _transform(self, array: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        raise NotImplementedError



