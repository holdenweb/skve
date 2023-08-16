from textual.app import App, ComposeResult
from textual.validation import Function, Number, ValidationResult, Validator
from textual.widgets import Input, Label, Pretty, Static, Footer, Button
from textual.containers import Container, Horizontal, Vertical, VerticalScroll, Center
import mongoengine

from models import Acronym


class InputApp(App):

    CSS_PATH = "acronyms.css"

    def __init__(self):
        super().__init__()


    def compose(self) -> ComposeResult:
        yield Horizontal(
            Input(
                placeholder="Enter (the beginning of) an acronym...",
                id="in_val,"
                ),
            id="question-box"
        )
        yield Horizontal(
            VerticalScroll(
                id="buttons"
                ),
            VerticalScroll(
                Static(" ".join(f"Label number {n}" for n in range(1000)),
                id="content"
                ),
            id="body"
            )
        )

        yield Center(Label(f"Initial message"), id="message")


    def on_input_changed(self, event: Input.Changed) -> None:
        # Updating the UI to show the reasons why validation failed
        for btn in self.query(Button):
            btn.remove()
        in_string = self.query_one(Input)
        value = in_string.value
        self.me_query = Acronym.objects(acronym__istartswith=value)
        count = self.me_query.count()
        if count == 0:
            self.replace_message("No matches")
        else:
            self.replace_message(f"{self.me_query.count()} acronyms")
            for acr in self.me_query:
                self.query_one("#buttons").mount(
                    Button(acr.acronym)
                )

    def replace_message(self, msg):
        self.query_one("#message").remove()
        self.mount(Center(Label(msg), id="message"))


if __name__ == "__main__":
    app = InputApp()
    dbcon = mongoengine.connect("acronyms")
    app.run()
