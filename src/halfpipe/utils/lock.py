# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import logging
from random import gauss
from time import sleep
from typing import List

from fasteners import InterProcessLock as FcntlLock
from flufl.lock._lockfile import Lock as FluflLock
from flufl.lock._lockfile import LockError as FluflLockError
from flufl.lock._lockfile import TimeOutError


class AdaptiveLock:
    def __init__(self, timeout: int = 180):
        self.timeout = timeout

        self.methods: List[str] = ["fcntl", "hard_links", "delay"]

        self.lock_instance: FcntlLock | FluflLock | None = None


