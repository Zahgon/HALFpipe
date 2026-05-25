# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

from nipype.interfaces.base import File, SimpleInterface, TraitedSpec, traits

from ...design import (
    group_design,
    intercept_only_design,
    make_design_tsv,
    prepare_data_frame,
)


class GroupDesignInputSpec(TraitedSpec):
    spreadsheet = File(exist=True, mandatory=True)
    contrastdicts = traits.List(
        traits.Dict(traits.Str, traits.Any),
        mandatory=True,
    )
    variabledicts = traits.List(
        traits.Dict(traits.Str, traits.Any),
        mandatory=True,
    )
    subjects = traits.List(traits.Str, mandatory=True)


class DesignOutputSpec(TraitedSpec):
    regressors = traits.Dict(traits.Str, traits.Any)
    contrasts = traits.List()
    contrast_numbers = traits.List(traits.Str())
    contrast_names = traits.List(traits.Str())


class GroupDesign(SimpleInterface):
    """interface to construct a group design"""

    input_spec = GroupDesignInputSpec
    output_spec = DesignOutputSpec



class InterceptOnlyDesignInputSpec(TraitedSpec):
    n_copes = traits.Range(low=1, desc="number of inputs")


class InterceptOnlyDesign(SimpleInterface):
    """interface to construct a group design"""

    input_spec = InterceptOnlyDesignInputSpec
    output_spec = DesignOutputSpec



class DesignSpec(TraitedSpec):
    regressors = traits.Dict(
        traits.Str,
        traits.List(traits.Float),
        mandatory=True,
    )
    contrasts = traits.List(
        traits.Either(
            traits.Tuple(
                traits.Str,
                traits.Enum("T"),
                traits.List(traits.Str),
                traits.List(traits.Float),
            ),
            traits.Tuple(
                traits.Str,
                traits.Enum("F"),
                traits.List(
                    traits.Tuple(
                        traits.Str,
                        traits.Enum("T"),
                        traits.List(traits.Str),
                        traits.List(traits.Float),
                    ),
                ),
            ),
        ),
        mandatory=True,
    )


class MakeDesignTsvInputSpec(DesignSpec):
    row_index = traits.Any(mandatory=True)


class MakeDesignTsvOutputSpec(TraitedSpec):
    design_tsv = File(exists=True)
    contrasts_tsv = File(exists=True)


class MakeDesignTsv(SimpleInterface):
    input_spec = MakeDesignTsvInputSpec
    output_spec = MakeDesignTsvOutputSpec

