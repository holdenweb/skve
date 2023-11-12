from __future__ import annotations

import pytest
from textual.widgets import Static
from textutils import lib

from tests.app_skel import BaseApp


class QuestionText(lib.YesNoText):
    def __init__(self, msg, *args, **kw):
        super().__init__(msg, *args, **kw)
        self.result = None


class LocalApp(BaseApp):

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.result = None
        self.tl_done = lib.YesNoText('Kill: ', 'app.yes', 'app.no')

    def compose(self):
        yield Static(self.tl_done.render(), id='qtxt')
        self.log(self.tree)

    def on_click(self, e):
        self.log(self.tree)

    def action_yes(self):
        self.result = 'YES!'

    def action_no(self):
        self.result = 'NO?'


@pytest.mark.parametrize(
    ('pos', 'expected'),
    [
        ((6, 7, 8), 'YES!'),
        ((10, 11), 'NO?'),
        ((5, 9, 12), None),
    ],
)
async def test_links_work(pos, expected):
    for p in pos:
        app = LocalApp()
        async with app.run_test() as pilot:
            assert app.result is None
            await pilot.click('Static', offset=(p, 0))
            assert app.result == expected

app = LocalApp()


if __name__ == '__main__':
    app.run()
