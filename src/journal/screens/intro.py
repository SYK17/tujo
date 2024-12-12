from textual.screen import Screen
from textual.widgets import Static
from textual.containers import Center, Middle

from src.journal.screens.home import HomeScreen


class IntroScreen(Screen):
    CSS = """
    Screen {
        background: black;
        align: center middle;
    }
    
    Middle {
        background: black;
        width: 100%;
        align: center middle;
    }
    
    Center {
        background: black;
        width: 100%;
        align: center middle;
    }
    
    #title {
        width: 100%;
        height: auto;
        text-align: center;
        color: white;
        background: black;
    }
    
    #subtitle {
        width: 100%;
        height: auto;
        text-align: center;
        color: #8C8C8C;
        background: black;
        margin-top: 1;
    }
    
    #prompt {
        dock: bottom;
        padding: 1 2;
        background: black;
        color: #8C8C8C;
    }
    """


    #------------
    # main method
    #------------

    def compose(self):
        yield Center(
            Middle(
                Static("Tujo.", id="title"),
                Static("a task journal to organize life simply", id="subtitle")
            )
        )
        yield Static("press any key to continue...", id="prompt")

    async def on_key(self, event):
        await self.app.push_screen(HomeScreen())
