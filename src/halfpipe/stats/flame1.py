# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

from collections import defaultdict
from typing import Any, Literal, NamedTuple

import nibabel as nib
import numpy as np
import pandas as pd
import scipy
from numba import njit
from numpy import typing as npt

from ..utils.format import format_workflow
from .base import ModelAlgorithm, demean, listwise_deletion
from .miscmaths import f2z_convert, t2z_convert












class TContrastResult(NamedTuple):
    cope: float
    var_cope: float
    t: float
    z: float




class FContrastResult(NamedTuple):
    cope: npt.NDArray[np.floating]
    var_cope: npt.NDArray[np.floating]
    t: npt.NDArray[np.floating]
    f: float
    z: float






def flame1_prepare_data(y: np.ndarray, z: np.ndarray, s: np.ndarray):
    # Filtering for design matrix is already done,
    # so the nans that are left should be replaced with zeros.
    z = np.nan_to_num(z)

    # If we don't have any variance information, set it to zero.
    if np.isnan(s).all():
        s[:] = 0

    # Remove observations with nan cope/varcope
    y, z, s = listwise_deletion(y, z, s)

    # finally demean the design matrix
    z = demean(z)

    return y, z, s


class FLAME1(ModelAlgorithm):
    model_outputs: list[str] = []
    contrast_outputs = [
        "copes",
        "var_copes",
        "zstats",
        "tstats",
        "fstats",
        "dof",
        "masks",
    ]


    @classmethod
    def write_outputs(
        cls,
        reference_image: nib.analyze.AnalyzeImage,
        contrast_matrices: dict,
        voxel_results: dict,
    ) -> dict[str, list[Literal[False] | str]]:
        output_files: dict[str, list[Literal[False] | str]] = dict()

        for output_name in cls.contrast_outputs:
            output_files[output_name] = [False] * len(contrast_matrices)

        for i, contrast_name in enumerate(contrast_matrices.keys()):  # cmatdict is ordered
            contrast_results = voxel_results[contrast_name]
            results_frame = pd.DataFrame.from_records(contrast_results)

            # Ensure that we always output a mask
            if "mask" not in results_frame.index:
                empty_mask = pd.Series(data=False, index=results_frame.columns, name="mask")
                results_frame = results_frame.append(empty_mask)  # type: ignore
            # Ensure that we always output a zstat
            if "zstat" not in results_frame.index:
                empty_zstat = pd.Series(data=np.nan, index=results_frame.columns, name="zstat")
                results_frame = results_frame.append(empty_zstat)  # type: ignore

            for map_name, series in results_frame.iterrows():
                output_prefix = f"{map_name}_{i + 1}_{format_workflow(contrast_name)}"
                fname = cls.write_map(reference_image, output_prefix, series)

                if map_name in frozenset(["dof"]):
                    output_name = str(map_name)

                else:
                    output_name = f"{map_name}s"

                if output_name in output_files:
                    output_files[output_name][i] = str(fname)

        return output_files
