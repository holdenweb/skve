from __future__ import annotations

import os
from dataclasses import dataclass
from itertools import cycle

from rich.text import Text
from textual.app import App
from textual.app import ComposeResult
from textual.containers import Center
from textual.containers import Horizontal
from textual.containers import Vertical
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.validation import Validator
from textual.widget import Widget
from textual.widgets import Button
from textual.widgets import Input
from textual.widgets import Label
from textual.widgets import Static
from textual.widgets import TextArea

from textutils.demo_store import people_matching
from textutils.demo_store import update_person
from textutils.key_value_edit import KeyValueEditScreen
from textutils.lib import SaveCancel
from textutils.validators import HasOneSpace

os.environ['TEXTUAL'] = 'debug,devtools'


class RegularisedTextArea(TextArea):
    def __init__(self, text='', validators: list[Validator] = [], *args, **kw):
        super().__init__(*args, **kw)
        self.validators = validators  # Use when returning?

    @property
    def value(self):
        return self.text

    @value.setter
    def value(self, new_value):
        return self.load_text(new_value)


@dataclass
class Field:
    primary_key: bool = False
    data_type: type = str
    widget_type: Widget = Input
    validators: list[Validator] | None = None


fields = {
    'name': Field(primary_key=True),
    'phone': Field(),
    'email': Field(validators=[]),
    'country': Field(),
    'currency': Field(),
    'company': Field(),
    'date': Field(),
    'time': Field(),
    'colour': Field(),
    'text': Field(widget_type=RegularisedTextArea),
}


class PeopleApp(App):
    CSS_PATH = 'people.css'

    def on_mount(self):
        self.main_screen = MainScreen()
        self.push_screen(self.main_screen)

    def action_yes(self):
        self.main_screen.replace_message('Yes, thanks!?')

    def action_no(self):
        self.main_screen.replace_message('OK then, not today!')

    def on_click(self, e):
        self.log(self.tree)


class ContentPane(VerticalScroll):
    def add_result_row(self, key, value, widget_type=Static, clickable=True):
        self.mount(
            ResultRow(
                key,
                str(value),
                validators=[HasOneSpace()],
                widget_type=widget_type,
                clickable=clickable,
            ),
        )()


class MainScreen(Screen):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.content_pane = ContentPane(
            Static(
                'Click on a name in the left-hand'
                ' panel to see details here',
            ),
            id='content',
        )

    def compose(self) -> ComposeResult:
        yield InputStripe(id='question-box')
        yield Horizontal(
            VerticalScroll(id='buttons'),
            self.content_pane, id='body',
        )
        msg = Text.from_markup(
            'Test Yes/No message: [@click=app.yes]yes[/] [@click=app.no]no[/]',
        )
        yield Center(Label(msg, id='message'))

    def on_input_changed(self, event: Input.Changed) -> None:
        self.query_one('#buttons').remove_children()
        self.log(self.tree)
        in_string = self.query_one('#in-val')
        value = in_string.value
        self.me_query = people_matching(value)
        count = self.current_count = len(self.me_query)
        if count == 0:
            self.replace_message('No matches')
        else:
            self.replace_message(f'{count} people')
            self.btns = []
            if value:
                for person in self.me_query:
                    self.query_one('#buttons').mount(
                        btn := PersonButton(
                            person,
                            content_pane=self.content_pane,
                            classes='person-button',
                        ),
                    )
                    self.btns.append(btn)

    def on_input_submitted(self, event):
        in_string = self.query_one(Input)
        value = in_string.value
        if self.current_count:
            self.replace_message(f'{self.current_count=} CONFLICTS')
        else:
            self.replace_message(f'Creating new person {value!r}')
            # Or something. Soon. I promise ...

    def replace_message(self, msg):
        self.query_one('#message').update(msg)


class InputStripe(Widget):
    def compose(self):
        with Horizontal():
            yield Label('Search: ')
            yield Input(
                placeholder="Enter (part of) a person's name...",
                id='in-val',
            )
            yield Button(label='+', variant='primary', id='add-person')


class PersonButton(Button):
    def __init__(self, person: dict, content_pane: ContentPane, **kw):
        super().__init__(person['name'], **kw)
        self.person = person
        self.content_pane = content_pane

    def on_button_pressed(self):
        app.bg_class = cycle(('bg-one', 'bg-two'))
        self.content_pane.remove_children()
        self.content_pane.add_result_row('Key', 'Value', clickable=False)
        self.content_pane.add_result_row(
            'name',
            self.person['name'],
            clickable=True,
        )
        for k in self.person.keys():
            if k not in {'name', 'id'}:
                self.content_pane.add_result_row(
                    k,
                    self.person[k],
                    widget_type=fields[k].widget_type,
                )
        app.query_one('#content').mount(SaveCancel(self.save_back))

    def save_back(self, save_flag):
        if save_flag:
            key_vals = {
                row.key: row.value
                for row in self.app.query('.result-row')
                if row.clickable
            }
            # Might get ugly with complex field types?
            update_person(self.person, key_vals)
        self.app.query_one('#content').remove_children()


class ResultRow(Widget):
    def __init__(
        self,
        key,
        value,
        clickable=True,
        validators=[],
        widget_type: Widget = Static,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.key = key
        self.value = value
        self.clickable = clickable
        self.validators = validators
        self.bg_class = next(app.bg_class)
        self.widget_type = widget_type
        self.classes = f'result-row {self.bg_class}'
        self.key_field = Static(classes=f'key {self.bg_class}')
        self.value_field = Static(classes=f'value {self.bg_class}')

    def on_click(self, e):
        if self.clickable:
            app.push_screen(
                KeyValueEditScreen(
                    self.key,
                    self.value,
                    validators=self.validators,
                    widget_type=self.widget_type,
                ),
                self.stash_result,
            )

    def compose(self):
        with Horizontal():
            yield Vertical(self.key_field, classes='key-col')
            yield Vertical(self.value_field, classes='value-col')

    def on_mount(self):
        self.update()

    def stash_result(self, return_value):
        if return_value is not None:
            # Some redundant code
            self.key, self.value = return_value
            self.key = self.key.lower()
            self.update()

    def update(self):
        self.key_field.update(
            Text(text=self.key.capitalize(), style='bold white'),
        )
        self.value_field.update(Text(text=self.value))


app = PeopleApp()


if __name__ == '__main__':
    app.run()
