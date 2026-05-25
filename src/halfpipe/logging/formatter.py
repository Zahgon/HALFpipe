# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import logging
import time

import stackprinter

fmt = "[{asctime},{msecs:04.0f}] [{name:16}] [{levelname:9}] {message}"
datefmt = "%Y-%m-%d %H:%M:%S"

black, red, green, yellow, blue, magenta, cyan, white = range(8)
resetseq = "\x1b[0m"
fillseq = "\x1b[K"
colorseq = "\x1b[{:d};{:d}m"
redseq = colorseq.format(30 + white, 40 + red)
yellowseq = colorseq.format(30 + black, 40 + yellow)
greenseq = colorseq.format(30 + white, 40 + green)
blueseq = colorseq.format(30 + white, 40 + blue)
greyseq = colorseq.format(30 + white, 100 + black)
colors = {
    "DEBUG": greyseq,
    "INFO": blueseq,
    "IMPORTANT": greenseq,
    "WARNING": yellowseq,
    "CRITICAL": redseq,
    "ERROR": redseq,
}


class Formatter(logging.Formatter):
    def __init__(self):
        super(Formatter, self).__init__(fmt=fmt, datefmt=datefmt, style="{")
        self.converter = time.localtime




class ColorFormatter(Formatter):
