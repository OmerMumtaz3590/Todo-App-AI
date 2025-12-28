# Implementation Plan: Phase I — In-Memory Todo Console Application

**Branch**: `phase-1-inmemory-todo` | **Date**: 2025-12-27 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/phase-1-inmemory-todo/spec.md`

---

## Summary

Implement a single-user, in-memory todo list console application in Python. The application provides a menu-driven CLI interface for basic CRUD operations on tasks. All data is stored in memory using Python's built-in data structures with no external dependencies.

---

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: None (Python standard library only)
**Storage**: In-memory (Python dict)
**Testing**: Manual testing via CLI (unit tests optional for Phase I)
**Target Platform**: Any platform with Python 3.11+ (Windows, macOS, Linux)
**Project Type**: Single project (console application)
**Performance Goals**: Instant response for all operations (< 100ms)
**Constraints**: No external dependencies, no file I/O, no network
**Scale/Scope**: Single user, unlimited tasks (memory permitting)

---

## Constitution Check

*GATE: Must pass before implementation. All items verified.*

**Phase Compliance** (per Constitution Section III):
- [x] Current phase identified: Phase I
- [x] No future-phase technologies used (RULE PG-002)
- [x] Architecture appropriate for current phase (RULE PG-003)

**Spec-Driven Compliance** (per Constitution Section I):
- [x] Specification approved before this plan (RULE SDD-004)
- [x] No features beyond specification scope (RULE SDD-002)

**Technology Compliance** (per Constitution Section IV):
- [x] Only phase-appropriate technologies used (RULE TC-001)
- [x] Additional libraries justified: None required (RULE TC-003)

**Quality Compliance** (per Constitution Section V):
- [x] Clean architecture principles followed (RULE QP-001 to QP-004)
- [x] Type hints planned for all public functions (RULE QP-008)
- [x] Error handling strategy defined (RULE QP-009)

**Phase I Prohibitions Verified**:
- [x] No database connections or ORM usage
- [x] No file system persistence
- [x] No network operations or HTTP
- [x] No authentication or authorization
- [x] No multi-user support
- [x] No web frameworks
- [x] No external service integrations
- [x] No async operations

---

## Project Structure

### Documentation (this feature)

```text
specs/phase-1-inmemory-todo/
├── spec.md              # Feature specification (approved)
├── plan.md              # This file
└── tasks.md             # Implementation tasks
```

### Source Code (repository root)

```text
src/
├── __init__.py          # Package marker
├── main.py              # Application entry point
├── models/
│   ├── __init__.py      # Package marker
│   └── task.py          # Task data model
├── services/
│   ├── __init__.py      # Package marker
│   └── task_service.py  # Business logic for task operations
└── cli/
    ├── __init__.py      # Package marker
    └── menu.py          # CLI menu and user interaction

tests/
└── (optional for Phase I)
```

**Structure Decision**: Single project layout with clear separation between:
- **models/**: Data structures (Task dataclass)
- **services/**: Business logic (TaskService with in-memory storage)
- **cli/**: User interface (menu display and input handling)

---

## Architecture Design

### Component Diagram

```
┌─────────────────────────────────────────────────────────┐
│                      main.py                            │
│                  (Entry Point)                          │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    cli/menu.py                          │
│              (User Interface Layer)                     │
│  - Display menu                                         │
│  - Get user input                                       │
│  - Format output                                        │
│  - Handle invalid input                                 │
└─────────────────────────┬───────────────────────────────┘
                          │ calls
                          ▼
┌─────────────────────────────────────────────────────────┐
│               services/task_service.py                  │
│                (Business Logic Layer)                   │
│  - Add task                                             │
│  - Get all tasks                                        │
│  - Get task by ID                                       │
│  - Update task                                          │
│  - Delete task                                          │
│  - Mark complete/incomplete                             │
│  - ID generation                                        │
└─────────────────────────┬───────────────────────────────┘
                          │ uses
                          ▼
┌─────────────────────────────────────────────────────────┐
│                  models/task.py                         │
│                   (Data Layer)                          │
│  - Task dataclass                                       │
│  - Field definitions                                    │
└─────────────────────────────────────────────────────────┘
```

### Data Flow

1. **User Input** → `menu.py` captures and validates input format
2. **Menu Selection** → `menu.py` calls appropriate `TaskService` method
3. **Business Logic** → `task_service.py` performs operation, validates business rules
4. **Data Access** → `task_service.py` reads/writes to in-memory dict
5. **Response** → `task_service.py` returns result or raises exception
6. **Output** → `menu.py` formats and displays result to user

---

## Design Decisions

### DD-001: In-Memory Storage Structure

**Decision**: Use a Python `dict[int, Task]` for task storage with task ID as key.

**Rationale**:
- O(1) lookup by ID for get, update, delete operations
- Simple iteration for list all tasks
- No external dependencies required
- Appropriate for Phase I scope

**Alternatives Considered**:
- List with linear search: Rejected — O(n) lookup performance
- SQLite: Rejected — Violates Phase I constraints (no persistence)

### DD-002: ID Generation Strategy

**Decision**: Use a monotonically increasing integer counter, never reusing IDs.

**Rationale**:
- Prevents confusion when tasks are deleted
- Simple implementation with a class variable
- Matches specification requirement (FR-002)

**Implementation**:
```python
class TaskService:
    _next_id: int = 1

    def _generate_id(self) -> int:
        task_id = self._next_id
        self._next_id += 1
        return task_id
```

### DD-003: Error Handling Strategy

**Decision**: Use custom exceptions for business logic errors, return values for success.

**Rationale**:
- Clean separation between expected errors and unexpected failures
- CLI layer can catch and format error messages appropriately
- Follows Python conventions

**Custom Exceptions**:
- `TaskNotFoundError`: When task ID doesn't exist
- `ValidationError`: When input validation fails (empty title)

### DD-004: Task Model Implementation

**Decision**: Use Python `dataclass` for the Task model.

**Rationale**:
- Built-in to Python 3.7+ (no dependencies)
- Automatic `__init__`, `__repr__`, `__eq__`
- Type hints included
- Immutable option available if needed later

### DD-005: CLI Menu Loop Structure

**Decision**: Implement a while loop with match-case statement for menu handling.

**Rationale**:
- Clean, readable menu routing
- Easy to extend with new options
- match-case available in Python 3.10+

---

## Module Specifications

### models/task.py

```python
@dataclass
class Task:
    id: int
    title: str
    is_complete: bool = False
```

**Responsibilities**:
- Define Task data structure
- Provide type hints for all fields
- Set default values

### services/task_service.py

```python
class TaskService:
    def add_task(self, title: str) -> Task
    def get_all_tasks(self) -> list[Task]
    def get_task(self, task_id: int) -> Task
    def update_task(self, task_id: int, title: str) -> Task
    def delete_task(self, task_id: int) -> None
    def mark_complete(self, task_id: int) -> Task
    def mark_incomplete(self, task_id: int) -> Task
```

**Responsibilities**:
- Manage in-memory task storage
- Generate unique task IDs
- Validate business rules (non-empty title)
- Raise appropriate exceptions for errors

### cli/menu.py

```python
class TodoMenu:
    def run(self) -> None          # Main application loop
    def display_menu(self) -> None  # Show menu options
    def get_choice(self) -> str     # Get user menu selection
    def handle_add(self) -> None
    def handle_view(self) -> None
    def handle_update(self) -> None
    def handle_delete(self) -> None
    def handle_mark_complete(self) -> None
    def handle_mark_incomplete(self) -> None
```

**Responsibilities**:
- Display menu and prompts
- Capture user input
- Validate input format (numeric IDs)
- Call TaskService methods
- Format and display results/errors
- Handle application lifecycle (welcome, exit)

### main.py

```python
def main() -> None:
    menu = TodoMenu()
    menu.run()

if __name__ == "__main__":
    main()
```

**Responsibilities**:
- Application entry point
- Initialize and run the menu

---

## Error Handling Matrix

| Error Condition | Exception/Handling | User Message |
|-----------------|-------------------|--------------|
| Empty task title | `ValidationError` | "Task title cannot be empty" |
| Whitespace-only title | `ValidationError` | "Task title cannot be empty" |
| Task ID not found | `TaskNotFoundError` | "Task with ID {id} not found" |
| Non-numeric menu choice | Input validation | "Invalid option. Please try again." |
| Non-numeric task ID | Input validation | "Invalid ID. Please enter a number." |

---

## CLI Menu Design

```
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

Enter your choice (1-7): _
```

### Task List Display Format

```
====================================
          YOUR TASKS
====================================
[1] [ ] Buy groceries
[2] [x] Call mom
[3] [ ] Finish report
====================================
Total: 3 tasks (1 complete, 2 incomplete)
```

---

## Complexity Tracking

> No violations identified — Phase I design is minimal and appropriate.

| Aspect | Complexity Level | Justification |
|--------|-----------------|---------------|
| Storage | Minimal | Single dict, no persistence |
| Architecture | Simple | 3 layers, clear separation |
| Dependencies | None | Standard library only |
| Error handling | Basic | 2 custom exceptions |

---

## Implementation Notes

1. **Type Hints**: All public functions must have complete type hints
2. **Docstrings**: All public classes and methods should have docstrings
3. **Input Validation**: Validate at CLI layer (format) and service layer (business rules)
4. **No Global State**: TaskService instance holds all state
5. **Testability**: Service layer can be unit tested independently of CLI
