# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import numpy as np
from nipype.interfaces.base import traits
from numpy import typing as npt

from ..array_transform import ArrayTransform, ArrayTransformInputSpec


def bandpass_temporal_filter(array, hp_sigma, lp_sigma):
    """
    numpy translation of fsl newimagefuns.h bandpass_temporal_filter
    """
    pass


class TemporalFilterInputSpec(ArrayTransformInputSpec):
    lowpass_sigma = traits.Float(default=-1, usedefault=True)
    highpass_sigma = traits.Float(default=-1, usedefault=True)


class TemporalFilter(ArrayTransform):
    input_spec = TemporalFilterInputSpec

    suffix = "bptf"

