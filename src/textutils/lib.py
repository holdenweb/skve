from textual.widget import Widget
from textual.widgets import Button
from textual.containers import Center, Horizontal, Vertical

class SaveCancel(Widget):

    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def compose(self):
        with Center(id="save-cancel-button-row"):
            with Horizontal(id="save-cancel-buttons"):
               yield Button("Save", variant="primary", id="save")
               yield Button("Cancel", variant="error", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        id = event.button.id
        self.callback(id == "save")

    DEFAULT_CSS = """\
SaveCancel {
    height: auto;
}
#save-cancel-button-row {
    min-height: 3;
}

#save-cancel-buttons {
    width: auto;
    height: 3;
}
SaveCancel Horizontal {
    height: 3;
}

SaveCancel Horizontal Button {
    height: 3;
    outline: white 75%;
}
"""