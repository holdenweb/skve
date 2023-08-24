from textual.app import App, ComposeResult
from textual.validation import Function, Number, ValidationResult, Validator
from textual.widgets import Input, Label, Pretty, Static, Footer, Button, DataTable, TextArea
from textual.containers import Container, Horizontal, HorizontalScroll, Vertical, VerticalScroll, Center, Grid
from textual.screen import Screen, ModalScreen
from textual.events import InputEvent
from textual.document import Document

import mongoengine

import importlib.resources as ir
import os
import sys
from itertools import cycle

from .models import Person

os.environ["TEXTUAL"] = "debug,devtools"
EMPTY_DOC = Document("")

class NewRecordScreen(ModalScreen):
    def compose(self) -> ComposeResult:
        yield Vertical(
            Horizontal(
                Input(id="input-key"),
                TextArea(document=EMPTY_DOC, id="input-value"),
                id="input-row"
            ),
            Center(
                Label("Are you sure you want to quit?", id="question"),
                Horizontal(
                    Button("Save", variant="error", id="save"),
                    Button("Cancel", variant="primary", id="cancel")
                ),
                id="label-and-buttons"
            ),
            id="dialog",
        )

    def on_button_pressed(self: Screen, event: Button.Pressed) -> None:
        for node in self.walk_children():
            print(node, node.id)
        id = event.button.id
        if id == "save":
            retval = (self.query_one("#input-key").value,
                      self.query_one("#input-value").text)
            self.dismiss(result=retval)
        elif id == "cancel":
            retval = None
            self.dismiss()
        else:
            raise ValueError("Press of unknown button {id!r}")

class InputStripe(Horizontal):
    def compose(self):
        yield Label("Search: ")
        yield Input(
                placeholder="Enter (part of) a person's name...",
                id="in-val",
        )
        yield Button(label="+", variant="primary", id="add-person")

    def on_button_pressed(self):
        app.push_screen(NewRecordScreen(), self.stash_result)

    def stash_result(self, return_value):
        print("DIALOG RETURNED", return_value)

class PeopleApp(App):

    CSS_PATH = "people.css"

    def on_mount(self):
        self.push_screen(MainScreen())
        self.screen.styles.background = "blue"

class MainScreen(Screen):

    def compose(self) -> ComposeResult:
        yield InputStripe(id="question-box")
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
        print("BOO", event)
        for btn in self.query(".person-button"):
            btn.remove()
        in_string = self.query_one(Input)
        value = in_string.value
        self.me_query = Person.objects(name__icontains=value)
        count = self.me_query.count()
        if count == 0:
            self.replace_message("No matches")
        else:
            app.bg_class = cycle(("bg-yellow", "bg-red"))
            self.replace_message(f"{self.me_query.count()} people")
            self.btns = []
            if value:
                for acr in self.me_query:
                    self.query_one("#buttons").mount(
                        btn := PersonButton(acr, classes="person-button")
                    )
                    self.btns.append(btn)

    def replace_message(self, msg):
        self.query_one("#message").remove()
        self.mount(Center(Label(msg, id="message")))

class PersonButton(Button):

    def __init__(self, person, **kw):
        super().__init__(person.name, **kw)
        self.person = person

    def on_button_pressed(self):
        app.query_one("#content").remove()
        app.query_one("#body").mount(
            VerticalScroll(id="content")
        )
        self.add_new_row("Key", "Value", clickable=False)
        self.add_new_row("Name", self.person.name, clickable=False)
        for k in self.person._fields_ordered:
            if k not in {'name', 'id'}:
                self.add_new_row(k.capitalize(), getattr(self.person, k))

    def add_new_row(self, key, value, w_type=Static, clickable=True):
        app.query_one("#content").mount(
            ResultRow(key, str(value))
        )

class ResultRow(Horizontal):

    def __init__(self, key, value, clickable=True):
        super().__init__()
        self.key = key
        self.value = value
        self.clickable = clickable
        self.bg_class = next(app.bg_class)
        self.classes = f"result-row {self.bg_class}"

    def compose(self):
        yield Vertical(Static(self.key), classes=f"key {self.bg_class}")
        yield Vertical(Static(str(self.value)), classes=f"value {self.bg_class}")

app = PeopleApp()
dbcon = mongoengine.connect("acronyms")