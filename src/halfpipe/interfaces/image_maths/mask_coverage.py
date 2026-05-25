# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

from pathlib import Path

import nibabel as nib
import numpy as np
from nilearn.image import new_img_like
from nipype.interfaces.base import (
    DynamicTraitedSpec,
    File,
    InputMultiPath,
    OutputMultiPath,
    isdefined,
    traits,
)
from nipype.interfaces.io import IOBase, add_traits

from ...utils.path import split_ext


class MaskCoverageInputSpec(DynamicTraitedSpec):
    in_files = InputMultiPath(File(exists=True), desc="Input files", mandatory=True)

    mask_file = File(desc="Mask file", exists=True, mandatory=True)

    min_coverage = traits.Float(1.0)


class MaskCoverageOutputSpec(DynamicTraitedSpec):
    out_files = OutputMultiPath(File(exists=True))
    coverage = traits.List(traits.Float)


class MaskCoverage(IOBase):
    input_spec = MaskCoverageInputSpec
    output_spec = MaskCoverageOutputSpec

    def __init__(self, keys: list[str] | None = None, **inputs):
        super(MaskCoverage, self).__init__(**inputs)
        if keys is None:
            keys = list()
        self._keys = keys
        add_traits(self.inputs, keys)



