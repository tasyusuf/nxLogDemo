import allure
from playwright.sync_api import expect

from pages.todo_page import TodoPage


@allure.feature("Complete Todo")
class TestCompleteTodo:
    def test_mark_completed_and_verify_in_completed_view(self, todo_page: TodoPage):
        todo_page.add_todo("Finish report")

        todo_page.toggle_todo_by_text("Finish report")
        expect(todo_page.todo_items.filter(has_text="Finish report")).to_have_class(["completed"])

        todo_page.filter_completed()
        expect(todo_page.todo_items).to_have_count(1)
        expect(todo_page.nth_item(0)).to_have_text("Finish report")
