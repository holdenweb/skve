from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widget import Widget
from textual.widgets import Input, Static, Label, Pretty
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
    min-height: 1;
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


    def __init__(
        self,
        key,
        value,
        validators=(),
        editable_key=False,
        widget_type: Widget = Static,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.key = key
        self.value = value
        self.editable_key = editable_key
        self.widget_type = widget_type

        self.key_field = (
            Input(id="input-key") if editable_key else Label(key, id="input-key")
        )
        self.value_field = self.widget_type(id="input-value")  # ,  validators=validators)

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
            yield Static("", id="kve-msg")
            yield SaveCancel(self.callback)

    def on_input_changed(self, event: Input.Changed) -> None:
        # Updating the UI to show the reasons why validation failed
        if event.validation_result is None:
            return
        newline = "\n"
        if not event.validation_result.is_valid:
            if event.validation_result.failure_descriptions:
                self.app.notify(f"**** VALIDATION FAILURE ****{newline}{newline.join(msg for msg in event.validation_result.failure_descriptions)}")
        else:
            self.query_one("#kde-msg").update("Validates OK")

    def callback(self, save):
        retval = (self.key_field.value, self.value_field.value) if save else None
        self.dismiss(retval)  # Parent screen should capture this result

    def on_mount(self):
        self.key_field.value = self.key
        self.value_field.value = self.value
        self.refresh()
