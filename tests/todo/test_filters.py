import allure
import pytest
from playwright.sync_api import expect

from pages.todo_page import TodoPage


@allure.feature("Filters")
class TestFilters:
    @pytest.fixture(autouse=True)
    def _setup_items(self, todo_page: TodoPage):
        """Create two items and complete one before each filter test."""
        todo_page.add_todo("Active task")
        todo_page.add_todo("Done task")
        todo_page.toggle_todo_by_text("Done task")

    def test_active_filter_shows_only_active(self, todo_page: TodoPage):
        todo_page.filter_active()
        expect(todo_page.todo_items).to_have_count(1)
        expect(todo_page.nth_item(0)).to_have_text("Active task")

    def test_completed_filter_shows_only_completed(self, todo_page: TodoPage):
        todo_page.filter_completed()
        expect(todo_page.todo_items).to_have_count(1)
        expect(todo_page.nth_item(0)).to_have_text("Done task")
