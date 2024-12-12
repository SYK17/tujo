import requests
from datetime import datetime

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Center, Vertical
from textual.widgets import Static

from src.journal.screens.base import BaseScreen


class PomodoroScreen(BaseScreen):
    """Pomodoro timer screen."""

    CSS_PATH = "tcss/main.tcss"


    #------------
    # keybindings
    #------------

    BINDINGS = [
        *BaseScreen.BINDINGS,  # Include base navigation bindings
        Binding("space", "toggle_timer", "Start/Stop"),
    ]


    #---------------
    # initialization
    #---------------

    def __init__(self):
        super().__init__()  # Inherits from Textual's Screen __init__ in BaseScreen
        self.timer_running = False


    #---------------
    # helper methods
    #---------------

    def _update_display(self, minutes: int, seconds: int):
        """Update the timer display."""
        timer_display = self.query_one("#timer-display")
        if timer_display:
            timer_display.update(f"{minutes:02d}:{seconds:02d}")

    def _update_status(self, status: str):
        """Update the timer status text."""
        timer_status = self.query_one("#timer-status")
        if timer_status:
            if status == "running":
                timer_status.update("press space to stop")
            else:
                timer_status.update("press space to start")

    def _check_timer(self) -> None:
        """Check timer status and update display."""
        if self.timer_running:
            response = requests.get('http://localhost:2003/time')
            data = response.json()
            self._update_display(data["minutes"], data["seconds"])
            
            # Auto-stop at 0
            if data["minutes"] == 0 and data["seconds"] == 0:
                self.timer_running = False
                self._update_status("stopped")


    #---------------------------
    # event handlers and actions
    #---------------------------

    def action_toggle_timer(self) -> None:
        """Toggle timer between running and stopped states."""
        try:
            if not self.timer_running:
                # Start timer
                response = requests.post('http://localhost:2003/start')
                self.timer_running = True
                self._update_status("running")
            else:
                # Stop timer
                response = requests.post('http://localhost:2003/stop')
                self.timer_running = False
                self._update_status("stopped")

            data = response.json()
            self._update_display(data["minutes"], data["seconds"])
            
        except requests.RequestException:
            # Handle connection error
            self.notify("Could not connect to timer service", severity="error")

    def on_mount(self) -> None:
        """Set up periodic timer updates when the screen is mounted."""
        self.set_interval(1, self._check_timer)  # Will auto-stop when leaving screen


    #------------
    # main method
    #------------

    def compose_content(self) -> ComposeResult:
        """Create child widgets for the screen."""
        # Navigation bar
        with Container(id="nav-bar"):
            yield Static(self._format_nav_text("pomodoro"), classes="nav-text")

        # Main content area
        with Container(id="main-content", classes="centered-main-content"):
            with Center():
                with Vertical():
                    yield Static("30:00", id="timer-display")
                    yield Static("press space to start", id="timer-status")

