# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import os
from glob import glob
from os import path as op

from nipype.interfaces.base import File, isdefined, traits
from nipype.interfaces.fsl.model import FLAMEO
from nipype.interfaces.fsl.model import FLAMEOInputSpec as NipypeFLAMEOInputSpec
from nipype.utils.misc import human_order_sorted


class FLAMEOInputSpec(NipypeFLAMEOInputSpec):
    cope_file = traits.Either(
        File(exists=True),
        traits.Bool(),
        argstr="--copefile=%s",
        desc="cope regressor data file",
    )
    var_cope_file = traits.Either(
        File(exists=True),
        traits.Bool(),
        argstr="--varcopefile=%s",
        desc="varcope weightings data file",
    )
    dof_var_cope_file = traits.Either(
        File(exists=True),
        traits.Bool(),
        argstr="--dofvarcopefile=%s",
        desc="dof data file for varcope data",
    )
    f_con_file = traits.Either(
        File(exists=True),
        traits.Bool(),
        argstr="--fcontrastsfile=%s",
        desc="ascii matrix specifying f-contrasts",
    )
    mask_file = traits.Either(File(exists=True), traits.Bool(), argstr="--maskfile=%s", desc="mask file")


class FixFLAMEO(FLAMEO):
    """
    Modified to be more robust to filtered out (missing) input files
    These are indicated by the value False
    """

    input_spec = FLAMEOInputSpec



