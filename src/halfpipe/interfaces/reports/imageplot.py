# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

from os import path as op
from typing import Any
from uuid import uuid4

import nibabel as nib
import numpy as np
from matplotlib import colormaps
from nilearn.plotting import plot_anat, plot_epi
from nipype.interfaces.base import File, isdefined, traits
from nireports.interfaces.reporting.base import (
    ReportingInterface,
    _SVGReportCapableInputSpec,
)
from niworkflows.viz.utils import (
    compose_view,
    cuts_from_bbox,
    extract_svg,
    robust_set_limits,
)
from seaborn import color_palette
from svgutils.transform import fromstring

from ...resource import get as getresource
from ...utils.image import nvol




class PlotInputSpec(_SVGReportCapableInputSpec):
    in_file = File(exists=True, mandatory=True, desc="volume")
    mask_file = File(exists=True, mandatory=True, desc="mask")
    label = traits.Str()


class PlotEpi(ReportingInterface):
    input_spec = PlotInputSpec



class PlotRegistrationInputSpec(PlotInputSpec):
    template = traits.Str(mandatory=True)


class PlotRegistration(ReportingInterface):
    input_spec = PlotRegistrationInputSpec

