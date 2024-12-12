import requests

from textual.app import ComposeResult
from textual.screen import Screen
from textual.binding import Binding
from textual.containers import Container, Center, Vertical
from textual.widgets import Static, Header, Footer


class BaseScreen(Screen):
    """Base screen with common components."""

    CSS_PATH = "tcss/main.tcss"

    TITLE = "Tujo"

    # Class variables
    _stored_weather = None
    _stored_quote = None


    #------------
    # Keybindings
    #------------

    BINDINGS = [
        Binding('d', "show_data", "data"),
        Binding('p', "show_pomodoro", "pomodoro"),
        Binding('h', "show_home", "home"),
        Binding('a', "show_about", "about"),
    ]


    #---------------
    # helper methods
    #---------------

    def _format_nav_text(self, current_screen: str) -> str:
        """Handles color formatting logic"""

        nav_items = [
            ('h', "home", current_screen == "home"),
            ('p', "pomodoro", current_screen == "pomodoro"),
            ('d', "data", current_screen == "data"),
            ('a', "about", current_screen == "about")
        ]

        formatted_items = []
        for key, word, is_active in nav_items:
            if is_active:
                formatted_items.append(f"[white]{key} {word}[/]")
            else:
                formatted_items.append(f"[white]{key}[/] [#8C8C8C]{word}[/]")

        return "  ".join(formatted_items)

    def _get_weather(self) -> dict:
        """Calls microservice to get weather info."""
        if BaseScreen._stored_weather is None:
            try:
                response = requests.post(
                    "http://localhost:3724/weatherMicro",
                    json={
                        "zip": "94104",
                        "operation": "current",
                        "addInfo": "0"
                    }
                )
                BaseScreen._stored_weather = response.json()
            except Exception:
                BaseScreen._stored_weather = {"temp": "?", "cond": "unavailable", "icon": ""}

        return BaseScreen._stored_weather

    def _get_lotr_quote(self):
        """Calls microservice to get random lotr quote."""
        if BaseScreen._stored_quote is None:
            try:
                response = requests.get("http://localhost:2001/lotrQuote")
                if response.status_code == 200:
                    BaseScreen._stored_quote = response.json()
                else: 
                    raise Exception(f"Http {response.status_code}")
            except Exception:
                BaseScreen._stored_quote = {
                    # Fallback quote
                    "quote": "There's some good in this world, Mr. Frodo, and it's worth fighting for.",
                    "character": "Samwise Gamgee"
                }
        return BaseScreen._stored_quote


    #---------------------------
    # event handlers and actions
    #---------------------------

    def compose_content(self) -> ComposeResult:
        """Will be overwritten in child classes for specific content."""
        yield Container()

    async def action_show_home(self) -> None:
        """Switch to the home screen."""
        from src.journal.screens.home import HomeScreen
        await self.app.switch_screen(HomeScreen())

    async def action_show_about(self) -> None:
        """Switch to the about screen."""
        from src.journal.screens.about import AboutScreen
        await self.app.switch_screen(AboutScreen())

    async def action_show_pomodoro(self) -> None:
        """Switch to the pomodoro screen."""
        from src.journal.screens.pomodoro import PomodoroScreen
        await self.app.switch_screen(PomodoroScreen())

    async def action_show_data(self) -> None:
        """Switch to the data screen."""
        from src.journal.screens.data import DataScreen
        await self.app.switch_screen(DataScreen())

    #------------
    # main method
    #------------

    def compose(self) -> ComposeResult:
        """Create child widgets for the screen."""
        yield Header()
        with Center():
            with Vertical():

                # weather at top of screen.
                weather_data = self._get_weather()
                with Container(id="weather-container"):
                    yield Static(
                        f"{weather_data['cond'].lower()}, {weather_data['temp']}°f",
                        classes="weather-text")

                # main page container wraps all content.
                with Container(id="page-container"):
                    yield from self.compose_content()

                # quote at bottom of screen.
                quote_data = self._get_lotr_quote()
                with Container(id="quote-container"):
                    yield Static(
                        f'"{quote_data["quote"]}" - {quote_data["character"]}',
                        classes="quote-text")
