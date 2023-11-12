from __future__ import annotations

from textual.app import App
from textual.app import ComposeResult
from textual.suggester import SuggestFromList
from textual.widgets import Input

countries = ['England', 'Scotland', 'Portugal', 'Spain', 'France']


class MyApp(App[None]):
    def compose(self) -> ComposeResult:
        yield Input(suggester=SuggestFromList(countries, case_sensitive=False))


MyApp().run()
