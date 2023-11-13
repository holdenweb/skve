from typing import Optional

from rich.text import Text
from textual.app import App
from textual.app import ComposeResult
from textual.containers import Center
from textual.containers import Horizontal
from textual.containers import Vertical
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.validation import Validator
from textual.widget import Widget
from textual.widgets import Button
from textual.widgets import Input
from textual.widgets import Label
from textual.widgets import Static
from textual.widgets import TextArea

from textutils.key_value_edit import KeyValueEditScreen

class ResultRow(Widget):

    def __init__(
        self,
        key,
        value,
        clickable=True,
        validators: Optional[list[Validator]] = None,
        widget_type: Widget = Input,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.key = key
        self.value = value
        self.clickable = clickable
        self.validators = validators if validators is not None else []
        self.bg_class = next(self.app.bg_class)
        self.widget_type = widget_type
        self.classes = f'result-row {self.bg_class}'
        self.key_field = Static(classes=f'key {self.bg_class}')
        self.value_field = Static(classes=f'value {self.bg_class}')

    def on_click(self, e):
        if self.clickable:
            self.app.push_screen(
                KeyValueEditScreen(
                    self.key,
                    self.value,
                    validators=self.validators,
                    widget_type=self.widget_type,
                ),
                self.stash_result,
            )

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Vertical(self.key_field, classes='key-col')
            yield Vertical(self.value_field, classes='value-col')

    def on_mount(self):
        self.update()

    def stash_result(self, return_value):
        if return_value is not None:
            # Some redundant code
            self.key, self.value = return_value
            self.key = self.key.lower()
            self.update()

    def update(self):
        self.key_field.update(
            Text(text=self.key.capitalize(), style='bold white'),
        )
        self.value_field.update(Text(text=self.value))
