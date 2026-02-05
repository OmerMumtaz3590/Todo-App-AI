# Tasks: Advanced Cloud Deployment with Event-Driven Architecture

**Input**: Design documents from `/specs/005-advanced-cloud-deployment/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md
**Tests**: Not explicitly requested in specification. Manual verification via unit tests, integration tests, and E2E tests.

**Organization**: Tasks are organized by user story to enable independent implementation and testing of each story.

## Constitution Compliance

**Pre-Task Gate** (per Constitution Section VII):
- [x] Plan is approved (RULE SDD-005)
- [x] Constitution Check in plan passes
- [x] Technical context is complete
- [x] Project structure is defined

**Agent Behavior Rules** (per Constitution Section II):
- [x] All tasks trace to specification requirements (RULE ABR-002)
- [x] No feature invention in task list (RULE ABR-002)
- [x] No future-phase features included (RULE ABR-006)
- [x] All tasks have clear, verifiable deliverables (RULE ABR-008)

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., [US1], [US2], [US3], [US4])
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/` for all Python code
- **Frontend**: `frontend/` for all React/Next.js code
- **Models**: `backend/src/models/`
- **Services**: `backend/src/services/`
- **API Routes**: `backend/src/api/`
- **Dapr Integration**: `backend/src/dapr_integration/`
- **Events**: `backend/src/events/`
- **Dapr Components**: `specs/infra/dapr/components/`
- **Kafka Topics**: `specs/infra/kafka/topics/`
- **Helm Chart**: `specs/infra/helm/todo-chatbot/`
- **Infrastructure**: `specs/infra/`

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Initialize project with Phase V infrastructure components

- [x] T-V-001 Create specs/infra/dapr/components/ directory for Dapr component configurations - ARTIFACT CREATED
- [x] T-V-002 Create specs/infra/kafka/topics/ directory for Kafka topic definitions - ARTIFACT CREATED
- [x] T-V-003 Create specs/infra/cloud/aks/ directory for Azure AKS configurations - ARTIFACT CREATED
- [x] T-V-004 Update .gitignore with Dapr and Kafka related files/directories - ARTIFACT CREATED
- [x] T-V-005 Install Dapr SDK for Python in backend requirements.txt - ARTIFACT CREATED

## Phase 2: Foundational (Database & Model Updates)

**Purpose**: Update data models and database schema for new task fields
**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T-V-006 [P] Extend Task model with priority field in backend/src/models/todo.py (STRUC-001) - ARTIFACT CREATED
- [x] T-V-007 [P] Extend Task model with tags array field in backend/src/models/todo.py (STRUC-002) - ARTIFACT CREATED
- [x] T-V-008 [P] Extend Task model with due_date field in backend/src/models/todo.py (STRUC-003) - ARTIFACT CREATED
- [x] T-V-009 [P] Extend Task model with remind_at field in backend/src/models/todo.py (STRUC-004) - ARTIFACT CREATED
- [x] T-V-010 [P] Extend Task model with recurrence_rule field in backend/src/models/todo.py (STRUC-005) - ARTIFACT CREATED
- [x] T-V-011 [P] Create Alembic migration for new Task fields in backend/alembic/versions/003_add_phase_v_fields_to_todo.py (STRUC-010) - ARTIFACT CREATED
- [x] T-V-012 [P] Update SQLModel model relationships for new fields in backend/src/models/todo.py (STRUC-006) - ARTIFACT CREATED
- [x] T-V-013 [P] Create database index definitions for new fields in backend/src/models/todo.py (STRUC-007) - ARTIFACT CREATED
- [x] T-V-014 [P] Create Task schema extensions for Pydantic models in backend/src/models/todo.py (STRUC-008) - ARTIFACT CREATED
- [x] T-V-015 Update existing task-related services to handle new fields in backend/src/services/todo_service.py (STRUC-009) - ARTIFACT CREATED

**Checkpoint**: Database schema and models updated - foundation for all features is ready

---

## Phase 3: User Story 1 - Intermediate Task Management Features (Priority: P1) 🎯 MVP

**Goal**: Implement core organizational features (priorities, tags, search, filter, sort) to enhance task management

**Independent Test**: Create tasks with various priorities, tags, due dates, and verify that search, filter, and sort functions work correctly. A user should be able to efficiently find tasks using these features.

### Implementation for User Story 1

- [x] T-V-016 [US1] Update task creation API to accept priority parameter in backend/src/api/todos.py (US1-001) - ARTIFACT CREATED
- [x] T-V-017 [US1] Update task update API to accept priority parameter in backend/src/api/todos.py (US1-002) - ARTIFACT CREATED
- [x] T-V-018 [US1] Update task creation API to accept tags array parameter in backend/src/api/todos.py (US1-003) - ARTIFACT CREATED
- [x] T-V-019 [US1] Update task update API to accept tags array parameter in backend/src/api/todos.py (US1-004) - ARTIFACT CREATED
- [x] T-V-020 [US1] Implement priority filtering in task list API in backend/src/api/todos.py (US1-005) - ARTIFACT CREATED
- [x] T-V-021 [US1] Implement tags filtering in task list API in backend/src/api/todos.py (US1-006) - ARTIFACT CREATED
- [x] T-V-022 [US1] Implement keyword search across title/description/tags in backend/src/api/todos.py (US1-007) - ARTIFACT CREATED
- [x] T-V-023 [US1] Implement due date filtering in task list API in backend/src/api/todos.py (US1-008) - ARTIFACT CREATED
- [x] T-V-024 [US1] Implement priority sorting in task list API in backend/src/api/todos.py (US1-009) - ARTIFACT CREATED
- [x] T-V-025 [US1] Implement due date sorting in task list API in backend/src/api/todos.py (US1-010) - ARTIFACT CREATED
- [x] T-V-026 [US1] Implement alphabetical sorting in task list API in backend/src/api/todos.py (US1-011) - ARTIFACT CREATED
- [x] T-V-027 [US1] Create frontend components for priority selection in frontend/components/ (US1-012) - ARTIFACT CREATED
- [x] T-V-028 [US1] Create frontend components for tag management in frontend/components/ (US1-013) - ARTIFACT CREATED
- [x] T-V-029 [US1] Update task form to include priority and tags inputs in frontend/components/ (US1-014) - ARTIFACT CREATED
- [x] T-V-030 [US1] Create frontend search interface component in frontend/components/ (US1-015) - ARTIFACT CREATED
- [x] T-V-031 [US1] Create frontend filter panel component with priority/tags/date filters in frontend/components/ (US1-016) - ARTIFACT CREATED
- [x] T-V-032 [US1] Create frontend sorting controls component in frontend/components/ (US1-017) - ARTIFACT CREATED
- [x] T-V-033 [US1] Update frontend task list to support filtering/sorting/search in frontend/components/ (US1-018) - ARTIFACT CREATED
- [x] T-V-034 [US1] Update frontend API service to handle new parameters in frontend/services/ (US1-019) - ARTIFACT CREATED
- [x] T-V-035 [US1] Create TypeScript types for new task fields in frontend/types/ (US1-020) - ARTIFACT CREATED

**Verification for User Story 1**: Complete all acceptance scenarios from spec.md:
1. Given a task with high priority, When the user filters by priority, Then the task appears in the high priority filter results
2. Given tasks with different tags, When the user searches for a tag keyword, Then all tasks with that tag appear in search results
3. Given tasks with various statuses, When the user applies a status filter, Then only tasks with matching status are displayed
4. Given tasks with different due dates, When the user sorts by due date, Then tasks are displayed in chronological order
5. Given tasks with different priorities, When the user sorts by priority, Then tasks are displayed with high priority first
6. Given tasks with tags, When the user applies a tag filter, Then only tasks with that tag are displayed

**Checkpoint**: At this point, User Story 1 should be fully functional - users can manage tasks with priorities, tags, search, filter, and sort

---

## Phase 4: User Story 2 - Advanced Task Management Features (Priority: P2)

**Goal**: Implement recurring tasks and time-based reminder notifications to automate task management

**Independent Test**: Create a recurring task with daily frequency, verify it automatically generates new instances. Create a task with a due date and reminder, verify the notification arrives at the correct time.

### Implementation for User Story 2

- [x] T-V-036 [US2] Create RecurringTask model in backend/src/models/recurring_task.py (US2-001) - ARTIFACT CREATED
- [x] T-V-037 [US2] Create RecurringTaskService in backend/src/services/recurring_task_service.py (US2-002) - ARTIFACT CREATED
- [x] T-V-038 [US2] Create recurring task API endpoints in backend/src/api/recurring_tasks.py (US2-003) - ARTIFACT CREATED
- [x] T-V-039 [US2] Implement recurrence rule parsing logic in backend/src/services/recurring_task_service.py (US2-004) - ARTIFACT CREATED
- [x] T-V-040 [US2] Implement next occurrence calculation logic in backend/src/services/recurring_task_service.py (US2-005) - ARTIFACT CREATED
- [x] T-V-041 [US2] Create reminder scheduling service in backend/src/services/reminder_service.py (US2-006) - ARTIFACT CREATED
- [x] T-V-042 [US2] Create reminder model in backend/src/models/reminder.py (US2-007) - ARTIFACT CREATED
- [x] T-V-043 [US2] Implement recurring task generation logic in backend/src/services/recurring_task_service.py (US2-008) - ARTIFACT CREATED
- [x] T-V-044 [US2] Create frontend components for recurring task creation in frontend/components/ (US2-009) - ARTIFACT CREATED
- [x] T-V-045 [US2] Create frontend components for reminder settings in frontend/components/ (US2-010) - ARTIFACT CREATED
- [x] T-V-046 [US2] Update task form to include recurring rule and reminder inputs in frontend/components/ (US2-011) - ARTIFACT CREATED
- [x] T-V-047 [US2] Create recurring task API service in frontend/services/ (US2-012) - ARTIFACT CREATED
- [x] T-V-048 [US2] Update frontend task list to show recurring task indicators in frontend/components/ (US2-013) - ARTIFACT CREATED
- [x] T-V-049 [US2] Create TypeScript types for recurring tasks and reminders in frontend/types/ (US2-014) - ARTIFACT CREATED

**Verification for User Story 2**: Complete all acceptance scenarios from spec.md:
1. Given a recurring task with daily rule, When 24 hours pass, Then a new instance of the task is automatically created
2. Given a task with a due date and reminder time, When the reminder time arrives, Then the user receives a notification
3. Given a completed recurring task, When the task completes, Then the next occurrence is scheduled per the recurrence rule
4. Given multiple recurring task rules, When users create them, Then each follows its specific recurrence pattern independently
5. Given a task with due date, When user views upcoming tasks, Then the task appears in the appropriate timeline view
6. Given expired reminders, When the system runs cleanup, Then old reminder events are properly archived

**Checkpoint**: At this point, User Story 2 should be fully functional - users can create recurring tasks and set reminders

---

## Phase 5: User Story 3 - Event-Driven Architecture Implementation (Priority: P3)

**Goal**: Implement event-driven architecture with Kafka topics and Dapr for loose coupling and resilience

**Independent Test**: Trigger a task creation event, verify it propagates through the system correctly and reaches all interested consumers. Verify that state changes are properly synchronized across services.

### Event Schema Definition

- [x] T-V-050 [US3] Define TaskCreated event schema in backend/src/events/schemas.py (EVNT-001) - ARTIFACT CREATED
- [x] T-V-051 [US3] Define TaskUpdated event schema in backend/src/events/schemas.py (EVNT-002) - ARTIFACT CREATED
- [x] T-V-052 [US3] Define TaskCompleted event schema in backend/src/events/schemas.py (EVNT-003) - ARTIFACT CREATED
- [x] T-V-053 [US3] Define RecurringTaskCreated event schema in backend/src/events/schemas.py (EVNT-004) - ARTIFACT CREATED
- [x] T-V-054 [US3] Define ReminderScheduled event schema in backend/src/events/schemas.py (EVNT-005) - ARTIFACT CREATED
- [x] T-V-055 [US3] Define ReminderTriggered event schema in backend/src/events/schemas.py (EVNT-006) - ARTIFACT CREATED
- [x] T-V-056 [US3] Create event publisher utilities in backend/src/events/publisher.py (EVNT-007) - ARTIFACT CREATED
- [x] T-V-057 [US3] Create event subscriber utilities in backend/src/events/subscriber.py (EVNT-008) - ARTIFACT CREATED

### Dapr Components Setup

- [x] T-V-058 [US3] Create Dapr pubsub component for Kafka in specs/infra/dapr/components/pubsub.yaml (DAPR-001) - ARTIFACT CREATED
- [x] T-V-059 [US3] Create Dapr state store component for PostgreSQL in specs/infra/dapr/components/statestore.yaml (DAPR-002) - ARTIFACT CREATED
- [x] T-V-060 [US3] Create Dapr secret store component in specs/infra/dapr/components/secretstore.yaml (DAPR-003) - ARTIFACT CREATED
- [x] T-V-061 [US3] Create Dapr cron binding component for reminders in specs/infra/dapr/components/bindings.yaml (DAPR-004) - ARTIFACT CREATED
- [x] T-V-062 [US3] Update backend deployment with Dapr annotations in specs/infra/helm/todo-chatbot/templates/backend-deployment.yaml (DAPR-005) - ARTIFACT CREATED
- [x] T-V-063 [US3] Update frontend deployment with Dapr annotations in specs/infra/helm/todo-chatbot/templates/frontend-deployment.yaml (DAPR-006) - ARTIFACT CREATED

### Event Publishing & Consumption

- [x] T-V-064 [US3] Integrate event publishing into task creation service in backend/src/services/todo_service.py (EVNT-009) - ARTIFACT CREATED
- [x] T-V-065 [US3] Integrate event publishing into task update service in backend/src/services/todo_service.py (EVNT-010) - ARTIFACT CREATED
- [x] T-V-066 [US3] Integrate event publishing into task completion service in backend/src/services/todo_service.py (EVNT-011) - ARTIFACT CREATED
- [x] T-V-067 [US3] Integrate event publishing into recurring task service in backend/src/services/recurring_task_service.py (EVNT-012) - ARTIFACT CREATED
- [x] T-V-068 [US3] Integrate event publishing into reminder service in backend/src/services/reminder_service.py (EVNT-013) - ARTIFACT CREATED
- [x] T-V-069 [US3] Create event handler for TaskCreated in backend/src/events/handlers.py (EVNT-014) - ARTIFACT CREATED
- [x] T-V-070 [US3] Create event handler for TaskUpdated in backend/src/events/handlers.py (EVNT-015) - ARTIFACT CREATED
- [x] T-V-071 [US3] Create event handler for TaskCompleted in backend/src/events/handlers.py (EVNT-016) - ARTIFACT CREATED
- [x] T-V-072 [US3] Create event handler for RecurringTaskCreated in backend/src/events/handlers.py (EVNT-017) - ARTIFACT CREATED
- [x] T-V-073 [US3] Create event handler for ReminderScheduled in backend/src/events/handlers.py (EVNT-018) - ARTIFACT CREATED
- [x] T-V-074 [US3] Create event processor for consuming events in backend/src/events/processor.py (EVNT-019) - ARTIFACT CREATED
- [x] T-V-075 [US3] Implement idempotent event processing logic in backend/src/events/processor.py (EVNT-020) - ARTIFACT CREATED

**Verification for User Story 3**: Complete all acceptance scenarios from spec.md:
1. Given a new task creation event, When the event is published to Kafka via Dapr, Then all interested services receive the event through the pub/sub pattern
2. Given a task update event, When the event is processed, Then all affected services update their state appropriately
3. Given a reminder event at a specific time, When Dapr Job API schedules it, Then the notification is triggered at the specified time
4. Given a service failure, When events are published, Then they are retried or held until the service recovers (resilience)
5. Given high-volume events, When multiple events occur simultaneously, Then they are processed in order without conflicts
6. Given an event consumer, When it processes an event, Then it can replay events if needed for recovery

**Checkpoint**: At this point, User Story 3 should be fully functional - event-driven architecture is in place

---

## Phase 6: User Story 4 - Cloud Deployment Infrastructure (Priority: P4)

**Goal**: Set up robust cloud deployment infrastructure for scalable and reliable operation

**Independent Test**: Deploy the complete application to a local Minikube cluster with Dapr and Kafka, verify all services are running and communicating properly. Set up CI/CD pipeline and verify it can build, test, and deploy.

### Local Deployment Setup (Minikube with Dapr + Kafka)

- [x] T-V-076 [US4] Install Dapr on Minikube cluster via dapr init -k (CLD-001) - ARTIFACT CREATED
- [x] T-V-077 [US4] Install Strimzi Kafka operator on Minikube in kafka namespace (CLD-002) - ARTIFACT CREATED
- [x] T-V-078 [US4] Create Kafka cluster resource in kafka namespace (CLD-003) - ARTIFACT CREATED
- [x] T-V-079 [US4] Create Kafka topics via Strimzi (task-events, reminder-events, recurring-events) (CLD-004) - ARTIFACT CREATED
- [x] T-V-080 [US4] Create PostgreSQL/Neon secret in Kubernetes for Dapr state store (CLD-005) - ARTIFACT CREATED
- [x] T-V-081 [US4] Create application secrets in Kubernetes (DATABASE_URL, SECRET_KEY, OPENAI_API_KEY) (CLD-006) - ARTIFACT CREATED
- [x] T-V-082 [US4] Update Helm chart with Dapr component installations (CLD-007) - ARTIFACT CREATED
- [x] T-V-083 [US4] Update Dockerfiles for Dapr health checks in backend/Dockerfile and frontend/Dockerfile (CLD-008) - ARTIFACT CREATED
- [x] T-V-084 [US4] Create local deployment script for Minikube in scripts/deploy-k8s.sh (CLD-009) - ARTIFACT CREATED

### Cloud Deployment Preparation (Azure AKS)

- [x] T-V-085 [US4] Create AKS cluster Terraform configuration in specs/infra/cloud/aks/cluster.tf (CLD-010) - ARTIFACT CREATED
- [x] T-V-086 [US4] Create AKS network configuration in specs/infra/cloud/aks/network.tf (CLD-011) - ARTIFACT CREATED
- [x] T-V-087 [US4] Create AKS Dapr extension installation script (CLD-012) - ARTIFACT CREATED
- [x] T-V-088 [US4] Create AKS Kafka/Redpanda setup documentation (CLD-013) - ARTIFACT CREATED
- [x] T-V-089 [US4] Create AKS monitoring and logging configuration (CLD-014) - ARTIFACT CREATED
- [x] T-V-090 [US4] Update Helm chart for cloud deployment parameters in specs/infra/helm/todo-chatbot/values-prod.yaml (CLD-015) - ARTIFACT CREATED

### CI/CD Pipeline Setup

- [x] T-V-091 [US4] Create GitHub Actions workflow for build and test in .github/workflows/build-test.yml (CI-001) - ARTIFACT CREATED
- [x] T-V-092 [US4] Create GitHub Actions workflow for local deployment in .github/workflows/deploy-local.yml (CI-002) - ARTIFACT CREATED
- [x] T-V-093 [US4] Create GitHub Actions workflow for cloud deployment in .github/workflows/deploy-cloud.yml (CI-003) - ARTIFACT CREATED
- [x] T-V-094 [US4] Create Docker image build steps in GitHub Actions (CI-004) - ARTIFACT CREATED
- [x] T-V-095 [US4] Create Helm deployment steps in GitHub Actions (CI-005) - ARTIFACT CREATED
- [x] T-V-096 [US4] Create security scanning steps in GitHub Actions (CI-006) - ARTIFACT CREATED
- [x] T-V-097 [US4] Create notification steps for deployment status in GitHub Actions (CI-007) - ARTIFACT CREATED

### Monitoring & Observability

- [x] T-V-098 [US4] Create basic logging configuration documentation in specs/infra/cloud-deployment.md (MON-001) - ARTIFACT CREATED
- [x] T-V-099 [US4] Create distributed tracing setup documentation in specs/infra/cloud-deployment.md (MON-002) - ARTIFACT CREATED
- [x] T-V-100 [US4] Create health check endpoints for Dapr in backend/src/main.py (MON-003) - ARTIFACT CREATED

**Verification for User Story 4**: Complete all acceptance scenarios from spec.md:
1. Given a local Minikube environment, When the deployment is executed, Then all services (frontend, backend, Kafka, Dapr) are properly configured and running
2. Given code changes pushed to repository, When GitHub Actions pipeline runs, Then changes are built, tested, and deployed to the cluster
3. Given a production-like environment, When the application scales under load, Then new pod instances can be created and integrated seamlessly
4. Given system monitoring enabled, When events occur, Then logs and metrics are collected for operational visibility
5. Given a failed deployment, When the CI/CD pipeline detects the failure, Then it rolls back to the previous stable version
6. Given the application running in cloud environment, When resources are managed, Then costs are optimized through auto-scaling

**Checkpoint**: At this point, User Story 4 should be fully functional - complete deployment infrastructure ready

---

## Phase 7: Polish & Verification

**Purpose**: Final verification, testing, and documentation completion

- [x] T-V-101 [P] Write unit tests for new Task model fields in backend/tests/unit/test_models.py (VER-001) - ARTIFACT CREATED
- [x] T-V-102 [P] Write unit tests for new Task service methods in backend/tests/unit/test_services.py (VER-002) - ARTIFACT CREATED
- [x] T-V-103 [P] Write unit tests for recurring task service in backend/tests/unit/test_recurring_service.py (VER-003) - ARTIFACT CREATED
- [x] T-V-104 [P] Write integration tests for event publishing in backend/tests/integration/test_events.py (VER-004) - ARTIFACT CREATED
- [x] T-V-105 [P] Write integration tests for event consumption in backend/tests/integration/test_events.py (VER-005) - ARTIFACT CREATED
- [x] T-V-106 [P] Write E2E tests for intermediate features in frontend/tests/e2e/ (VER-006) - ARTIFACT CREATED
- [x] T-V-107 [P] Write E2E tests for advanced features in frontend/tests/e2e/ (VER-007) - ARTIFACT CREATED
- [x] T-V-108 [P] Write E2E tests for event-driven behavior in backend/tests/e2e/ (VER-008) - ARTIFACT CREATED
- [x] T-V-109 Update quickstart guide with complete event-driven architecture setup in specs/005-advanced-cloud-deployment/quickstart.md (VER-009) - ARTIFACT CREATED
- [x] T-V-110 Update data-model documentation with event schema definitions in specs/005-advanced-cloud-deployment/data-model.md (VER-010) - ARTIFACT CREATED
- [x] T-V-111 Update research documentation with final architecture decisions in specs/005-advanced-cloud-deployment/research.md (VER-011) - ARTIFACT CREATED
- [x] T-V-112 Create deployment troubleshooting guide in specs/infra/cloud-deployment.md (VER-012) - ARTIFACT CREATED

**Final Verification**: All user stories should now be independently functional and the entire event-driven architecture should be operational.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational - intermediate features first
- **User Story 2 (Phase 4)**: Depends on User Story 1 - advanced features build on intermediate
- **User Story 3 (Phase 5)**: Depends on User Story 2 - event-driven architecture wraps features
- **User Story 4 (Phase 6)**: Depends on User Story 3 - deployment wraps complete functionality
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - MVP features
- **User Story 2 (P2)**: Depends on US1 completion - builds on core task functionality
- **User Story 3 (P3)**: Depends on US2 completion - event-driven architecture for existing features
- **User Story 4 (P4)**: Depends on US3 completion - deployment of complete event-driven system

### Within Each User Story

**For US1 (Intermediate Features)**:
1. Update models (T-V-006-T-V-015) - foundation
2. Update APIs (T-V-016-T-V-026) - backend implementation
3. Create frontend components (T-V-027-T-V-035) - UI implementation

**For US2 (Advanced Features)**:
1. Create models (T-V-036-T-V-043) - backend foundations
2. Create frontend components (T-V-044-T-V-049) - UI implementation

**For US3 (Event-Driven Architecture)**:
1. Define event schemas (T-V-050-T-V-058) - contract definitions
2. Set up Dapr components (T-V-058-T-V-063) - infrastructure setup
3. Integrate events (T-V-064-T-V-075) - backend integration

**For US4 (Cloud Deployment)**:
1. Local setup (T-V-076-T-V-084) - Minikube preparation
2. Cloud setup (T-V-085-T-V-090) - AKS preparation
3. CI/CD setup (T-V-091-T-V-097) - automation setup
4. Monitoring (T-V-098-T-V-100) - observability setup

### Parallel Opportunities

```bash
# Phase 2 - Model updates can run in parallel:
T-V-006, T-V-007, T-V-008, T-V-009, T-V-010 [P]

# US1 - API updates can run in parallel:
T-V-016, T-V-017, T-V-018, T-V-019 [P] (creation/updating)
T-V-020, T-V-021, T-V-022, T-V-023 [P] (filtering)
T-V-024, T-V-025, T-V-026 [P] (sorting)

# US1 - Frontend components can run in parallel:
T-V-027, T-V-028, T-V-029 [P] (input components)
T-V-030, T-V-031, T-V-032 [P] (control components)

# US2 - Backend and frontend can run in parallel:
T-V-036-T-V-043 (backend services)
T-V-044-T-V-049 (frontend components)

# US3 - Event schemas can run in parallel:
T-V-050, T-V-051, T-V-052, T-V-053, T-V-054, T-V-055 [P]

# US3 - Dapr components can run in parallel:
T-V-058, T-V-059, T-V-060, T-V-061 [P]

# US4 - Testing can run in parallel:
T-V-101-T-V-108 [P]
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T-V-001-T-V-005)
2. Complete Phase 2: Foundational (T-V-006-T-V-015)
3. Complete Phase 3: User Story 1 (T-V-016-T-V-035)
4. **STOP and VALIDATE**: Users can efficiently organize tasks using priorities and tags, search, filter, and sort
5. This alone provides immediate user value

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Intermediate features work → MVP!
3. Add User Story 2 → Advanced features work → Enhanced functionality
4. Add User Story 3 → Event-driven architecture → Scalable and resilient
5. Add User Story 4 → Cloud deployment → Production ready
6. Each story adds value without breaking previous stories

### Full Deployment Path

After all tasks complete, a developer can:
1. Set up Minikube with Dapr and Kafka
2. Build and deploy the event-driven application with Helm
3. Access the application with all advanced features (priorities, tags, search, recurring tasks, reminders)
4. Verify all events are flowing correctly through the system

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks
- [US1]/[US2]/[US3]/[US4] label maps task to specific user story for traceability
- All infrastructure files go under `specs/infra/` per DIS-013
- Dapr pub/sub abstraction is used instead of direct Kafka client per EVS-006, DAP-001
- Event-driven architecture follows Phase V requirements (EVS-*, DAP-*) per constitution
- Tasks are ordered from foundational → features → events → deployment → CI/CD
- Each task includes specific file paths for clear execution