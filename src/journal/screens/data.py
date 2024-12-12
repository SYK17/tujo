import requests

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Center, Vertical
from textual.widgets import Static

from src.journal.screens.base import BaseScreen


class DataScreen(BaseScreen):
    """Data screen that shows task statistics."""

    CSS_PATH = "tcss/main.tcss"


    #------------
    # keybindings
    #------------

    BINDINGS = [
        *BaseScreen.BINDINGS,  # Include base navigation bindings
        Binding("up", "move_up", "Move Up"),
        Binding("down", "move_down", "Move Down"),
        Binding("k", "move_up", "Move Up"),
        Binding("j", "move_down", "Move Down"),
    ]


    #---------------
    # initialization
    #---------------

    def __init__(self):
        super().__init__()  # Inherits from Textual's Screen __init__ in BaseScreen
        self.stats = {"total": 0, "completed": 0, "pending": 0}
        self._fetch_stats()


    #--------------
    # helper method
    #--------------

    def _fetch_stats(self):
        """Fetch statistics from analytics microservice"""
        try:
            response = requests.get("http://localhost:2002/stats")
            if response.status_code == 200:
                self.stats = response.json()
            else:
                self.stats = {"total": '?', "completed": '?', "pending": "Error"}
        except requests.RequestException:
            self.stats = {"total": '?', "completed": '?', "pending": "Service Unavailable"}


    #------------
    # main method
    #------------

    def compose_content(self) -> ComposeResult:
        """Create child widgets for the screen."""
        # Navigation bar
        with Container(id="nav-bar"):
            yield Static(self._format_nav_text("data"), classes="nav-text")

        # Main content area
        with Container(id="main-content", classes="centered-main-content"):
            with Center():
                with Vertical():
                    yield Static("task statistics", classes="section-title")
                    yield Static(f"total tasks created: {self.stats['total']}", classes="stat-item")
                    yield Static(f"tasks completed: {self.stats['completed']}", classes="stat-item")
                    yield Static(f"tasks pending: {self.stats['pending']}", classes="stat-item")
