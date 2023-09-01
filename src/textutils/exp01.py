from textual.app import App, ComposeResult
from textutils.key_value_edit import KeyValueEditScreen


class TestApp(App):

    def on_mount(self):
        self.push_screen(KeyValueEditScreen("KEY", "Value Value Value"),
                         self.done)
        self.screen.styles.background = "blue"

    def done(self, result):
        self.exit(message=f"Done!\nresult: {result}")

app = TestApp()

if __name__ == '__main___':
    app.run()