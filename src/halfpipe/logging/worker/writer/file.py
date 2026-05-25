# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import re
from pathlib import Path
from random import gauss
from typing import IO

from ....utils.lock import AdaptiveLock
from .base import Writer

escape_codes_regex = re.compile(r"\x1b\[.*?(m|K)")


class FileWriter(Writer, AdaptiveLock):
    def __init__(self, **kwargs) -> None:
        Writer.__init__(self, **kwargs)
        AdaptiveLock.__init__(self)
        self.filename: Path | None = None
        self.stream: IO[str] | None = None


    def check(self) -> bool:
        if self.filename is None or not isinstance(self.filename, Path):
            return False

        return True



