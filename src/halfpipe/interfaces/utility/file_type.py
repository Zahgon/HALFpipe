# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

from nipype.interfaces.base import File, SimpleInterface, TraitedSpec, isdefined, traits
from nipype.interfaces.base.support import Bunch

from ...utils.path import split_ext


class SplitByFileTypeInputSpec(TraitedSpec):
    files = traits.List(File(exists=True))


class SplitByFileTypeOutputSpec(TraitedSpec):
    tsv_files = traits.List(File(exists=True))
    nifti_files = traits.List(File(exists=True))


class SplitByFileType(SimpleInterface):
    input_spec = SplitByFileTypeInputSpec
    output_spec = SplitByFileTypeOutputSpec

