# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

from argparse import Namespace
from collections import defaultdict
from dataclasses import dataclass
from functools import cached_property, partial
from pathlib import Path
from shutil import copyfile
from tempfile import TemporaryDirectory
from typing import Callable, Mapping

import nibabel as nib
import numpy as np
import pandas as pd
import pint
from tqdm import tqdm

from ....collect.derivatives import find_derivatives_directories
from ....exclude import Decision
from ....file_index.bids import BIDSIndex
from ....logging import logger
from ....model.tags.resultdict import resultdict_entities
from ....result.bids.base import make_bids_prefix
from ....result.variables import Continuous
from ....utils.multiprocessing import make_pool_or_null_context
from ....utils.nipype import run_workflow
from ....utils.path import AnyPath
from ....workflows.configurables import configurables
from ....workflows.features.jacobian import init_jacobian_wf
from .design import DesignBase

ureg = pint.UnitRegistry()


def apply_derived(
    arguments: Namespace,
    design_base: DesignBase,
):
    ImagingVariables(
        arguments,
        design_base,
    ).apply()
    design_base.filter_results()
    apply_derived_variables(
        arguments.derived_variable,
        design_base,
    )
    variables_to_drop: list[str] | None = arguments.drop_variable
    if variables_to_drop is not None:
        for name in variables_to_drop:
            design_base.drop_variable(name)


def calculate_jacobian(
    task: tuple[str, AnyPath],
) -> tuple[str, Path | None]:
    """
    Calculates the jacobian for a given subject and transform path using a nipype workflow.
    All files are save din the current directory.

    Args:
        task (tuple[str, Path]): A tuple containing the subject ID and the path to the transformation file.

    Returns:
        tuple[str, Path]: A tuple containing the subject ID and the path to the jacobian file.
    """
    pass


@dataclass
class ImagingVariables:
    arguments: Namespace
    design_base: DesignBase











    def apply(self) -> None:
        arguments = self.arguments
        variable_handlers: Mapping[str, Callable] = dict(
            fd_mean=partial(self.apply_from_vals, "fd_mean"),
            fd_perc=partial(self.apply_from_vals, "fd_perc"),
            mean_gm_tsnr=partial(self.apply_from_vals, "mean_gm_tsnr"),
            aroma_noise_frac=partial(self.apply_from_vals, "aroma_noise_frac"),
            total_intracranial_volume=self.apply_total_intracranial_volume,
            jacobian_mean=partial(self.apply_from_jacobian, "jacobian_mean"),
            jacobian_variance=partial(self.apply_from_jacobian, "jacobian_variance"),
        )
        if arguments.imaging_variable is not None:
            for variable in arguments.imaging_variable:
                variable_handlers[variable]()
        image_handlers: Mapping[str, Callable] = dict(
            jacobian=self.apply_jacobian,
        )
        if arguments.derived_image is not None:
            for image in arguments.derived_image:
                image_handlers[image]()


def apply_derived_variables(
    derived_variables: list[tuple[str, str]] | None,
    design_base: DesignBase,
):
    data_frame = design_base.data_frame
    if derived_variables is None:
        return
    if data_frame is None:
        raise ValueError("Design has no data frame")
    for derived_variable in derived_variables:
        name, expression = derived_variable
        data_frame.eval(f"{name} = ({expression})", inplace=True)
        data_frame[name] = data_frame[name].astype(float)
        # Add contrast for new variable
        design_base.add_variable(name)
