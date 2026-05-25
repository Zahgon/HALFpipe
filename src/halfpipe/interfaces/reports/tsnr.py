# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import numpy as np
from nipype.interfaces.base import isdefined, traits
from numba import guvectorize
from numpy import typing as npt

from ..array_transform import ArrayTransform, ArrayTransformInputSpec




class TSNRInputSpec(ArrayTransformInputSpec):
    dummy_scans = traits.Int(default=0, usedefault=True)


class TSNR(ArrayTransform):
    input_spec = TSNRInputSpec
    suffix = "tsnr"

