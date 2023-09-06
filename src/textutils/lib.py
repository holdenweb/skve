from textual.widget import Widget
from textual.widgets import Button
from textual.containers import Center, Horizontal, Vertical

class SaveCancel(Widget):

    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def compose(self):
        with Vertical():
            yield Center(
                Horizontal(
                    Button("Save", variant="primary", id="save"),
                    Button("Cancel", variant="error", id="cancel")
                ),
                id="save-cancel-buttons"
            )
            self.log(self.css_tree)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        id = event.button.id
        self.callback(id == "save")
