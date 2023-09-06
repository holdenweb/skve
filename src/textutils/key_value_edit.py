from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, Center
from textual.widgets import Input, TextArea, Button, Static
from textual.screen import ModalScreen

from textutils.lib import SaveCancel

class KeyValueEditScreen(ModalScreen):

    DEFAULT_CSS = """\
KeyValueEditScreen {
    background: $primary 100%;
}

#input-value {
    width: 7fr;
    height: auto;
    min-height: 5;
    border: yellow 100%;
    background: $primary 100%;
}

#input-key {
    width: 7fr;
    border: yellow 100%;
    background: $primary 100%;
}

.title {
    text-style: bold;
    width: 1fr;
}
"""

    def __init__(self, key, value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key = key
        self.value = value
        self.key_field = Input(id="input-key")
        self.value_field = TextArea(id="input-value")
        self.value_field.show_line_numbers = False

    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Horizontal(
                Static("Key", classes="title"),
                self.key_field
            )
            yield Horizontal(
                Static("Value", classes="title"),
                self.value_field
            )
            yield SaveCancel(self.callback)

    def callback(self, save):
        retval = (self.key_field.value, self.value_field.text) if save else None
        self.dismiss(retval)  # Assumes parent screen will capture this result

    def on_mount(self):
        self.key_field.value = self.key
        self.value_field.load_text(self.value)
        self.refresh()
