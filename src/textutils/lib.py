from textual.widget import Widget
from textual.widgets import Button
from rich.text import Text
from textual.containers import Center, Horizontal

class DeleteMe(Button):
    CSS = """DeleteMe {
    width: 1; height: 1;
    }
    """
    def __init__(self, *args, **kw):
        super().__init__("x", *args, **kw)


class YesNoText(Text):

    def __init__(self, msg, yes_action, no_action, *args, **kw):
        super().__init__(msg, *args, **kw)
        self.msg = msg
        self.yes_action = yes_action
        self.no_action = no_action

    def render(self):
        return Text.from_markup(f"{self.msg}: [@click='{self.yes_action}']yes[/] [@click='{self.no_action}']no[/]")


class SaveCancel(Widget):

    def __init__(self, callback, *args, **kw):
        super().__init__(*args, **kw)
        self.callback = callback

    def compose(self):
        with Center(classes=f"id-{self.id} save-cancel-button-row"):
            with Horizontal(classes=f"id-{self.id} save-cancel-buttons"):
                yield Button("Save", variant="primary", classes=f"save id-{self.id} save-cancel-save-button")
                yield Button("Cancel", variant="error", classes=f"cancel id-{self.id} save-cancel-cancel-button")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.callback("save" in event.button.classes)

    DEFAULT_CSS = """\
SaveCancel {
    height: auto;
}
.save-cancel-button-row {
    min-height: 3;
}

.save-cancel-buttons {
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