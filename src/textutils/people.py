from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.validation import Function, Number, ValidationResult, Validator
from textual.widget import Widget
from textual.widgets import Input, Label, Pretty, Static, Footer, Button, DataTable, TextArea
from textual.containers import Container, Horizontal, HorizontalScroll, Vertical, VerticalScroll, Center, Grid
from textual.screen import Screen, ModalScreen
from textual.events import InputEvent
from textual.document import Document

from textutils.key_value_edit import KeyValueEditScreen
import mongoengine

import importlib.resources as ir
import os
import sys
from itertools import cycle

from .models import Person

os.environ["TEXTUAL"] = "debug,devtools"
EMPTY_DOC = Document("")

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
        for btn in self.query(".person-button"):
            btn.remove()
        in_string = self.query_one(Input)
        value = in_string.value
        self.me_query = Person.objects(name__icontains=value)
        count = self.me_query.count()
        if count == 0:
            self.replace_message("No matches")
        else:
            app.bg_class = cycle(("bg-one", "bg-two"))
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

class InputStripe(Horizontal):
    def compose(self):
        yield Label("Search: ")
        yield Input(
                placeholder="Enter (part of) a person's name...",
                id="in-val",
        )
        yield Button(label="+", variant="primary", id="add-person")

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

    def __init__(self, key, value):
        super().__init__()
        self.key = key
        self.value = value
        self.bg_class = next(app.bg_class)
        self.classes = f"result-row {self.bg_class}"

    def compose(self):
        yield Vertical(Static(self.key), classes=f"key {self.bg_class}")
        yield Vertical(Static(str(self.value)), classes=f"value {self.bg_class}")
        yield Vertical(Button(label="#", classes="edit-button"), classes="edit-button-col")

    def on_button_pressed(self):
        app.push_screen(KeyValueEditScreen(self.key, self.value), self.stash_result)
        print("RESULTROW TREE:")
        self.log(self.tree)

    def stash_result(self, return_value):
        if return_value is not None:
            self.key, self.value = return_value
            key_f, value_f, button = self.query(Static)
            key_f.update(self.key)
            value_f.update(self.value)

app = PeopleApp()
dbcon = mongoengine.connect("acronyms")