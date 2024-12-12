from textual.app import App
from .screens.intro import IntroScreen

class JournalApp(App):
    def on_mount(self) -> None:
        self.push_screen(IntroScreen())
