# TodoMVC Playwright Tests

Automated end-to-end tests for [TodoMVC](https://demo.playwright.dev/todomvc/#/) using **Playwright** with **Python** and **pytest**.

## Test Coverage

| Test | Description |
|------|-------------|
| `test_add_english_todo` | Add a todo item with English text |
| `test_add_non_english_todo` | Add todo items with German, Japanese, Russian, Turkish, and Arabic characters |
| `test_add_todo_with_numbers` | Add todo items containing numbers |
| `test_mark_completed_and_verify_in_completed_view` | Mark a todo as completed and verify it appears in the "Completed" filter |
| `test_delete_todo_removed_from_all_views` | Delete a todo and verify it is gone from All, Active, and Completed views |
| `test_active_filter_shows_only_active` | Verify the "Active" filter shows only uncompleted items |
| `test_completed_filter_shows_only_completed` | Verify the "Completed" filter shows only completed items |

## Prerequisites

- Python 3.10+

## Setup & Run

```bash
# 1. Clone the repository
git clone <repo-url> && cd <repo-name>

# 2. Create a virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Install browser binaries (first time only)
playwright install chromium

# 4. Run the tests
pytest -v
```

### Run in headed mode (see the browser)

```bash
pytest -v --headed
```

### Run on a specific browser

```bash
pytest -v --browser firefox
pytest -v --browser webkit
```

## Reporting

### Allure Report

Tests automatically generate Allure results. To view the report:

```bash
allure serve allure-results
```

On test failure, screenshots and Playwright traces are attached to the report.

### Playwright Trace Viewer

Failed test traces can be viewed with:

```bash
playwright show-trace traces/<test-name>.zip
```

Or drag the `.zip` file into [trace.playwright.dev](https://trace.playwright.dev).

## CI/CD

Tests run automatically on GitHub Actions for every push and pull request to `main`. The workflow:

- Installs Python 3.13 and dependencies
- Installs Chromium with system dependencies
- Runs all tests
- Uploads Allure results as artifacts (always)
- Uploads Playwright traces as artifacts (on failure)

## Project Structure

```
.
├── conftest.py                   # Shared fixtures (page lifecycle, tracing, reporting)
├── pytest.ini                    # Pytest + Playwright configuration
├── requirements.txt              # Python dependencies
├── pages/
│   └── todo_page.py              # Page Object Model for TodoMVC
├── tests/
│   └── todo/
│       ├── test_add_todo.py      # Adding todo items (English, non-English, numbers)
│       ├── test_complete_todo.py # Marking items as completed
│       ├── test_delete_todo.py   # Deleting items
│       └── test_filters.py       # Active / Completed filter views
└── .github/
    └── workflows/
        └── playwright.yml        # GitHub Actions CI pipeline
```
