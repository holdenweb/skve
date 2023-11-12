from __future__ import annotations

import itertools
import os
from itertools import cycle

from rich.text import Text
from textual.app import App
from textual.app import ComposeResult
from textual.containers import Center
from textual.containers import Horizontal
from textual.containers import Vertical
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.validation import ValidationResult
from textual.validation import Validator
from textual.widget import Widget
from textual.widgets import Button
from textual.widgets import Input
from textual.widgets import Label
from textual.widgets import Placeholder
from textual.widgets import Static
from textutils.demo_store import people_matching
from textutils.demo_store import update_person
from textutils.key_value_edit import KeyValueEditScreen
from textutils.lib import DeleteMe
from textutils.lib import SaveCancel

os.environ['TEXTUAL'] = 'debug,devtools'


class NoteApp(App):
    """
    Capture a list of people, plus meeting notes in Markdown.
    """
    CSS_PATH = 'note.css'

    def on_mount(self):
        self.push_screen(MainScreen())


class MainScreen(Screen):

    def compose(self) -> ComposeResult:
        with Horizontal(id='list-container'):
            yield LabelList(id='list-of-people')
        with Horizontal(id='caption'):
            yield Static('People')
            yield Horizontal(
                Vertical(
                    Static('This will be the results'),
                    id='content',
                ),
                id='body',
            )
        yield Horizontal(Label(f'Initial message', id='message'))

    def replace_message(self, msg):
        self.query_one('#message').update(msg)


class ListStatic(Static):

    fmt = 'Subclass with own fmt required: {name} {j}'

    def __init__(self, click_function, *args, **kw):
        super().__init__(*args, **kw)
        self.click_function = click_function

    def action_click(self, i):
        self.click_function(i)


class SelectedStatic(ListStatic):

    fmt = "\\[{person_name} [black on white bold][@click='({j})']x[/][/black on white bold]]"

    def __init__(self, *arg, **kw):
        super().__init__


class UnselectedStatic(ListStatic):

    fmt = "\\[[@click='add_to_list(i)]{person_name}[/]"

    def action_click(self, i):
        'Move indicated item from unselected to selected.'
        return self.del_function()


class LabelList(Widget):

    DEFAULT_CSS = """
    Horizontal {min-height: 1;}
    #buttons {background: red 100%}
    """

    def __init__(self, labels: dict[int, str] | None = None, *args, **kw):
        super().__init__(*args, **kw)
        self.item_no = itertools.count()
        self.labels = {} if labels is None else labels

    def compose(self):
        with Horizontal(id='search-bar'):
            yield Label('Search:')
            yield Input(placeholder='Name ...')
            yield Static(Text.from_markup("[black on white bold][@click='clear_input()'] x[/][/black on white bold]"))
        with Horizontal(id='ll-selected'):
            yield self.lozenge_static(self.labels)
        with Horizontal(id='ll-available'):
            everyone = {
                next(self.item_no): item['name']
                for item in people_matching('')
            }
            yield self.lozenge_static(everyone)

    def remove_item(self, i):
        del self.labels[i]
        button_box = self.query_one('#buttons')
        button_box.remove_children()
        button_box.mount(self.lozenge_static())
        query_one('#name-input').refocus()

    def refocus(self):
        name_input = self.query_one('#name-input')
        name_input.focus()

    def on_input_submitted(self, event: Input.Changed) -> None:
        value = self.query_one(Input).value
        self.labels[next(self.item_no)] = value
        button_box = self.query_one('#buttons')
        button_box.remove_children()
        button_box.mount(self.lozenge_static())
        self.refocus()


app = NoteApp()
