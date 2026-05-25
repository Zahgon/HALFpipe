# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import numpy as np
from nipype.interfaces.base import File

from ..array_transform import ArrayTransform, ArrayTransformInputSpec


class AddMeansInputSpec(ArrayTransformInputSpec):
    mean_file = File(exists=True, mandatory=True)


class AddMeans(ArrayTransform):
    input_spec = AddMeansInputSpec

    suffix = "addmean"

