"""Command-line interface for the todo application.

Spec Reference: FR-008 (menu interface), FR-009 (validation), FR-010 (exit), US6
Plan Reference: cli/menu.py, CLI Menu Design, DD-005
"""

from ..exceptions import TaskNotFoundError, ValidationError
from ..services import TaskService


class TodoMenu:
    """Command-line interface for the todo application.

    This class provides a menu-driven interface for managing tasks.
    It handles user input, displays output, and routes operations
    to the TaskService.

    Attributes:
        _service: The TaskService instance for task operations
        _running: Flag to control the main application loop
    """

    MENU_OPTIONS = """
====================================
       TODO LIST APPLICATION
====================================

1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete
6. Mark Task Incomplete
7. Exit

Enter your choice (1-7): """

    def __init__(self) -> None:
        """Initialize the menu with a new TaskService."""
        self._service = TaskService()
        self._running = False

    def display_menu(self) -> None:
        """Display the main menu."""
        print(self.MENU_OPTIONS, end="")

    def get_choice(self) -> str:
        """Get the user's menu choice.

        Returns:
            The user's input as a string
        """
        return input().strip()

    def _get_task_id(self, prompt: str = "Enter task ID: ") -> int | None:
        """Get a task ID from the user.

        Args:
            prompt: The prompt to display

        Returns:
            The task ID as an integer, or None if invalid

        Spec Reference: US3-AC4 (invalid ID error)
        """
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Invalid ID. Please enter a number.")
            return None

    def handle_add(self) -> None:
        """Handle the Add Task menu option.

        Spec Reference: US1-AC1, US1-AC2, US1-AC3
        """
        title = input("Enter task title: ").strip()
        try:
            task = self._service.add_task(title)
            print(f"\nTask added successfully!")
            print(f"[{task.id}] [ ] {task.title}")
        except ValidationError as e:
            print(f"\nError: {e}")

    def handle_view(self) -> None:
        """Handle the View All Tasks menu option.

        Spec Reference: US2-AC1, US2-AC2, US2-AC3
        """
        tasks = self._service.get_all_tasks()

        if not tasks:
            print("\nNo tasks found.")
            return

        print("\n====================================")
        print("          YOUR TASKS")
        print("====================================")

        complete_count = 0
        for task in tasks:
            status = "x" if task.is_complete else " "
            print(f"[{task.id}] [{status}] {task.title}")
            if task.is_complete:
                complete_count += 1

        print("====================================")
        print(f"Total: {len(tasks)} tasks ({complete_count} complete, {len(tasks) - complete_count} incomplete)")

    def handle_update(self) -> None:
        """Handle the Update Task menu option.

        Spec Reference: US4-AC1, US4-AC2, US4-AC3
        """
        task_id = self._get_task_id()
        if task_id is None:
            return

        new_title = input("Enter new title: ").strip()
        try:
            task = self._service.update_task(task_id, new_title)
            print(f"\nTask updated successfully!")
            status = "x" if task.is_complete else " "
            print(f"[{task.id}] [{status}] {task.title}")
        except TaskNotFoundError as e:
            print(f"\nError: {e}")
        except ValidationError as e:
            print(f"\nError: {e}")

    def handle_delete(self) -> None:
        """Handle the Delete Task menu option.

        Spec Reference: US5-AC1, US5-AC2
        """
        task_id = self._get_task_id()
        if task_id is None:
            return

        try:
            self._service.delete_task(task_id)
            print(f"\nTask {task_id} deleted successfully!")
        except TaskNotFoundError as e:
            print(f"\nError: {e}")

    def handle_mark_complete(self) -> None:
        """Handle the Mark Task Complete menu option.

        Spec Reference: US3-AC1, US3-AC3
        """
        task_id = self._get_task_id()
        if task_id is None:
            return

        try:
            task = self._service.mark_complete(task_id)
            print(f"\nTask marked as complete!")
            print(f"[{task.id}] [x] {task.title}")
        except TaskNotFoundError as e:
            print(f"\nError: {e}")

    def handle_mark_incomplete(self) -> None:
        """Handle the Mark Task Incomplete menu option.

        Spec Reference: US3-AC2, US3-AC3
        """
        task_id = self._get_task_id()
        if task_id is None:
            return

        try:
            task = self._service.mark_incomplete(task_id)
            print(f"\nTask marked as incomplete!")
            print(f"[{task.id}] [ ] {task.title}")
        except TaskNotFoundError as e:
            print(f"\nError: {e}")

    def run(self) -> None:
        """Run the todo application main loop.

        Spec Reference: US6-AC1, US6-AC2, US6-AC3, US6-AC4
        Plan Reference: DD-005 (Menu Loop Structure)
        """
        print("\n====================================")
        print("   Welcome to Todo List App!")
        print("====================================")

        self._running = True
        while self._running:
            self.display_menu()
            choice = self.get_choice()

            match choice:
                case "1":
                    self.handle_add()
                case "2":
                    self.handle_view()
                case "3":
                    self.handle_update()
                case "4":
                    self.handle_delete()
                case "5":
                    self.handle_mark_complete()
                case "6":
                    self.handle_mark_incomplete()
                case "7":
                    self._running = False
                    print("\nGoodbye! Your tasks were not saved (in-memory only).")
                case _:
                    print("\nInvalid option. Please try again.")

            if self._running:
                input("\nPress Enter to continue...")
