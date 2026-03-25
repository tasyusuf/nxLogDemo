import allure
import pytest
from playwright.sync_api import expect

from pages.todo_page import TodoPage


@allure.feature("Add Todo")
class TestAddTodo:
    def test_add_english_todo(self, todo_page: TodoPage):
        todo_page.add_todo("Buy groceries")
        expect(todo_page.todo_items).to_have_count(1)
        expect(todo_page.nth_item(0)).to_have_text("Buy groceries")

    @pytest.mark.parametrize("text", [
        pytest.param("Einkaufen gehen", id="german"),
        pytest.param("日本語のタスク", id="japanese"),
        pytest.param("Задача на русском", id="russian"),
        pytest.param("Görev tamamla", id="turkish"),
        pytest.param("مهمة جديدة", id="arabic"),
    ])
    def test_add_non_english_todo(self, todo_page: TodoPage, text: str):
        todo_page.add_todo(text)
        expect(todo_page.todo_items).to_have_count(1)
        expect(todo_page.nth_item(0)).to_have_text(text)

    @pytest.mark.parametrize("text", [
        pytest.param("Task 123", id="mixed-text-and-numbers"),
        pytest.param("456", id="numbers-only"),
        pytest.param("Buy 2 eggs & 3 bananas", id="numbers-in-sentence"),
    ])
    def test_add_todo_with_numbers(self, todo_page: TodoPage, text: str):
        todo_page.add_todo(text)
        expect(todo_page.todo_items).to_have_count(1)
        expect(todo_page.nth_item(0)).to_have_text(text)
