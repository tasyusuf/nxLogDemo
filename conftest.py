import allure
import pytest
from playwright.sync_api import BrowserContext, Page

from pages.todo_page import TodoPage


@pytest.fixture(scope="module")
def module_context(browser, base_url) -> BrowserContext:
    """A single browser context shared across all tests in a module."""
    context = browser.new_context(base_url=base_url)
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield context
    context.tracing.stop()
    context.close()


@pytest.fixture(scope="module")
def module_page(module_context: BrowserContext) -> Page:
    """A single page shared across all tests in a module."""
    page = module_context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="module")
def todo_page(module_page: Page) -> TodoPage:
    """Navigate to the app once per module, reused across tests."""
    tp = TodoPage(module_page)
    tp.goto()
    return tp


@pytest.fixture(autouse=True)
def _clean_todos(todo_page: TodoPage):
    """Clear all todos before each test to ensure a clean state."""
    todo_page.clear_todos()


@pytest.fixture(autouse=True)
def _attach_trace_on_failure(request, module_context: BrowserContext):
    """Attach a Playwright trace to the Allure report on test failure."""
    yield
    if request.node.rep_call and request.node.rep_call.failed:
        trace_path = f"traces/{request.node.name}.zip"
        module_context.tracing.stop(path=trace_path)
        allure.attach.file(trace_path, name="trace", extension="zip")
        # Restart tracing for the next test.
        module_context.tracing.start(screenshots=True, snapshots=True, sources=True)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Store test result on the request node so fixtures can access it."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(autouse=True)
def _attach_screenshot_on_failure(request, module_page: Page):
    """Attach a screenshot to the Allure report on test failure."""
    yield
    if request.node.rep_call and request.node.rep_call.failed:
        allure.attach(
            module_page.screenshot(),
            name="screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
