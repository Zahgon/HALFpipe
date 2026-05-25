# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

from nipype.interfaces.ants.resampling import (
    ApplyTransformsInputSpec as NipypeApplyTransformsInputSpec,
)
from nipype.interfaces.base import File
from niworkflows.interfaces.fixes import FixHeaderApplyTransforms


class ApplyTransformsInputSpec(NipypeApplyTransformsInputSpec):
    input_image = File(
        argstr="--input %s",
        mandatory=False,
        desc="image to apply transformation to",
        exists=True,
    )


class ApplyTransforms(FixHeaderApplyTransforms):
    input_spec = ApplyTransformsInputSpec

