from __future__ import annotations

from textual.app import App
from textual.app import ComposeResult
from textual.containers import Center
from textual.containers import Horizontal
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Button
from textual.widgets import Input


class KeyValueEditScreen(ModalScreen):

    DEFAULT_CSS = """\
KeyValueEditScreen {
    border: $boost 100%;
}

#input-row {
    height: 1fr;
}

#input-value {
    width: 7fr;
    height: auto;
    min-height: 5;
    border: red 100%;
}

#input-key {
    width: 2fr;
    border: red 100%;
}

#label-and-buttons {
    width: 100%;
    align-horizontal: center;
    height: auto;
    border: black 100%;
    background: green 100%;
}
"""

    def __init__(self, key, value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key = key
        self.value = value
        self.key_field = Input(id='input-key')
        self.value_field = Input(id='input-value')

    def compose(self) -> ComposeResult:
        with Vertical(id='dialog'):
            yield Horizontal(
                self.key_field,
                self.value_field,
                id='input-row',
            )
            yield Center(
                Horizontal(
                    Button('Save', variant='primary', id='save'),
                    Button('Cancel', variant='error', id='cancel'),
                    id='label-and-buttons',
                ),
            )

    def on_mount(self):
        self.key_field.value = self.key
        self.value_field.value = self.value
        self.refresh()
        print('NEWRECORDSCREEN TREE')
        self.log(self.css_tree)

    def on_button_pressed(self: ModalScreen, event: Button.Pressed) -> None:
        id = event.button.id
        if id == 'save':
            retval = (
                self.query_one('#input-key').value,
                self.query_one('#input-value').value,
            )
        elif id == 'cancel':
            retval = None
        else:
            raise ValueError('Press of unknown button {id!r}')
        self.dismiss(result=retval)
        self.log(self.css_tree)


class TestApp(App):

    def on_mount(self):
        self.push_screen(
            KeyValueEditScreen('KEY', 'Value Value Value'),
            self.done,
        )
        self.screen.styles.background = 'blue'

    def done(self, result):
        self.exit(message=f'Done!\nresult: {result}')


app = TestApp()

if __name__ == '__main__':
    app.run()
