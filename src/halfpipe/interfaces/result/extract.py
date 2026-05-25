# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

from nipype.interfaces.base import BaseInterfaceInputSpec, DynamicTraitedSpec, traits
from nipype.interfaces.io import IOBase, add_traits

from ...model.resultdict import ResultdictSchema


class ExtractFromResultdictInputSpec(BaseInterfaceInputSpec):
    indict = traits.Dict(traits.Str(), traits.Any())


class ExtractFromResultdictOutputSpec(DynamicTraitedSpec):
    tags = traits.Dict(traits.Str(), traits.Any())
    metadata = traits.Dict(traits.Str(), traits.Any())
    vals = traits.Dict(traits.Str(), traits.Any())


class ExtractFromResultdict(IOBase):
    input_spec = ExtractFromResultdictInputSpec
    output_spec = ExtractFromResultdictOutputSpec

    def __init__(self, keys: list | None = None, aliases: dict | None = None, **inputs):
        super(ExtractFromResultdict, self).__init__(**inputs)

        self._keys = [] if keys is None else keys
        self._aliases = {} if aliases is None else aliases


