import allure
from playwright.sync_api import expect

from pages.todo_page import TodoPage


@allure.feature("Delete Todo")
class TestDeleteTodo:
    def test_delete_todo_removed_from_all_views(self, todo_page: TodoPage):
        todo_page.add_todo("Temporary task")
        todo_page.add_todo("Keeper task")
        expect(todo_page.todo_items).to_have_count(2)
        expect(todo_page.todo_count).to_have_text("2 items left")

        todo_page.delete_todo_by_text("Temporary task")

        # "All" view
        expect(todo_page.todo_items).to_have_count(1)
        expect(todo_page.nth_item(0)).to_have_text("Keeper task")
        expect(todo_page.todo_count).to_have_text("1 item left")

        # "Active" view
        todo_page.filter_active()
        expect(todo_page.todo_items).to_have_count(1)
        expect(todo_page.nth_item(0)).to_have_text("Keeper task")

        # "Completed" view
        todo_page.filter_completed()
        expect(todo_page.todo_items).to_have_count(0)
