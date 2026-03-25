import allure
from playwright.sync_api import Page, Locator


class TodoPage:
    PATH = "/todomvc/#/"

    def __init__(self, page: Page):
        self.page = page
        self.new_todo_input = page.get_by_role("textbox", name="What needs to be done?")
        self.todo_items = page.locator(".todo-list").get_by_role("listitem")
        self.all_link = page.get_by_role("link", name="All")
        self.active_link = page.get_by_role("link", name="Active")
        self.completed_link = page.get_by_role("link", name="Completed")
        self.clear_completed_button = page.get_by_role("button", name="Clear completed")
        self.todo_count = page.get_by_test_id("todo-count")

    @allure.step("Navigate to TodoMVC app")
    def goto(self) -> None:
        self.page.goto(self.PATH)
        self.new_todo_input.wait_for()

    @allure.step('Add todo: "{text}"')
    def add_todo(self, text: str) -> None:
        self.new_todo_input.click()
        self.new_todo_input.fill(text)
        self.new_todo_input.press("Enter")

    @allure.step('Mark "{text}" as completed')
    def toggle_todo_by_text(self, text: str) -> None:
        self.todo_items.filter(has_text=text).get_by_label("Toggle Todo").check()

    @allure.step('Unmark "{text}" as completed')
    def untoggle_todo_by_text(self, text: str) -> None:
        self.todo_items.filter(has_text=text).get_by_label("Toggle Todo").uncheck()

    @allure.step('Delete todo: "{text}"')
    def delete_todo_by_text(self, text: str) -> None:
        self.todo_items.filter(has_text=text).hover()
        self.todo_items.filter(has_text=text).get_by_role("button", name="Delete").click()

    @allure.step("Clear completed todos")
    def clear_completed(self) -> None:
        self.clear_completed_button.click()

    @allure.step('Filter by "All"')
    def filter_all(self) -> None:
        self.all_link.click()

    @allure.step('Filter by "Active"')
    def filter_active(self) -> None:
        self.active_link.click()

    @allure.step('Filter by "Completed"')
    def filter_completed(self) -> None:
        self.completed_link.click()

    @allure.step("Clear all todos")
    def clear_todos(self) -> None:
        """Remove all todo items via the UI by deleting each one."""
        if self.todo_items.count() == 0:
            return
        if self.all_link.is_visible():
            self.all_link.click()
        while self.todo_items.count() > 0:
            self.todo_items.first.hover()
            self.todo_items.first.get_by_role("button", name="Delete").click()

    def nth_item(self, index: int) -> Locator:
        return self.todo_items.nth(index)
