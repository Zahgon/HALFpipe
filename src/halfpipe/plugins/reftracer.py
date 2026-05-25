# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

from collections import defaultdict
from pathlib import Path
from shutil import rmtree

from nipype.pipeline.engine.utils import load_resultfile

from ..logging import logger
from ..utils.path import find_paths, is_empty


class PathReferenceTracer:
    def __init__(self, workdir: str | Path):
        self.workdir: Path = self.resolve(workdir)
        self.weak_references: set[Path] = set()

        self.black: set[Path] = set()  # is pending
        self.grey: set[Path] = set()  # still has references from pending nodes
        self.white: set[Path] = set()

        self.refs: dict[Path, set[Path]] = defaultdict(set)  # other paths that are referenced by a path
        self.deps: dict[Path, set[Path]] = defaultdict(set)  # paths that a path depends on (inverse refs)

    def resolve(self, path) -> Path:
        if not isinstance(path, Path):
            path = Path(path)
        path = path.resolve()
        return path





    def add_file(self, path, target=None):
        if target is None:
            target = self.white

        if path not in self.black and path not in self.grey and path not in self.white:
            target.add(path)





