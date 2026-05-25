# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

from os.path import relpath
from pathlib import Path

from nipype.interfaces import afni

from ...utils.path import split_ext


class ReHo(afni.ReHo):
    """
    3dReHo supports paths up to 300 characters
    Sometimes we have longer paths
    Therefore, use a symlink
    """

