from textual.app import App, ComposeResult
from textual.validation import Function, Number, ValidationResult, Validator
from textual.widgets import Input, Label, Pretty, Static, Footer, Button, DataTable
from textual.containers import Container, Horizontal, HorizontalScroll, Vertical, VerticalScroll, Center
import mongoengine
import importlib.resources as ir
import os
import sys

from .models import Person

os.environ["TEXTUAL"] = "debug,devtools"

class PeopleApp(App):

    CSS_PATH = "people.css"

    def __init__(self):
        super().__init__()


    def compose(self) -> ComposeResult:
        yield Horizontal(
            Label("Name: "),
            Input(
                placeholder="Enter (part of) a person's name...",
                id="in_val,"
                ),
            id="question-box"
        )
        yield Horizontal(
            VerticalScroll(
                id="buttons"
            ),
            VerticalScroll(
                Static("This will be the results"),
                id="content"
            ),
            id="body"
        )

        yield Center(Label(f"Initial message"), id="message")


    def on_input_changed(self, event: Input.Changed) -> None:
        # Updating the UI to show the reasons why validation failed
        for btn in self.query(Button):
            btn.remove()
        in_string = self.query_one(Input)
        value = in_string.value
        self.me_query = Person.objects(name__icontains=value)
        count = self.me_query.count()
        if count == 0:
            self.replace_message("No matches")
        else:
            self.replace_message(f"{self.me_query.count()} people")
            self.btns = []
            if value:
                for acr in self.me_query:
                    self.query_one("#buttons").mount(
                        btn := PersonButton(acr)
                    )
                    self.btns.append(btn)

    def replace_message(self, msg):
        self.query_one("#message").remove()
        self.mount(Center(Label(msg), id="message"))

class PersonButton(Button):

    def __init__(self, person):
        super().__init__(person.name)
        self.person = person

    def on_button_pressed(self):
        app.query_one("#content").remove()
        app.query_one("#body").mount(
            VerticalScroll(id="content")
        )
        self.add_new_row("Key", "Value")
        self.add_new_row("Name", self.person.name)
        for k in self.person._fields_ordered:
            if k not in {'name', 'id'}:
                self.add_new_row(k.capitalize(), getattr(self.person, k))

    def add_new_row(self, key, value, w_type=Static):

        app.query_one("#content").mount(
            Horizontal(
                Vertical(w_type(key), classes="key"),
                Vertical(w_type(str(value)), classes="value"),
                classes="result-row"
            )
        )

app = PeopleApp()
dbcon = mongoengine.connect("acronyms")

def main(args=sys.argv):
    return app.run()

if __name__ == "__main__":
    main()
