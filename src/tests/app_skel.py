from textual.app import App, ComposeResult

from lib import SaveCancel

class SkelApp(App):
    """A Textual app in which to drop test functionality."""

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield SaveCancel(self.report)

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def report(self, arg):
        print(f"ARG: {True}")
        self.panic(self.tree)

app = SkelApp()

if __name__ == "__main__":
    app.run()
