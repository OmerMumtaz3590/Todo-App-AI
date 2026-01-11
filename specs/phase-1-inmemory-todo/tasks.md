# Tasks: Phase I — In-Memory Todo Console Application

**Input**: Design documents from `specs/phase-1-inmemory-todo/`
**Prerequisites**: spec.md (approved), plan.md (approved)
**Branch**: `phase-1-inmemory-todo`
**Created**: 2025-12-27

---

## Constitution Compliance

**Pre-Task Gate** (per Constitution Section VII):
- [x] Plan is approved (RULE SDD-005)
- [x] Constitution Check in plan passes
- [x] Technical context is complete
- [x] Project structure is defined

**Agent Behavior Rules** (per Constitution Section II):
- [x] All tasks trace to specification requirements (RULE ABR-002)
- [x] No feature invention in task list (RULE ABR-002)
- [x] No future-phase work included (RULE ABR-006)
- [x] All tasks have clear, verifiable deliverables (RULE ABR-008)

---

## Task Format

```
[ID] [Flags] Description
```

- **[P]**: Can run in parallel (different files, no dependencies)
- **[US#]**: Maps to User Story number from spec.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and directory structure
**Spec Reference**: NFR-002 (Python 3.11+), NFR-003 (no external dependencies)
**Plan Reference**: Project Structure section

---

### T001 — Create Project Directory Structure

**Description**: Create the source code directory structure as defined in plan.md

**Preconditions**: None

**Expected Output**: Directory structure exists and is ready for code

**Artifacts Created**:
```
src/
├── __init__.py
├── main.py (empty placeholder)
├── models/
│   └── __init__.py
├── services/
│   └── __init__.py
└── cli/
    └── __init__.py
```

**Spec Reference**: N/A (infrastructure)
**Plan Reference**: Project Structure → Source Code

**Verification**:
- [ ] All directories exist
- [ ] All `__init__.py` files exist (can be empty)
- [ ] `main.py` exists as placeholder

---

### T002 — Create Custom Exception Classes

**Description**: Create exception classes for error handling

**Preconditions**: T001 complete (directory structure exists)

**Expected Output**: Exception module with `TaskNotFoundError` and `ValidationError`

**Artifacts Created**:
- `src/exceptions.py`

**Implementation**:
```python
class TaskNotFoundError(Exception):
    """Raised when a task with the given ID does not exist."""
    pass

class ValidationError(Exception):
    """Raised when input validation fails."""
    pass
```

**Spec Reference**: FR-009 (validate input, display error messages)
**Plan Reference**: DD-003 (Error Handling Strategy)

**Verification**:
- [ ] `TaskNotFoundError` class exists
- [ ] `ValidationError` class exists
- [ ] Both inherit from `Exception`
- [ ] Both have docstrings

---

## Phase 2: Data Model (Foundation)

**Purpose**: Define the Task data structure
**Spec Reference**: Key Entities → Task
**Plan Reference**: models/task.py, DD-004

---

### T003 — Implement Task Data Model

**Description**: Create the Task dataclass with all required fields

**Preconditions**: T001 complete

**Expected Output**: Task dataclass with id, title, is_complete fields

**Artifacts Created**:
- `src/models/task.py`

**Implementation Details**:
```python
from dataclasses import dataclass

@dataclass
class Task:
    """Represents a todo task.

    Attributes:
        id: Unique identifier for the task (positive integer)
        title: Description of the task (non-empty string)
        is_complete: Whether the task is marked as done (default: False)
    """
    id: int
    title: str
    is_complete: bool = False
```

**Spec Reference**: Key Entities → Task (id: int, title: str, is_complete: bool)
**Plan Reference**: DD-004 (Task Model Implementation), models/task.py

**Verification**:
- [ ] Task class is a dataclass
- [ ] Has `id` field of type `int`
- [ ] Has `title` field of type `str`
- [ ] Has `is_complete` field of type `bool` with default `False`
- [ ] Has complete docstring
- [ ] Type hints present for all fields

---

### T004 — Update models/__init__.py Exports

**Description**: Export Task class from models package

**Preconditions**: T003 complete

**Expected Output**: Task can be imported from `src.models`

**Artifacts Modified**:
- `src/models/__init__.py`

**Implementation**:
```python
from .task import Task

__all__ = ["Task"]
```

**Spec Reference**: N/A (infrastructure)
**Plan Reference**: Project Structure

**Verification**:
- [ ] `from src.models import Task` works
- [ ] `__all__` defined

---

## Phase 3: Business Logic (Service Layer)

**Purpose**: Implement task management business logic
**Spec Reference**: FR-001 through FR-011
**Plan Reference**: services/task_service.py, DD-001, DD-002

---

### T005 — Implement TaskService Class Structure

**Description**: Create TaskService class with storage and ID generation

**Preconditions**: T002, T003, T004 complete

**Expected Output**: TaskService class with in-memory storage and ID generation

**Artifacts Created**:
- `src/services/task_service.py`

**Implementation Details**:
```python
from src.models import Task
from src.exceptions import TaskNotFoundError, ValidationError

class TaskService:
    """Service for managing todo tasks in memory."""

    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def _generate_id(self) -> int:
        """Generate a unique task ID (never reused)."""
        task_id = self._next_id
        self._next_id += 1
        return task_id
```

**Spec Reference**: FR-002 (unique, auto-incrementing IDs), FR-011 (in-memory storage)
**Plan Reference**: DD-001 (Storage Structure), DD-002 (ID Generation)

**Verification**:
- [ ] Class has `_tasks` dict for storage
- [ ] Class has `_next_id` counter starting at 1
- [ ] `_generate_id()` returns incrementing IDs
- [ ] IDs are never reused (counter only increments)
- [ ] Type hints present
- [ ] Docstrings present

---

### T006 — Implement add_task Method

**Description**: Add method to create new tasks

**Preconditions**: T005 complete

**Expected Output**: Method that creates and stores a new task

**Artifacts Modified**:
- `src/services/task_service.py`

**Implementation Details**:
```python
def add_task(self, title: str) -> Task:
    """Add a new task with the given title.

    Args:
        title: The task description (must be non-empty)

    Returns:
        The newly created Task

    Raises:
        ValidationError: If title is empty or whitespace-only
    """
    if not title or not title.strip():
        raise ValidationError("Task title cannot be empty")

    task_id = self._generate_id()
    task = Task(id=task_id, title=title.strip())
    self._tasks[task_id] = task
    return task
```

**Spec Reference**: FR-001 (add tasks), US1-AC2 (empty string error), US1-AC3 (whitespace error)
**Plan Reference**: services/task_service.py → add_task

**Verification**:
- [ ] Creates task with unique ID
- [ ] Stores task in `_tasks` dict
- [ ] Returns the created Task
- [ ] Raises `ValidationError` for empty title
- [ ] Raises `ValidationError` for whitespace-only title
- [ ] Strips whitespace from valid titles
- [ ] Type hints present
- [ ] Docstring present

---

### T007 — Implement get_all_tasks Method

**Description**: Add method to retrieve all tasks

**Preconditions**: T005 complete

**Expected Output**: Method that returns list of all tasks

**Artifacts Modified**:
- `src/services/task_service.py`

**Implementation Details**:
```python
def get_all_tasks(self) -> list[Task]:
    """Get all tasks.

    Returns:
        List of all tasks (may be empty)
    """
    return list(self._tasks.values())
```

**Spec Reference**: FR-003 (view all tasks)
**Plan Reference**: services/task_service.py → get_all_tasks

**Verification**:
- [ ] Returns list of Task objects
- [ ] Returns empty list when no tasks exist
- [ ] Returns all stored tasks
- [ ] Type hints present
- [ ] Docstring present

---

### T008 — Implement get_task Method

**Description**: Add method to retrieve a single task by ID

**Preconditions**: T005 complete

**Expected Output**: Method that returns a task by ID or raises error

**Artifacts Modified**:
- `src/services/task_service.py`

**Implementation Details**:
```python
def get_task(self, task_id: int) -> Task:
    """Get a task by ID.

    Args:
        task_id: The ID of the task to retrieve

    Returns:
        The Task with the given ID

    Raises:
        TaskNotFoundError: If no task with the given ID exists
    """
    if task_id not in self._tasks:
        raise TaskNotFoundError(f"Task with ID {task_id} not found")
    return self._tasks[task_id]
```

**Spec Reference**: US3-AC3 (task not found error), US4-AC2, US5-AC2
**Plan Reference**: services/task_service.py → get_task

**Verification**:
- [ ] Returns Task for valid ID
- [ ] Raises `TaskNotFoundError` for invalid ID
- [ ] Error message includes the ID
- [ ] Type hints present
- [ ] Docstring present

---

### T009 — Implement update_task Method

**Description**: Add method to update a task's title

**Preconditions**: T005, T008 complete

**Expected Output**: Method that updates task title and returns updated task

**Artifacts Modified**:
- `src/services/task_service.py`

**Implementation Details**:
```python
def update_task(self, task_id: int, title: str) -> Task:
    """Update a task's title.

    Args:
        task_id: The ID of the task to update
        title: The new title (must be non-empty)

    Returns:
        The updated Task

    Raises:
        TaskNotFoundError: If no task with the given ID exists
        ValidationError: If title is empty or whitespace-only
    """
    if not title or not title.strip():
        raise ValidationError("Task title cannot be empty")

    task = self.get_task(task_id)  # Raises TaskNotFoundError if not found
    task.title = title.strip()
    return task
```

**Spec Reference**: FR-004 (update title), US4-AC1 (successful update), US4-AC2 (not found), US4-AC3 (empty title)
**Plan Reference**: services/task_service.py → update_task

**Verification**:
- [ ] Updates task title for valid ID
- [ ] Returns the updated Task
- [ ] Raises `TaskNotFoundError` for invalid ID
- [ ] Raises `ValidationError` for empty title
- [ ] Does not change title if validation fails
- [ ] Strips whitespace from new title
- [ ] Type hints present
- [ ] Docstring present

---

### T010 — Implement delete_task Method

**Description**: Add method to delete a task by ID

**Preconditions**: T005, T008 complete

**Expected Output**: Method that removes a task from storage

**Artifacts Modified**:
- `src/services/task_service.py`

**Implementation Details**:
```python
def delete_task(self, task_id: int) -> None:
    """Delete a task by ID.

    Args:
        task_id: The ID of the task to delete

    Raises:
        TaskNotFoundError: If no task with the given ID exists
    """
    if task_id not in self._tasks:
        raise TaskNotFoundError(f"Task with ID {task_id} not found")
    del self._tasks[task_id]
```

**Spec Reference**: FR-005 (delete task), US5-AC1 (successful delete), US5-AC2 (not found), US5-AC3 (ID not reused)
**Plan Reference**: services/task_service.py → delete_task

**Verification**:
- [ ] Removes task from storage
- [ ] Raises `TaskNotFoundError` for invalid ID
- [ ] Does not affect `_next_id` (IDs not reused)
- [ ] Type hints present
- [ ] Docstring present

---

### T011 — Implement mark_complete Method

**Description**: Add method to mark a task as complete

**Preconditions**: T005, T008 complete

**Expected Output**: Method that sets is_complete to True

**Artifacts Modified**:
- `src/services/task_service.py`

**Implementation Details**:
```python
def mark_complete(self, task_id: int) -> Task:
    """Mark a task as complete.

    Args:
        task_id: The ID of the task to mark complete

    Returns:
        The updated Task

    Raises:
        TaskNotFoundError: If no task with the given ID exists
    """
    task = self.get_task(task_id)
    task.is_complete = True
    return task
```

**Spec Reference**: FR-006 (mark complete), US3-AC1 (successful mark complete)
**Plan Reference**: services/task_service.py → mark_complete

**Verification**:
- [ ] Sets `is_complete` to `True`
- [ ] Returns the updated Task
- [ ] Raises `TaskNotFoundError` for invalid ID
- [ ] Type hints present
- [ ] Docstring present

---

### T012 — Implement mark_incomplete Method

**Description**: Add method to mark a task as incomplete

**Preconditions**: T005, T008 complete

**Expected Output**: Method that sets is_complete to False

**Artifacts Modified**:
- `src/services/task_service.py`

**Implementation Details**:
```python
def mark_incomplete(self, task_id: int) -> Task:
    """Mark a task as incomplete.

    Args:
        task_id: The ID of the task to mark incomplete

    Returns:
        The updated Task

    Raises:
        TaskNotFoundError: If no task with the given ID exists
    """
    task = self.get_task(task_id)
    task.is_complete = False
    return task
```

**Spec Reference**: FR-007 (mark incomplete), US3-AC2 (successful mark incomplete)
**Plan Reference**: services/task_service.py → mark_incomplete

**Verification**:
- [ ] Sets `is_complete` to `False`
- [ ] Returns the updated Task
- [ ] Raises `TaskNotFoundError` for invalid ID
- [ ] Type hints present
- [ ] Docstring present

---

### T013 — Update services/__init__.py Exports

**Description**: Export TaskService class from services package

**Preconditions**: T012 complete (all service methods implemented)

**Expected Output**: TaskService can be imported from `src.services`

**Artifacts Modified**:
- `src/services/__init__.py`

**Implementation**:
```python
from .task_service import TaskService

__all__ = ["TaskService"]
```

**Spec Reference**: N/A (infrastructure)
**Plan Reference**: Project Structure

**Verification**:
- [ ] `from src.services import TaskService` works
- [ ] `__all__` defined

---

## Phase 4: User Interface (CLI Layer)

**Purpose**: Implement menu-driven command line interface
**Spec Reference**: FR-008 (menu interface), FR-009 (validation), FR-010 (exit), US6
**Plan Reference**: cli/menu.py, CLI Menu Design

---

### T014 — Implement TodoMenu Class Structure

**Description**: Create TodoMenu class with service dependency

**Preconditions**: T013 complete

**Expected Output**: TodoMenu class with TaskService instance

**Artifacts Created**:
- `src/cli/menu.py`

**Implementation Details**:
```python
from src.services import TaskService
from src.exceptions import TaskNotFoundError, ValidationError

class TodoMenu:
    """Command-line interface for the todo application."""

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
        self._service = TaskService()
        self._running = False
```

**Spec Reference**: FR-008 (menu-driven interface)
**Plan Reference**: cli/menu.py, CLI Menu Design

**Verification**:
- [ ] Class has `_service` attribute (TaskService)
- [ ] Class has `_running` attribute for loop control
- [ ] `MENU_OPTIONS` constant matches plan design
- [ ] Type hints present
- [ ] Docstring present

---

### T015 — Implement display_menu and get_choice Methods

**Description**: Add methods to show menu and get user selection

**Preconditions**: T014 complete

**Expected Output**: Methods for menu display and input capture

**Artifacts Modified**:
- `src/cli/menu.py`

**Implementation Details**:
```python
def display_menu(self) -> None:
    """Display the main menu."""
    print(self.MENU_OPTIONS, end="")

def get_choice(self) -> str:
    """Get the user's menu choice.

    Returns:
        The user's input as a string
    """
    return input().strip()
```

**Spec Reference**: FR-008 (menu-driven interface)
**Plan Reference**: cli/menu.py → display_menu, get_choice

**Verification**:
- [ ] `display_menu()` prints the menu
- [ ] `get_choice()` returns user input
- [ ] Input is stripped of whitespace
- [ ] Type hints present
- [ ] Docstring present

---

### T016 — Implement _get_task_id Helper Method

**Description**: Add helper method to get and validate task ID input

**Preconditions**: T014 complete

**Expected Output**: Method that prompts for ID and returns int or None

**Artifacts Modified**:
- `src/cli/menu.py`

**Implementation Details**:
```python
def _get_task_id(self, prompt: str = "Enter task ID: ") -> int | None:
    """Get a task ID from the user.

    Args:
        prompt: The prompt to display

    Returns:
        The task ID as an integer, or None if invalid
    """
    try:
        return int(input(prompt).strip())
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return None
```

**Spec Reference**: US3-AC4 (invalid ID error), US4-AC2, US5-AC2
**Plan Reference**: Error Handling Matrix

**Verification**:
- [ ] Prompts user for input
- [ ] Returns int for valid numeric input
- [ ] Returns None for non-numeric input
- [ ] Prints error message for invalid input
- [ ] Type hints present
- [ ] Docstring present

---

### T017 — Implement handle_add Method

**Description**: Add handler for "Add Task" menu option

**Preconditions**: T014, T006 complete

**Expected Output**: Method that adds a task via user input

**Artifacts Modified**:
- `src/cli/menu.py`

**Implementation Details**:
```python
def handle_add(self) -> None:
    """Handle the Add Task menu option."""
    title = input("Enter task title: ").strip()
    try:
        task = self._service.add_task(title)
        print(f"\nTask added successfully!")
        print(f"[{task.id}] [ ] {task.title}")
    except ValidationError as e:
        print(f"\nError: {e}")
```

**Spec Reference**: US1-AC1 (successful add), US1-AC2 (empty error), US1-AC3 (whitespace error)
**Plan Reference**: cli/menu.py → handle_add

**Verification**:
- [ ] Prompts for task title
- [ ] Calls `_service.add_task()`
- [ ] Displays success message with task details
- [ ] Catches and displays `ValidationError`
- [ ] Type hints present
- [ ] Docstring present

---

### T018 — Implement handle_view Method

**Description**: Add handler for "View All Tasks" menu option

**Preconditions**: T014, T007 complete

**Expected Output**: Method that displays all tasks

**Artifacts Modified**:
- `src/cli/menu.py`

**Implementation Details**:
```python
def handle_view(self) -> None:
    """Handle the View All Tasks menu option."""
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
```

**Spec Reference**: US2-AC1 (empty list), US2-AC2 (single task), US2-AC3 (multiple tasks)
**Plan Reference**: cli/menu.py → handle_view, Task List Display Format

**Verification**:
- [ ] Displays "No tasks found." for empty list
- [ ] Displays all tasks with ID, status, title
- [ ] Shows `[x]` for complete, `[ ]` for incomplete
- [ ] Shows total count with breakdown
- [ ] Type hints present
- [ ] Docstring present

---

### T019 — Implement handle_update Method

**Description**: Add handler for "Update Task" menu option

**Preconditions**: T014, T016, T009 complete

**Expected Output**: Method that updates a task title via user input

**Artifacts Modified**:
- `src/cli/menu.py`

**Implementation Details**:
```python
def handle_update(self) -> None:
    """Handle the Update Task menu option."""
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
```

**Spec Reference**: US4-AC1 (successful update), US4-AC2 (not found), US4-AC3 (empty title)
**Plan Reference**: cli/menu.py → handle_update

**Verification**:
- [ ] Prompts for task ID
- [ ] Returns early if ID invalid
- [ ] Prompts for new title
- [ ] Calls `_service.update_task()`
- [ ] Displays success message
- [ ] Catches and displays `TaskNotFoundError`
- [ ] Catches and displays `ValidationError`
- [ ] Type hints present
- [ ] Docstring present

---

### T020 — Implement handle_delete Method

**Description**: Add handler for "Delete Task" menu option

**Preconditions**: T014, T016, T010 complete

**Expected Output**: Method that deletes a task via user input

**Artifacts Modified**:
- `src/cli/menu.py`

**Implementation Details**:
```python
def handle_delete(self) -> None:
    """Handle the Delete Task menu option."""
    task_id = self._get_task_id()
    if task_id is None:
        return

    try:
        self._service.delete_task(task_id)
        print(f"\nTask {task_id} deleted successfully!")
    except TaskNotFoundError as e:
        print(f"\nError: {e}")
```

**Spec Reference**: US5-AC1 (successful delete), US5-AC2 (not found)
**Plan Reference**: cli/menu.py → handle_delete

**Verification**:
- [ ] Prompts for task ID
- [ ] Returns early if ID invalid
- [ ] Calls `_service.delete_task()`
- [ ] Displays success message
- [ ] Catches and displays `TaskNotFoundError`
- [ ] Type hints present
- [ ] Docstring present

---

### T021 — Implement handle_mark_complete Method

**Description**: Add handler for "Mark Task Complete" menu option

**Preconditions**: T014, T016, T011 complete

**Expected Output**: Method that marks a task complete via user input

**Artifacts Modified**:
- `src/cli/menu.py`

**Implementation Details**:
```python
def handle_mark_complete(self) -> None:
    """Handle the Mark Task Complete menu option."""
    task_id = self._get_task_id()
    if task_id is None:
        return

    try:
        task = self._service.mark_complete(task_id)
        print(f"\nTask marked as complete!")
        print(f"[{task.id}] [x] {task.title}")
    except TaskNotFoundError as e:
        print(f"\nError: {e}")
```

**Spec Reference**: US3-AC1 (successful mark complete), US3-AC3 (not found)
**Plan Reference**: cli/menu.py → handle_mark_complete

**Verification**:
- [ ] Prompts for task ID
- [ ] Returns early if ID invalid
- [ ] Calls `_service.mark_complete()`
- [ ] Displays success message
- [ ] Catches and displays `TaskNotFoundError`
- [ ] Type hints present
- [ ] Docstring present

---

### T022 — Implement handle_mark_incomplete Method

**Description**: Add handler for "Mark Task Incomplete" menu option

**Preconditions**: T014, T016, T012 complete

**Expected Output**: Method that marks a task incomplete via user input

**Artifacts Modified**:
- `src/cli/menu.py`

**Implementation Details**:
```python
def handle_mark_incomplete(self) -> None:
    """Handle the Mark Task Incomplete menu option."""
    task_id = self._get_task_id()
    if task_id is None:
        return

    try:
        task = self._service.mark_incomplete(task_id)
        print(f"\nTask marked as incomplete!")
        print(f"[{task.id}] [ ] {task.title}")
    except TaskNotFoundError as e:
        print(f"\nError: {e}")
```

**Spec Reference**: US3-AC2 (successful mark incomplete), US3-AC3 (not found)
**Plan Reference**: cli/menu.py → handle_mark_incomplete

**Verification**:
- [ ] Prompts for task ID
- [ ] Returns early if ID invalid
- [ ] Calls `_service.mark_incomplete()`
- [ ] Displays success message
- [ ] Catches and displays `TaskNotFoundError`
- [ ] Type hints present
- [ ] Docstring present

---

### T023 — Implement run Method (Main Loop)

**Description**: Add main application loop with menu routing

**Preconditions**: T015, T017-T022 complete

**Expected Output**: Method that runs the application loop

**Artifacts Modified**:
- `src/cli/menu.py`

**Implementation Details**:
```python
def run(self) -> None:
    """Run the todo application main loop."""
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
```

**Spec Reference**: US6-AC1 (welcome message), US6-AC2 (exit), US6-AC3 (invalid option), US6-AC4 (non-numeric)
**Plan Reference**: cli/menu.py → run, DD-005 (Menu Loop Structure)

**Verification**:
- [ ] Displays welcome message on start
- [ ] Shows menu each iteration
- [ ] Routes to correct handler for options 1-6
- [ ] Exits cleanly for option 7 with goodbye message
- [ ] Displays error for invalid options
- [ ] Pauses between operations (Press Enter)
- [ ] Type hints present
- [ ] Docstring present

---

### T024 — Update cli/__init__.py Exports

**Description**: Export TodoMenu class from cli package

**Preconditions**: T023 complete

**Expected Output**: TodoMenu can be imported from `src.cli`

**Artifacts Modified**:
- `src/cli/__init__.py`

**Implementation**:
```python
from .menu import TodoMenu

__all__ = ["TodoMenu"]
```

**Spec Reference**: N/A (infrastructure)
**Plan Reference**: Project Structure

**Verification**:
- [ ] `from src.cli import TodoMenu` works
- [ ] `__all__` defined

---

## Phase 5: Application Entry Point

**Purpose**: Create main entry point and wire everything together
**Spec Reference**: FR-010 (clean exit)
**Plan Reference**: main.py

---

### T025 — Implement main.py Entry Point

**Description**: Create application entry point

**Preconditions**: T024 complete

**Expected Output**: Working application that can be run with `python -m src.main`

**Artifacts Modified**:
- `src/main.py`

**Implementation**:
```python
"""Todo List Application - Phase I

A simple in-memory todo list console application.
All data is lost when the application exits.

Usage:
    python -m src.main
"""

from src.cli import TodoMenu


def main() -> None:
    """Run the todo list application."""
    menu = TodoMenu()
    menu.run()


if __name__ == "__main__":
    main()
```

**Spec Reference**: FR-010 (clean exit), NFR-001 (single-user console app)
**Plan Reference**: main.py

**Verification**:
- [ ] Module docstring explains purpose
- [ ] `main()` function creates TodoMenu and runs it
- [ ] `if __name__ == "__main__"` guard present
- [ ] Application runs with `python -m src.main`
- [ ] Type hints present
- [ ] Docstring present

---

## Phase 6: Integration Testing (Manual)

**Purpose**: Verify all acceptance criteria are met
**Spec Reference**: All User Stories and Success Criteria

---

### T026 — Manual Test: Add Task Flow

**Description**: Test all Add Task acceptance scenarios

**Preconditions**: T025 complete

**Expected Output**: All US1 acceptance criteria pass

**Test Steps**:
1. Run application
2. Select "Add Task"
3. Enter "Buy groceries" → Verify task created with ID, shown correctly
4. Select "Add Task"
5. Enter empty string → Verify error message
6. Select "Add Task"
7. Enter "   " (whitespace) → Verify error message

**Spec Reference**: US1-AC1, US1-AC2, US1-AC3
**Plan Reference**: N/A

**Verification**:
- [ ] Task created with unique ID
- [ ] Confirmation message displayed
- [ ] Empty title rejected with error
- [ ] Whitespace title rejected with error

---

### T027 — Manual Test: View Task Flow

**Description**: Test all View Tasks acceptance scenarios

**Preconditions**: T026 complete

**Expected Output**: All US2 acceptance criteria pass

**Test Steps**:
1. Run fresh application
2. Select "View All Tasks" → Verify "No tasks found"
3. Add one task "Task A"
4. Select "View All Tasks" → Verify single task shown
5. Add another task "Task B"
6. Mark "Task A" complete
7. Select "View All Tasks" → Verify both tasks with correct status markers

**Spec Reference**: US2-AC1, US2-AC2, US2-AC3
**Plan Reference**: N/A

**Verification**:
- [ ] Empty list shows "No tasks found"
- [ ] Single task displays correctly
- [ ] Multiple tasks with status markers [x] and [ ]
- [ ] Total count accurate

---

### T028 — Manual Test: Update Task Flow

**Description**: Test all Update Task acceptance scenarios

**Preconditions**: T026 complete

**Expected Output**: All US4 acceptance criteria pass

**Test Steps**:
1. Add task "Original title"
2. Select "Update Task", enter ID, enter "New title" → Verify updated
3. Select "Update Task", enter non-existent ID 99 → Verify error
4. Select "Update Task", enter valid ID, enter empty title → Verify error

**Spec Reference**: US4-AC1, US4-AC2, US4-AC3
**Plan Reference**: N/A

**Verification**:
- [ ] Title updates successfully
- [ ] Non-existent ID shows error
- [ ] Empty title rejected with error

---

### T029 — Manual Test: Delete Task Flow

**Description**: Test all Delete Task acceptance scenarios

**Preconditions**: T026 complete

**Expected Output**: All US5 acceptance criteria pass

**Test Steps**:
1. Add task "To delete"
2. Note the ID
3. Select "Delete Task", enter ID → Verify deleted
4. Select "View All Tasks" → Verify task gone
5. Add new task → Verify ID is NOT reused
6. Select "Delete Task", enter non-existent ID 99 → Verify error

**Spec Reference**: US5-AC1, US5-AC2, US5-AC3
**Plan Reference**: N/A

**Verification**:
- [ ] Task deleted successfully
- [ ] Task no longer in list
- [ ] New task gets new ID (not reused)
- [ ] Non-existent ID shows error

---

### T030 — Manual Test: Mark Complete/Incomplete Flow

**Description**: Test all Mark Complete/Incomplete acceptance scenarios

**Preconditions**: T026 complete

**Expected Output**: All US3 acceptance criteria pass

**Test Steps**:
1. Add task "Test task"
2. Select "Mark Complete", enter ID → Verify marked complete
3. View tasks → Verify [x] marker
4. Select "Mark Incomplete", enter ID → Verify marked incomplete
5. View tasks → Verify [ ] marker
6. Select "Mark Complete", enter non-existent ID 99 → Verify error
7. Select "Mark Complete", enter "abc" → Verify "Invalid ID" error

**Spec Reference**: US3-AC1, US3-AC2, US3-AC3, US3-AC4
**Plan Reference**: N/A

**Verification**:
- [ ] Mark complete works
- [ ] Mark incomplete works
- [ ] Non-existent ID shows error
- [ ] Non-numeric ID shows error

---

### T031 — Manual Test: Application Lifecycle

**Description**: Test application start and exit

**Preconditions**: T025 complete

**Expected Output**: All US6 acceptance criteria pass

**Test Steps**:
1. Run application → Verify welcome message and menu
2. Enter invalid option "99" → Verify error, menu redisplays
3. Enter non-numeric "abc" → Verify error, menu redisplays
4. Select "Exit" → Verify goodbye message and clean exit

**Spec Reference**: US6-AC1, US6-AC2, US6-AC3, US6-AC4
**Plan Reference**: N/A

**Verification**:
- [ ] Welcome message on start
- [ ] Menu displays correctly
- [ ] Invalid option handled gracefully
- [ ] Non-numeric input handled gracefully
- [ ] Clean exit with goodbye message

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup)
    └── T001 (directories)
         └── T002 (exceptions)

Phase 2 (Data Model)
    └── T003 (Task model) ← depends on T001
         └── T004 (exports)

Phase 3 (Business Logic)
    └── T005 (TaskService structure) ← depends on T002, T003, T004
         ├── T006 (add_task)
         ├── T007 (get_all_tasks)
         ├── T008 (get_task)
         ├── T009 (update_task) ← depends on T008
         ├── T010 (delete_task) ← depends on T008
         ├── T011 (mark_complete) ← depends on T008
         └── T012 (mark_incomplete) ← depends on T008
              └── T013 (exports)

Phase 4 (CLI)
    └── T014 (TodoMenu structure) ← depends on T013
         ├── T015 (display_menu, get_choice)
         ├── T016 (_get_task_id helper)
         ├── T017 (handle_add) ← depends on T006
         ├── T018 (handle_view) ← depends on T007
         ├── T019 (handle_update) ← depends on T016, T009
         ├── T020 (handle_delete) ← depends on T016, T010
         ├── T021 (handle_mark_complete) ← depends on T016, T011
         └── T022 (handle_mark_incomplete) ← depends on T016, T012
              └── T023 (run method) ← depends on T015-T022
                   └── T024 (exports)

Phase 5 (Entry Point)
    └── T025 (main.py) ← depends on T024

Phase 6 (Testing)
    └── T026-T031 (manual tests) ← depends on T025
```

### Parallel Opportunities

Tasks that can be implemented in parallel (different files):

**Phase 2**:
- T003 and T002 can run in parallel (different files)

**Phase 3** (after T005):
- T006, T007, T008 can run in parallel (same file, but independent methods)

**Phase 4** (after T014):
- T015, T016 can run in parallel
- T017, T018, T019, T020, T021, T022 can run in parallel (after dependencies met)

**Phase 6**:
- All test tasks are sequential (depend on complete application)

---

## Summary

| Phase | Tasks | Purpose |
|-------|-------|---------|
| 1. Setup | T001-T002 | Project structure, exceptions |
| 2. Data Model | T003-T004 | Task dataclass |
| 3. Business Logic | T005-T013 | TaskService with all CRUD |
| 4. CLI | T014-T024 | Menu-driven interface |
| 5. Entry Point | T025 | main.py |
| 6. Testing | T026-T031 | Manual acceptance tests |

**Total Tasks**: 31
**Estimated Files Created**: 8
**Estimated Lines of Code**: ~350-400
