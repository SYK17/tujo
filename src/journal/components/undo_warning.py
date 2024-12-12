from textual.screen import Screen
from textual.widgets import Static
from textual.containers import Vertical, Center


class UndoWarningScreen(Screen):
    """Warning screen shown before undoing actions."""

    def compose(self):
        with Center():
            with Vertical():
                yield Static(
                    "warning: this task will be permanently undone and cannot be recovered.",
                    classes="warning-title"
                )
                yield Static(
                    "\ncontinue?\n",
                    classes="warning-prompt"
                )
                yield Static(
                    "y yes  n no", classes="warning-options"
                )

    def on_key(self, event):
        if event.key.lower() in ["y", "n"]:
            should_undo = event.key.lower() == "y"
            self.app.pop_screen()
            if should_undo:
                if hasattr(self.app.screen, '_perform_undo'):
                    self.app.screen._perform_undo()
