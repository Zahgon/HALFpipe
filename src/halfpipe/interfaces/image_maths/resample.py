# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

from pathlib import Path
from typing import Literal

import nibabel as nib
import numpy as np
from nipype.interfaces.base import File, InputMultiObject, isdefined, traits
from templateflow.api import get as get_template

from ...resource import get as getresource
from ...utils.image import nvol
from ..fixes.applytransforms import ApplyTransforms, ApplyTransformsInputSpec


class ResampleInputSpec(ApplyTransformsInputSpec):
    input_space = traits.Either("MNI152NLin6Asym", "MNI152NLin2009cAsym", mandatory=False)
    reference_space = traits.Either("MNI152NLin6Asym", "MNI152NLin2009cAsym", mandatory=False)
    reference_res = traits.Int(requires=["reference_space"], mandatory=False)
    lazy = traits.Bool(default=True, usedefault=True, desc="only resample if necessary")

    # make not mandatory as these inputs will be computed from other inputs
    reference_image = File(
        argstr="--reference-image %s",
        mandatory=False,
        desc="reference image space that you wish to warp INTO",
        exists=True,
    )
    transforms = InputMultiObject(
        traits.Either(File(exists=True), "identity"),
        argstr="%s",
        mandatory=False,
        desc="transform files: will be applied in reverse order. For "
        "example, the last specified transform will be applied first.",
    )


class Resample(ApplyTransforms):
    input_spec = ResampleInputSpec


