from __future__ import annotations

from textual.app import App
from textual.app import ComposeResult
from textutils.key_value_edit import KeyValueEditScreen


class TestApp(App):

    def on_mount(self):
        self.push_screen(
            KeyValueEditScreen('KEY', 'Value Value Value'),
            self.done,
        )
        self.screen.styles.background = 'blue'

    def done(self, result):
        self.exit(message=f'Done!\nresult: {result}')

    # def compose(self) -> ComposeResult:
        # yield Static("Yield components in compose() method")


app = TestApp()

if __name__ == '__main__':
    app.run()
