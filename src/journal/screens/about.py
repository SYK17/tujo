from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal
from textual.widgets import Static

from .base import BaseScreen


class AboutScreen(BaseScreen):
    """About screen that shows information about the app."""
    
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
        super().__init__()
        self.selected_index = 0
        self.categories = ["welcome", "keys", "tips"]
        self.content = {
            "welcome": [
                "tujo is a simple journal designed to help you",
                "track your daily tasks and thoughts.",
                "tujo aims to keep things simple and focused.",
                "\n",
                "terminal + journal = tujo",
            ],
            "keys": [
                "h.......home",
                "a.......about",
                "d.......data",
                "c.......calendar",
                "↑/k.....move Up",
                "↓/j.....move Down",
                "⏎.......toggle Task Selection",
                "t.......create a new task",
                "x.......complete a task",
                "u.......undo last action",
                "^c......quit Application",
                "^p......open Command Palette",
            ],
            "tips": [
                "1. keep tasks atomic and actionable",
                "2. review your tasks daily",
                "3. there is beauty in brevity"
            ]
        }


    #--------------
    # helper method
    #--------------

    def refresh_screen(self) -> None:
        """Refresh the screen content."""
        # Get containers
        categories_container = self.query_one("#dates-container")
        content_area = self.query_one("#content-area")
        
        if not categories_container or not content_area:
            return
            
        # Refresh categories
        categories_container.remove_children()
        for i, category in enumerate(self.categories):
            if i == self.selected_index:
                categories_container.mount(Static(f">> {category}", classes="date date-selected"))
            else:
                categories_container.mount(Static(f"   {category}", classes="date"))

        # Refresh content area
        content_area.remove_children()

        # Add section title
        content_area.mount(Static("about tujo", classes="day-title"))

        # Add content
        current_content = self.content[self.categories[self.selected_index]]
        for line in current_content:
            content_area.mount(Static(line, classes="task"))


    #---------------------------
    # event handlers and actions
    #---------------------------

    def action_move_up(self) -> None:
        if self.selected_index > 0:
            self.selected_index -= 1
            self.refresh_screen()

    def action_move_down(self) -> None:
        if self.selected_index < len(self.categories) - 1:
            self.selected_index += 1
            self.refresh_screen()


    #------------
    # main method
    #------------

    def compose_content(self) -> ComposeResult:
        """Create child widgets for the screen."""
        # Navigation bar
        with Container(id="nav-bar"):
            yield Static(self._format_nav_text("about"), classes="nav-text")

        # Main content area
        with Container(id="main-content"):
            with Horizontal():
                # Categories sidebar
                with Container(id="dates-container"):
                    for i, category in enumerate(self.categories):
                        if i == self.selected_index:
                            yield Static(f">> {category}", classes="date date-selected")
                        else:
                            yield Static(f"   {category}", classes="date")

                # Content area
                with Container(id="content-area"):
                    # Add section title
                    yield Static("about tujo", classes="day-title")
                    
                    # Add content
                    current_content = self.content[self.categories[self.selected_index]]
                    for line in current_content:
                        yield Static(line, classes="task")

        # Footer
        yield Container(id="about-footer")
        yield Static(
            "version 0.1.0",
            classes="version-text",
            markup=True
        )

        # Navigation help
        yield Static(
            "[white]↕[/] or [white]jk[/] navigate",
            id="navigation-help",
            markup=True
        )

