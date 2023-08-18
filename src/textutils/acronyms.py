from textual.app import App, ComposeResult
from textual.validation import Function, Number, ValidationResult, Validator
from textual.widgets import Input, Label, Pretty, Static, Footer, Button
from textual.containers import Container, Horizontal, Vertical, VerticalScroll, Center
import mongoengine
import importlib.resources as ir
import os
import sys

print("INFO: About to import Acronym")
from .models import Acronym
print("INFO: IMPORTED")
print("__NAME__:", __name__)

os.environ["TEXTUAL"] = "debug,devtools"

def load_css(name=__name__):
    module = sys.modules[name]
    m_path = ir.files(module)
    print("MODULE PATH:", m_path)
    with ir.as_file(m_path / f"styles.css") as f_path:
        with open(f_path) as in_file:
            return in_file.read()

class InputApp(App):

    CSS_PATH = "acronyms.css"

    def __init__(self):
        super().__init__()


    def compose(self) -> ComposeResult:
        yield Horizontal(
            Input(
                placeholder="Enter (the beginning of) an acronym...",
                id="in_val,"
                ),
            id="question-box"
        )
        yield Horizontal(
            VerticalScroll(
                id="buttons"
                ),
            VerticalScroll(
                Static(""),
                id="content"
                ),
            id="body"
        )

        yield Center(Label(f"Initial message"), id="message")


    def on_input_changed(self, event: Input.Changed) -> None:
        # Updating the UI to show the reasons why validation failed
        for btn in self.query(Button):
            btn.remove()
        in_string = self.query_one(Input)
        value = in_string.value
        self.me_query = Acronym.objects(acronym__istartswith=value)
        count = self.me_query.count()
        if count == 0:
            self.replace_message("No matches")
        else:
            self.replace_message(f"{self.me_query.count()} acronyms")
            self.btns = []
            if value:
                for acr in self.me_query.order_by("acronym"):
                    self.query_one("#buttons").mount(
                        btn := ExplainButton(acr)
                    )
                    self.btns.append(btn)

    def replace_message(self, msg):
        self.query_one("#message").remove()
        self.mount(Center(Label(msg), id="message"))

class ExplainButton(Button):
    def __init__(self, acronym):
        super().__init__(acronym.acronym)
        self.title = acronym.title
        self.explanation = acronym.explanation
        print("Acronym:", acronym.acronym, self.title, self.explanation)

    def on_button_pressed(self):
        app.query_one("#content").remove()
        app.query_one("#body").mount(
            VerticalScroll(
                Static(f"{self.title}\n\n{self.explanation}"),
                id="content"
            )
        )

app = InputApp()
dbcon = mongoengine.connect("acronyms")

def main(args=sys.argv):
    return app.run()

if __name__ == "__main__":
    main()
