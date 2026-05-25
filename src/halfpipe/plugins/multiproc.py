# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import gc
import os
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count
from threading import Thread
from typing import Any

import nipype.pipeline.engine as pe
from matplotlib import pyplot as plt
from nipype.pipeline import plugins as nip
from nipype.utils.gpu_count import gpu_count
from nipype.utils.profiler import get_system_total_memory_gb
from stackprinter import format_current_exception

from ..logging import logger
from ..utils.multiprocessing import get_init_args, mp_context
from .reftracer import PathReferenceTracer




# Run node
def run_node(node: pe.Node, updatehash: bool, taskid: int):
    """Function to execute node.run(), catch and log any errors and
    return the result dictionary
    Parameters
    ----------
    node : nipype Node instance
        the node to run
    updatehash : boolean
        flag for updating hash
    taskid : int
        an identifier for this task
    Returns
    -------
    result : dictionary
        dictionary containing the node runtime results and stats
    """
    pass


class MultiProcPlugin(nip.MultiProcPlugin):
    def __init__(self, plugin_args: dict):
        # Init variables and instance attributes
        super(nip.MultiProcPlugin, self).__init__(plugin_args=plugin_args)
        self._taskresult: dict = dict()
        self._task_obj: dict = dict()
        self._taskid = 0
        self._rt = None

        # Cache current working directory and make sure we
        # change to it when workers are set up
        self._cwd: str = plugin_args.get("workdir", os.getcwd())

        # Read in options or set defaults.
        self.processors = self.plugin_args.get("n_procs", cpu_count())
        self.memory_gb = self.plugin_args.get(
            "memory_gb",
            get_system_total_memory_gb() * 0.9,  # Allocate 90% of system memory
        )
        self.raise_insufficient = self.plugin_args.get("raise_insufficient", True)

        # GPU handling for compatibility with Nipype ≥1.10
        self.n_gpus_visible = gpu_count()  # default is the available GPUs
        self.n_gpu_procs = plugin_args.get("n_gpu_procs", self.n_gpus_visible)  # allow to override by user

        # Instantiate different thread pools for non-daemon processes
        logger.debug(
            "[MultiProc] Starting (n_procs=%d, n_gpu_procs=%d, mem_gb=%0.2f, cwd=%s)",
            self.processors,
            self.n_gpu_procs,
            self.memory_gb,
            self._cwd,
        )

        self.pool = ProcessPoolExecutor(
            max_workers=self.processors,
            initializer=initializer,  # type: ignore
            initargs=(get_init_args(), plugin_args),  # type: ignore
            mp_context=mp_context,
        )

        self._stats = None
        self._keep = plugin_args.get("keep", "all")
        if self._keep != "all":
            self._rt = PathReferenceTracer(self._cwd)






    def _remove_node_dirs(self):
        """
        Removes directories whose outputs have already been used up
        """
        pass
