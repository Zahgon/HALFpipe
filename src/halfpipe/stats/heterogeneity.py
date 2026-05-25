# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

from typing import NamedTuple

import nibabel as nib
import numpy as np
import pandas as pd
import scipy
from numpy import typing as npt

from ..logging import logger
from .base import ModelAlgorithm
from .flame1 import flame1_prepare_data


def method_of_moments_i_squared(
    y: npt.NDArray[np.float64],
    z: npt.NDArray[np.float64],
    s: npt.NDArray[np.float64],
) -> float:
    """
    Chen et al. 2012
    """
    pass


class ReMLTerms(NamedTuple):
    inverse_variance: npt.NDArray[np.float64]
    projection_matrix: npt.NDArray[np.float64]
    gram_matrix: npt.NDArray[np.float64]
























class Heterogeneity(ModelAlgorithm):
    model_outputs: list[str] = [
        "hetnorm",
        "hetbeta",
        "hetgamma",
        "hettypical",
        "heti2",
        "hetpseudor2",
        "hetchisq",
    ]
    contrast_outputs: list[str] = []


    @classmethod
    def write_outputs(cls, reference_image: nib.analyze.AnalyzeImage, contrast_matrices: dict, voxel_results: dict) -> dict:
        output_files = dict()

        rdf = pd.DataFrame.from_records(voxel_results)

        for map_name, series in rdf.iterrows():
            assert isinstance(map_name, str)

            fname = cls.write_map(reference_image, map_name, series)
            output_files[map_name] = str(fname)

        return output_files
