# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

from copy import copy
from logging import Handler

from .worker.message import LogMessage


class QueueHandler(Handler):
    def __init__(self, queue):
        super(QueueHandler, self).__init__()
        self.queue = queue

