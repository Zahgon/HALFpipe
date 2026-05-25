# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

from contextlib import chdir
from pathlib import Path

from nipype.interfaces import fsl
from tqdm.auto import tqdm

from ....design import intercept_only_design
from ....interfaces.image_maths.merge import merge, merge_mask
from ....logging import logger
from ....result.aggregate import aggregate_results, summarize_metadata
from ....result.base import ResultDict
from ....utils.hash import b32_digest
from ....utils.multiprocessing import make_pool_or_null_context
from .base import aliases
from .design import DesignBase


def apply_aggregate(
    design: DesignBase,
    num_threads: int,
) -> None:
    if design.aggregate is None:
        return

    results = design.results
    for aggregate_key in design.aggregate:
        results, other_results = aggregate_results(results, aggregate_key)

        logger.info(f'Will run {len(results):d} models at level "{aggregate_key}"')
        cm, iterator = make_pool_or_null_context(
            results,
            callable=map_fixed_effects_aggregate,
            num_threads=num_threads,
        )
        with cm:
            results = list(
                tqdm(
                    iterator,
                    total=len(results),
                    desc=f'aggregate "{aggregate_key}"',
                )
            )

        results.extend(other_results)
        for result in results:
            result["tags"] = {
                key: value
                for key, value in result["tags"].items()
                if isinstance(value, str)  # Remove list fields
                and key != aggregate_key  # Remove what we just aggregated over
            }

        results = [summarize_metadata(result) for result in results]

    # Set in design object
    design.results = results


