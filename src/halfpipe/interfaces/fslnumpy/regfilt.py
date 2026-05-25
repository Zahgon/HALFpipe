# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import warnings

import numpy as np
import scipy.stats
from nipype.interfaces.base import File, isdefined, traits
from numpy import typing as npt

from ...logging import logger
from ..array_transform import ArrayTransform, ArrayTransformInputSpec


def binarize(array, lowerth, upperth, threstype="inclusive", invert: bool = False):
    """
    numpy translation of fsl newimage.cc binarise
    default arguments come from newimagefns.h:142
    """
    pass


def regfilt(
    array: npt.NDArray[np.float64],
    design: npt.NDArray[np.float64],
    comps: list[int],
    calculate_mask: bool = True,
    aggressive: bool = False,
) -> npt.NDArray:
    """
    numpy translation of fsl fsl_regfilt.cc dofilter
    """
    pass


class FilterRegressorInputSpec(ArrayTransformInputSpec):
    design_file = File(desc="design file", exists=True, mandatory=True)
    filter_columns = traits.List(traits.Int)
    filter_all = traits.Bool(default_value=False, usedefault=True)
    mask = traits.Either(
        File(desc="mask image file name", exists=True),
        traits.Bool(),
        default=True,
        usedefault=True,
    )
    aggressive = traits.Bool(default_value=False, usedefault=True)


class FilterRegressor(ArrayTransform):
    input_spec = FilterRegressorInputSpec

    suffix = "regfilt"

