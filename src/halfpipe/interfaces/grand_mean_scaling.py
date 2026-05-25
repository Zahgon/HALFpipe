# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import logging

import numpy as np
from nipype.interfaces.base import (
    BaseInterfaceInputSpec,
    File,
    TraitedSpec,
    isdefined,
    traits,
)

from .array_transform import ArrayTransform


class GrandMeanScalingInputSpec(BaseInterfaceInputSpec):
    files = traits.List(File(exists=True), mandatory=True)
    mask = File(exists=True, desc="3D brain mask")
    mean = traits.Float(mandatory=True, desc="grand mean scale value")


class GrandMeanScalingOutputSpec(TraitedSpec):
    files = traits.List(File(exists=True))


class GrandMeanScaling(ArrayTransform):
    """
    Scale voxel values in every image by dividing
    the average global mean intensity of the whole session.
    Applies the scaling factor of the first file to the other files
    in in_files
    """

    scaling_factor: float | None

    input_spec = GrandMeanScalingInputSpec
    output_spec = GrandMeanScalingOutputSpec

    suffix = "grandmeanscaled"


