# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

from __future__ import annotations

import logging
from multiprocessing.process import BaseProcess
from multiprocessing.queues import JoinableQueue
from pathlib import Path
from threading import RLock
from typing import Any, ClassVar

from ..utils.multiprocessing import mp_context
from .worker import run as run_worker
from .worker.message import (
    DisablePrintMessage,
    EnablePrintMessage,
    EnableVerboseMessage,
    SetWorkdirMessage,
    TeardownMessage,
)

rlock = RLock()


class NullQueue:
    def put(self, _) -> None:
        pass

    def join(self) -> None:
        pass


Queue = NullQueue | JoinableQueue


class Context(object):
    _instance: ClassVar[Context | None] = None

    def __init__(self) -> None:
        self._queue: Queue = NullQueue()
        self._worker: BaseProcess | None = None

    @classmethod
    def instance(cls) -> Context:
        if cls._instance is None:
            with rlock:
                if cls._instance is None:
                    cls._instance = cls()

        return cls._instance



    @classmethod
    def queue(cls) -> Queue:
        return cls.instance()._queue

    @classmethod
    def logging_args(cls) -> dict[str, Any]:
        return dict(queue=cls.queue(), levelno=logging.getLogger("halfpipe").level)

    @classmethod
    def enable_verbose(cls) -> None:
        obj = EnableVerboseMessage()
        queue = cls.queue()
        queue.put(obj)

    @classmethod
    def enable_print(cls) -> None:
        obj = EnablePrintMessage()
        queue = cls.queue()
        queue.put(obj)
        queue.join()

    @classmethod
    def disable_print(cls) -> None:
        obj = DisablePrintMessage()
        queue = cls.queue()
        queue.put(obj)
        queue.join()

    @classmethod
    def set_workdir(cls, workdir: Path) -> None:
        obj = SetWorkdirMessage(workdir=workdir)
        queue = cls.queue()
        queue.put(obj)
