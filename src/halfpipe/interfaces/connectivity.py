# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

from os import path as op

import nibabel as nib
import numpy as np
import pandas as pd
from nipype.interfaces.base import (
    BaseInterface,
    BaseInterfaceInputSpec,
    File,
    TraitedSpec,
    traits,
)
from nipype.interfaces.base.support import Bunch

from ..signals import mean_signals

savetxt_argdict = dict(fmt="%.10f", delimiter="\t")


class ConnectivityMeasureInputSpec(BaseInterfaceInputSpec):
    in_file = File(desc="Image file(s) from where to extract the data", exists=True, mandatory=True)
    mask_file = File(desc="Mask file", exists=True, mandatory=True)
    atlas_file = File(
        desc="Atlas image file defining the connectivity ROIs",
        exists=True,
        mandatory=True,
    )

    background_label = traits.Int(desc="", default=0, usedefault=True)
    min_region_coverage = traits.Float(desc="", default=0.8, usedefault=True)


class ConnectivityMeasureOutputSpec(TraitedSpec):
    time_series = File(desc="Numpy text file with the timeseries matrix")
    covariance = File(desc="Numpy text file with the connectivity matrix")
    correlation = File(desc="Numpy text file with the connectivity matrix")
    region_coverage = traits.List(traits.Float)


class ConnectivityMeasure(BaseInterface):
    """
    Nipype interfaces to calculate connectivity measures using nilearn.
    Adapted from https://github.com/Neurita/pypes
    """

    input_spec = ConnectivityMeasureInputSpec
    output_spec = ConnectivityMeasureOutputSpec


