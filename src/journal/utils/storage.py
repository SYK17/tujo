import json
from pathlib import Path
from typing import Dict, List


class Storage:
    def __init__(self):
        # Create data directory in same location as file
        self.data_dir = Path(__file__).parent
        self.data_file = self.data_dir / "tasks.json"
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        """Create data directory if it doesn't exist."""
        self.data_dir.mkdir(exist_ok=True)
        if not self.data_file.exists():
            self.save({})

    def load(self) -> Dict[str, List[str]]:
        """Load tasks from storage."""
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def save(self, tasks: Dict[str, List[str]]) -> None:
        """Save tasks to storage."""
        with open(self.data_file, 'w') as f:
            json.dump(tasks, f, indent=2)
