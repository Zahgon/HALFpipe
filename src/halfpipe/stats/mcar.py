# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import warnings

import numpy as np
import statsmodels.api as sm
from statsmodels.tools.sm_exceptions import (
    PerfectSeparationError,
    PerfectSeparationWarning,
)

from .base import demean
from .heterogeneity import Heterogeneity
from .miscmaths import chisq2z_convert


class MCARTest(Heterogeneity):
    model_outputs = ["mcarchisq", "mcardof", "mcarz"]
    contrast_outputs: list[str] = []

