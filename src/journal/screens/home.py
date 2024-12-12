from datetime import datetime, timedelta

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal
from textual.widgets import Static

from src.journal.screens.base import BaseScreen
from src.journal.utils.storage import Storage
from src.journal.components.task_input import TaskInput
from src.journal.components.undo_warning import UndoWarningScreen


class HomeScreen(BaseScreen):
    """Home screen that manages tasks from the past week."""

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
        Binding("enter", "toggle_selection_mode", "Toggle Task Selection"),
        Binding("t", "new_task", "New Task"),
        Binding("x", "toggle_done", "Toggle Done"),
        Binding("u", "undo", "Undo"),
    ]


    #---------------
    # initialization
    #---------------

    def __init__(self):
        super().__init__()
        self.storage = Storage()
        self.selected_index = 0
        self.selected_task_index = -1  # -1 indicates no task is selected
        self.task_selection_mode = False
        self.tasks = self.storage.load()
        self.undo_stack = []
        self.dates = []
        self._generate_dates()


    #---------------
    # helper methods
    #---------------

    def _generate_dates(self) -> None:
        self.dates = []  # clear existing dates
        today = datetime.now()

        for i in range(8):
            date = today - timedelta(days=i)
            formatted_date = date.strftime("%m.%d.%y")
            self.dates.append(formatted_date)

        if not self.tasks:
            self.tasks = {}
            self.tasks[self.dates[0]] = [
                "this is a sample task.",
                "press `t` to add a new task.",
                "press `x` to mark me 'done'.",
                "now press `u` to undo."
            ]
            self.storage.save(self.tasks)

    def _format_task(self, task: str, index: int) -> tuple[str, str]:
        """Format a task and return the text and CSS class."""
        selection_mark = ""
        if self.task_selection_mode and index == self.selected_task_index:
            selection_mark = " <<"

        if task.startswith("x "):
            return (f"{task}{selection_mark}", "task-done")
        elif task.startswith("> "):
            return (f"{task}{selection_mark}", "task-migrated")
        else:
            return (f"• {task}{selection_mark}", "task")

    def _save_state(self) -> None:
        saved_state = {}
        for date in self.tasks:
            saved_state[date] = self.tasks[date].copy()

        self.undo_stack.append(saved_state)
        self.storage.save(self.tasks)

    def refresh_screen(self) -> None:
        """Refresh the screen content."""
        # Get containers
        dates_container = self.query_one("#dates-container")
        content_area = self.query_one("#content-area")
        footer = self.query_one("#footer")

        if not dates_container or not content_area or not footer:
            return  # Guard against containers not being mounted yet

        self.refresh_dates(dates_container)
        self.refresh_content(content_area)
        self.refresh_footer(footer)

    def refresh_dates(self, container: Container) -> None:
        container.remove_children()
        for i, date in enumerate(self.dates):
            if i == self.selected_index:
                container.mount(Static(f">> {date}", classes = "date date-selected"))
            else:
                container.mount(Static(f"   {date}", classes = "date"))

    def refresh_content(self, container: Container) -> None:
        container.remove_children()

        # Add day title
        current_date = self.dates[self.selected_index]
        selected_date = datetime.strptime(current_date, "%m.%d.%y")
        container.mount(Static(selected_date.strftime("%A").lower(), classes="day-title"))

        # Add tasks
        current_tasks = self.tasks.get(current_date, [])
        for i, task in enumerate(current_tasks):
            task_text, task_class = self._format_task(task, i)
            container.mount(Static(task_text, classes=task_class))

    def refresh_footer(self, container: Container) -> None:
        container.remove_children()
        container.mount(Static(
            "[white]t[/] new task    [white]x[/] done    [white]u[/] to undo",
            classes="footer-text",
            markup=True
        ))


    #---------------------------
    # event handlers and actions
    #---------------------------

    def action_move_up(self) -> None:
        if self.task_selection_mode:
            if self.selected_task_index > 0:
                self.selected_task_index -= 1
                self.refresh_screen()
        else:
            if self.selected_index > 0:
                self.selected_index -= 1
                self.refresh_screen()

    def action_move_down(self) -> None:
        current_date = self.dates[self.selected_index]
        tasks = self.tasks.get(current_date, [])

        if self.task_selection_mode:
            if self.selected_task_index < len(tasks) - 1:
                self.selected_task_index += 1
                self.refresh_screen()
        else:
            if self.selected_index < len(self.dates) - 1:
                self.selected_index += 1
                self.refresh_screen()

    async def action_undo(self) -> None:
        if self.undo_stack:
            undo_warning = UndoWarningScreen()
            await self.app.push_screen(undo_warning)

    def _perform_undo(self) -> None:
        if not self.undo_stack:
            return

        previous_state = self.undo_stack.pop()
        self.tasks = {}
        for date in previous_state:
            self.tasks[date] = previous_state[date].copy()

        self.storage.save(self.tasks)
        self.refresh_screen()

    def action_toggle_selection_mode(self) -> None:
        current_date = self.dates[self.selected_index]
        tasks = self.tasks.get(current_date, [])

        if not tasks:
            return

        if self.task_selection_mode:
            self.task_selection_mode = False
            self.selected_task_index = -1
        else:
            self.task_selection_mode = True
            self.selected_task_index = 0

        self.refresh_screen()

    def action_new_task(self) -> None:
        content_area = self.query_one("#content-area")
        if content_area:
            task_input = TaskInput()
            content_area.mount(task_input)
            task_input.focus()

    def handle_new_task(self, task_text: str) -> None:
        task_text = task_text.strip()
        if not task_text:
            return

        self._save_state()

        current_date = self.dates[self.selected_index]
        if current_date not in self.tasks:
            self.tasks[current_date] = []

        self.tasks[current_date].append(task_text)
        self.storage.save(self.tasks)
        self.refresh_screen()

    def action_toggle_done(self) -> None:
        """Toggle the done state of the selected task."""
        if not self.task_selection_mode or self.selected_task_index == -1:
            return

        current_date = self.dates[self.selected_index]
        tasks = self.tasks.get(current_date, [])

        if self.selected_task_index >= len(tasks):
            return

        self._save_state()

        task = tasks[self.selected_task_index]
        tasks[self.selected_task_index] = task[2:] if task.startswith("x ") else f"x {task}"

        self.tasks[current_date] = tasks
        self.storage.save(self.tasks)
        self.refresh_screen()


    #------------
    # main method
    #------------

    def compose_content(self) -> ComposeResult:
        """Create child widgets for the screen."""
        # Navigation bar
        with Container(id="nav-bar"):
            yield Static(self._format_nav_text("home"), classes="nav-text")

        # Main content area
        with Container(id="main-content"):
            with Horizontal():
                # Dates sidebar
                with Container(id="dates-container"):
                    for i, date in enumerate(self.dates):
                        if i == self.selected_index:
                            yield Static(f">> {date}", classes="date date-selected")
                        else:
                            yield Static(f"   {date}", classes="date")

                # Tasks area
                with Container(id="content-area"):
                    # Add day title
                    selected_date = datetime.strptime(self.dates[self.selected_index], "%m.%d.%y")
                    yield Static(selected_date.strftime("%A").lower(), classes="day-title")

                    # Add tasks
                    current_tasks = self.tasks.get(self.dates[self.selected_index], [])
                    for i, task in enumerate(current_tasks):
                        task_text, task_class = self._format_task(task, i)
                        yield Static(task_text, classes=task_class)
        # Footer
        with Container(id="about-footer"):
            yield Static(
                "[white]t[/] new task    [white]x[/] done    [white]u[/] to undo",
                classes="footer-text",
                markup=True
            )

        # Navigation help
        yield Static(
            "[white]↕[/] or [white]jk[/] navigate    [white]enter[/] toggle select    [white]^p[/] toggle palette",
            id="navigation-help",
            markup=True
        )

