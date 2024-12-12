from textual.widgets import Input


class TaskInput(Input):
    """A reusable task input widget that handles task creation across all log screens."""
    
    DEFAULT_CSS = """
    TaskInput {
        border: none;
        height: 1;
        margin: 1 0;
        padding: 0 2;
        background: $boost;
    }
    
    TaskInput:focus {
        border: none;
    }
    """
    
    def __init__(self):
        super().__init__(
            placeholder="Enter a task...",
            id="task-input"
        )
    
    def _on_key(self, event) -> None:
        if event.key == "escape":
            self.remove()
        elif event.key == "enter":
            parent_screen = self.screen
            if hasattr(parent_screen, 'handle_new_task'):
                parent_screen.handle_new_task(self.value)
            self.remove()
        else:
            super()._on_key(event)
