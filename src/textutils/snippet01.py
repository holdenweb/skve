from textual.app import App, ComposeResult
from textual.widgets import Input
from textual.suggester import SuggestFromList

countries = ["England", "Scotland", "Portugal", "Spain", "France"]

class MyApp(App[None]):
    def compose(self) -> ComposeResult:
        yield Input(suggester=SuggestFromList(countries, case_sensitive=False))

MyApp().run()
