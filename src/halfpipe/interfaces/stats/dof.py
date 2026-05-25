# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

from os import path as op

import nibabel as nib
import numpy as np
from nilearn.image import new_img_like
from nipype.interfaces.base import BaseInterface, File, TraitedSpec, isdefined, traits

from ...utils.image import nvol
from ...utils.matrix import ncol
from ...utils.ops import first_str


class MakeDofVolumeInputSpec(TraitedSpec):
    dof_file = File(desc="", exists=True)
    copes = traits.Either(traits.List(File(exists=True)), File(exists=True))

    bold_file = File(exists=True, desc="input file")
    num_regressors = traits.Range(low=1, desc="number of regressors")
    design = File(desc="", exists=True)


class MakeDofVolumeOutputSpec(TraitedSpec):
    out_file = File(exists=True)


class MakeDofVolume(BaseInterface):
    input_spec = MakeDofVolumeInputSpec
    output_spec = MakeDofVolumeOutputSpec


