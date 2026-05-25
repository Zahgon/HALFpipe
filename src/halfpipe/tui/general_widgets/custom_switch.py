# -*- coding: utf-8 -*-
from math import ceil
from typing import ClassVar, Type

from rich.color import Color
from rich.console import RenderableType
from rich.segment import Segment, Segments
from rich.style import Style
from textual.scrollbar import ScrollBarRender
from textual.widget import Widget
from textual.widgets._switch import Switch  # Make sure this import path is correct based on your project structure


class MyScrollBarRender(ScrollBarRender):
    """
    Renders the scrollbar with ON/OFF text. For more see ScrollBarRender.
    """



class MyScrollBar(Widget):
    """
    This is just needed so that we can provide the modified rendered. `MyScrollBarRender`
    """

    renderer: ClassVar[Type[ScrollBarRender]] = MyScrollBarRender


class TextSwitch(Switch):
    """
    TextSwitch(Switch)

    A custom switch that renders ON/OFF labels over the colored bars. Essenstially
    is the same as parent `Switch` the renderer needed small modifications. Hence
    the function `render` is here overriding the oroginal function only to reroute
    the renderer to the custom one. The `watch_value` needed different duration
    times as original, hence it is also here.

    Methods
    -------
    render() -> RenderableType
        Renders the switch component with a scrollbar UI.

    watch_value(value: bool) -> None
        Updates the slider position based on the switch value with optional animation.
    """

    DEFAULT_CSS = """
        TextSwitch {
            border: tall transparent;
            height: 3;
            width: 16;
            padding: 0 2;
        }
    """

    def render(self) -> RenderableType:
        style = self.get_component_rich_style("switch--slider")
        return MyScrollBarRender(
            virtual_size=100,
            window_size=50,
            position=self._slider_position * 50,
            style=style,
            vertical=False,
        )

