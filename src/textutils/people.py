from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.widgets import Input, Label, Static, Button
from textual.containers import Horizontal, Vertical, VerticalScroll, Center
from textual.screen import Screen
from textual.validation import Validator

from rich.text import Text

from textutils.key_value_edit import KeyValueEditScreen
from textutils.lib import SaveCancel
from textutils.demo_store import people_matching, update_person
from textual.validation import ValidationResult

import os
from itertools import cycle

os.environ["TEXTUAL"] = "debug,devtools"

class HasOneSpace(Validator):
    def validate(self, value: str) -> ValidationResult:
        print(self, value)
        return self.success() if (c := value.count(" ")) == 1 else self.failure("Too many spaces" if c else "No spaces")

class PeopleApp(App):

    CSS_PATH = "people.css"

    def on_mount(self):
        self.main_screen = MainScreen()
        self.push_screen(self.main_screen)

    def action_yes(self):
        self.main_screen.replace_message("Yes, thanks!?")

    def action_no(self):
        self.main_screen.replace_message("OK then, not today!")


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
        msg = Text.from_markup("Test Yes/No message: [@click=app.yes]yes[/] [@click=app.no]no[/]")
        yield Center(Label(msg, id="message"))

    def on_input_changed(self, event: Input.Changed) -> None:
        self.query_one("#buttons").remove_children()
        in_string = self.query_one(Input)
        value = in_string.value
        self.me_query = people_matching(value)
        count = self.current_count = len(self.me_query)
        if count == 0:
            self.replace_message("No matches")
        else:
            self.replace_message(f"{count} people")
            self.btns = []
            if value:
                for person in self.me_query:
                    self.query_one("#buttons").mount(
                        btn := PersonButton(person, classes="person-button")
                    )
                    self.btns.append(btn)

    def on_input_submitted(self, event):
        in_string = self.query_one(Input)
        value = in_string.value
        if self.current_count:
            self.replace_message(f"{self.current_count=} CONFLICTS")
        else:
            self.replace_message(f"Creating new person {value!r}")
            # Or something. Soon. I promise ...

    def replace_message(self, msg):
        self.query_one("#message").update(msg)

class InputStripe(Widget):
    def compose(self):
        with Horizontal():
            yield Label("Search: ")
            yield Input(
                    placeholder="Enter (part of) a person's name...",
                    id="in-val",
            )
            yield Button(label="+", variant="primary", id="add-person")

class PersonButton(Button):

    def __init__(self, person, **kw):
        super().__init__(person['name'], **kw)
        self.person = person

    def on_button_pressed(self):
        app.bg_class = cycle(("bg-one", "bg-two"))
        app.query_one("#content").remove_children()
        self.add_new_row("Key", "Value", clickable=False)
        self.add_new_row("name", self.person['name'], clickable=True)
        for k in self.person.keys():
            if k not in {'name', 'id'}:
                self.add_new_row(k,self.person[k])
        app.query_one("#content").mount(SaveCancel(self.save_back))

    def add_new_row(self, key, value, w_type=Static, clickable=True):
        app.query_one("#content").mount(
            ResultRow(key, str(value), validators=[HasOneSpace()], clickable=clickable)
        )()

    def save_back(self, save_flag):
        if save_flag:
            key_vals = dict((row.key, row.value) for row in self.app.query(".result-row") if row.clickable)
            # Might get ugly with complex field types?
            update_person(self.person, key_vals)
        self.app.query_one("#content").remove_children()

class ResultRow(Widget):

    def __init__(self, key, value, clickable, validators=[], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key = key
        self.value = value
        self.clickable = clickable
        self.validators = validators
        self.bg_class = next(app.bg_class)
        self.classes = f"result-row {self.bg_class}"
        self.key_field = Static(classes=f"key {self.bg_class}")
        self.value_field = Static(classes=f"value {self.bg_class}")

    def on_click(self, e):
        if self.clickable:
            app.push_screen(KeyValueEditScreen(self.key, self.value, validators=self.validators), self.stash_result)

    def compose(self):
        with Horizontal():
            yield Vertical(self.key_field, classes="key-col")
            yield Vertical(self.value_field, classes="value-col")

    def on_mount(self):
        self.update()

    def stash_result(self, return_value):
        if return_value is not None:
            # Some redundant code
            self.key, self.value = return_value
            self.key = self.key.lower()
            self.update()

    def update(self):
        self.key_field.update(Text(text=self.key.capitalize(), style="bold white"))
        self.value_field.update(Text(text=self.value))

app = PeopleApp()


if __name__ == '__main__':
    app.run()
