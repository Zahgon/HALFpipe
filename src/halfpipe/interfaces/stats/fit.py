# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import os

from nipype.interfaces.base import (
    DynamicTraitedSpec,
    File,
    InputMultiPath,
    isdefined,
    traits,
)
from nipype.interfaces.io import IOBase, add_traits

from ...stats.algorithms import algorithms, make_algorithms_dict
from ...stats.fit import fit
from .design import DesignSpec


class ModelFitInputSpec(DesignSpec):
    cope_files = InputMultiPath(
        File(exists=True),
        mandatory=True,
    )
    var_cope_files = InputMultiPath(
        File(exists=True),
        mandatory=False,
    )
    mask_files = InputMultiPath(
        File(exists=True),
        mandatory=True,
    )

    algorithms_to_run = traits.List(
        traits.Enum(*algorithms.keys()),
        value=["flame1"],
        usedefault=True,
    )

    num_threads = traits.Int(1, usedefault=True)


class ModelFit(IOBase):
    input_spec = ModelFitInputSpec
    output_spec = DynamicTraitedSpec

    def __init__(self, **inputs):
        super(ModelFit, self).__init__(**inputs)
        self._results = dict()



