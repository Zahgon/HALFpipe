# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import hashlib
import json
import re
from os import path as op
from pathlib import Path

from nipype.interfaces.base import SimpleInterface, TraitedSpec, traits

from ...logging import logger
from ...model.tags import FuncTagsSchema
from ...resource import get as getresource
from ...result.bids.base import make_bids_path
from ...result.bids.images import save_images
from ...result.variables import Continuous
from ...utils.path import copy_if_newer, find_paths
from ...utils.table import SynchronizedTable












class ResultdictDatasinkInputSpec(TraitedSpec):
    base_directory = traits.Directory(desc="Path to the base directory for storing data.", mandatory=True)
    indicts = traits.List(traits.Dict(traits.Str(), traits.Any()))


class ResultdictDatasink(SimpleInterface):
    input_spec = ResultdictDatasinkInputSpec
    output_spec = TraitedSpec

    always_run: bool = True

