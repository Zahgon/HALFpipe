# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

from collections import defaultdict
from copy import deepcopy

import nipype.pipeline.engine as pe
from nipype.interfaces.base import InterfaceResult, Undefined, isdefined, traits
from nipype.pipeline.engine.utils import (
    evaluate_connect_function,
    load_resultfile,
    save_resultfile,
)
from nipype.utils.misc import str2bool

from ..logging import logger


class Node(pe.Node):
    _got_inputs: bool

    def __init__(
        self,
        interface,
        name: str,
        keep: bool = False,
        allow_missing_input_source: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(interface, name, **kwargs)
        self.keep: bool = keep
        self.allow_missing_input_source: bool = allow_missing_input_source

    def _get_inputs(self):
        """
        Retrieve inputs from pointers to results files.
        This mechanism can be easily extended/replaced to retrieve data from
        other data sources (e.g., XNAT, HTTP, etc.,.)
        """
        pass


class MapNode(pe.MapNode, Node):
    def __init__(
        self,
        interface,
        iterfield,
        name: str,
        allow_undefined_iterfield: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(interface=interface, iterfield=iterfield, name=name, **kwargs)
        self.allow_undefined_iterfield: bool = allow_undefined_iterfield


