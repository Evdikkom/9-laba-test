import pytest
import requests
import sys
import random
import string

BASE_URL = "https://jsonplaceholder.typicode.com"

class TestJSONPlaceholderAPI:
    """Тесты для API jsonplaceholder.typicode.com с использованием pytest и requests"""
    
    def _print_result(self, message, status="INFO"):
        """Вывод результата в stderr"""
        print(f"\n{status}: {message}", file=sys.stderr)
        sys.stderr.flush()
    
    def generate_random_name(self):
        """Генерация случайного имени для тестов"""
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(8))
    
    @pytest.fixture
    def api_headers(self):
        """Фикстура с заголовками для API запросов"""
        self._print_result("Подготавливаем заголовки для API запросов")
        return {
            "Content-Type": "application/json"
            # JSONPlaceholder не требует API ключа!
        }

    def test_get_user(self, api_headers):
        """Тест GET запроса для получения пользователя"""
        self._print_result("Выполняем GET запрос для получения пользователя")
        response = requests.get(f"{BASE_URL}/users/1", headers=api_headers)
        
        # Проверка статус-кода
        assert response.status_code == 200
        self._print_result(f"Статус-код: {response.status_code} - OK", "SUCCESS")
        
        # Проверка структуры JSON
        json_data = response.json()
        expected_keys = ["id", "name", "username", "email", "address", "phone", "website", "company"]
        assert all(key in json_data for key in expected_keys)
        self._print_result("Структура JSON ответа корректна", "SUCCESS")
        
        # Проверка значений полей
        assert json_data["id"] == 1
        assert json_data["name"] == "Leanne Graham"
        self._print_result("Значения полей соответствуют ожидаемым", "SUCCESS")
        
        self._print_result("GET тест пройден успешно", "SUCCESS")

    def test_create_user(self, api_headers):
        """Тест POST запроса для создания пользователя"""
        self._print_result("Выполняем POST запрос для создания пользователя")
        
        random_name = self.generate_random_name()
        payload = {
            "name": f"Test User {random_name}",
            "username": f"testuser_{random_name}",
            "email": f"test{random_name}@example.com",
            "phone": "1-770-736-8031 x56442",
            "website": f"{random_name}.org"
        }
        
        response = requests.post(f"{BASE_URL}/users", json=payload, headers=api_headers)
        
        # Проверка статус-кода
        assert response.status_code == 201
        self._print_result(f"Статус-код: {response.status_code} - Created", "SUCCESS")
        
        # Проверка структуры JSON
        json_data = response.json()
        assert "id" in json_data  # JSONPlaceholder возвращает созданный ID
        self._print_result("Структура JSON ответа корректна", "SUCCESS")
        
        # Проверка значений полей (JSONPlaceholder возвращает отправленные данные + ID)
        assert json_data["name"] == payload["name"]
        assert json_data["username"] == payload["username"]
        self._print_result("Значения полей соответствуют ожидаемым", "SUCCESS")
        
        self._print_result("POST тест пройден успешно", "SUCCESS")

    def test_update_user(self, api_headers):
        """Тест PUT запроса для обновления пользователя"""
        self._print_result("Выполняем PUT запрос для обновления пользователя")
        
        random_name = self.generate_random_name()
        payload = {
            "name": f"Updated User {random_name}",
            "username": f"updated_{random_name}",
            "email": f"updated{random_name}@example.com"
        }
        
        response = requests.put(f"{BASE_URL}/users/1", json=payload, headers=api_headers)
        
        # Проверка статус-кода
        assert response.status_code == 200
        self._print_result(f"Статус-код: {response.status_code} - OK", "SUCCESS")
        
        # Проверка структуры JSON
        json_data = response.json()
        assert all(key in json_data for key in ["name", "username", "email", "id"])
        self._print_result("Структура JSON ответа корректна", "SUCCESS")
        
        # Проверка значений полей
        assert json_data["name"] == payload["name"]
        assert json_data["username"] == payload["username"]
        self._print_result("Значения полей соответствуют ожидаемым", "SUCCESS")
        
        self._print_result("PUT тест пройден успешно", "SUCCESS")
        
    def test_delete_user(self, api_headers):
        """Тест DELETE запроса для удаления пользователя"""
        self._print_result("Выполняем DELETE запрос для удаления пользователя")
        
        response = requests.delete(f"{BASE_URL}/users/1", headers=api_headers)
        
        # Проверка статус-кода
        assert response.status_code == 200
        self._print_result(f"Статус-код: {response.status_code} - OK", "SUCCESS")
        
        self._print_result("DELETE тест пройден успешно", "SUCCESS")

if __name__ == "__main__":
    # Запуск pytest с аргументами
    pytest.main([__file__, "-v", "-s"])
