from textual.app import App, ComposeResult

from textutils.lib import SaveCancel

class BaseApp(App):
    """A Textual app in which to drop test functionality."""

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def report(self, arg):
        print(f"ARG: {True}")
        self.panic(self.tree)

app = BaseApp()

if __name__ == "__main__":
    app.run()
