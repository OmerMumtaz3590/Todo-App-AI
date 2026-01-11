"""
End-to-end API testing script.
Tests all authentication and todo CRUD endpoints.
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def print_test(test_name):
    print(f"\n{'='*60}")
    print(f"TEST: {test_name}")
    print('='*60)

def print_response(response):
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")

def test_health_check():
    print_test("Health Check")
    response = requests.get(f"{BASE_URL}/")
    print_response(response)
    assert response.status_code == 200
    assert "Todo API is running" in response.json()["message"]
    print("✅ Health check passed")

def test_signup():
    print_test("User Signup")
    email = f"test_{int(time.time())}@example.com"
    password = "testpassword123"

    data = {
        "email": email,
        "password": password
    }

    response = requests.post(f"{BASE_URL}/auth/signup", json=data)
    print_response(response)
    assert response.status_code == 201
    assert "user_id" in response.json()
    print("✅ Signup passed")
    return email, password

def test_signin(email, password):
    print_test("User Signin")
    data = {
        "email": email,
        "password": password
    }

    response = requests.post(f"{BASE_URL}/auth/signin", json=data)
    print_response(response)
    assert response.status_code == 200
    assert "user" in response.json()

    # Get session cookie
    cookies = response.cookies
    print(f"Cookies: {dict(cookies)}")
    print("✅ Signin passed")
    return cookies

def test_get_empty_todos(cookies):
    print_test("Get Todos (Empty)")
    response = requests.get(f"{BASE_URL}/todos", cookies=cookies)
    print_response(response)
    assert response.status_code == 200
    assert response.json()["todos"] == []
    print("✅ Get empty todos passed")

def test_create_todo(cookies):
    print_test("Create Todo")
    data = {
        "title": "Test Todo 1",
        "description": "This is a test todo item"
    }

    response = requests.post(f"{BASE_URL}/todos", json=data, cookies=cookies)
    print_response(response)
    assert response.status_code == 201
    assert response.json()["title"] == "Test Todo 1"
    assert response.json()["is_completed"] == False
    print("✅ Create todo passed")
    return response.json()["id"]

def test_get_todos(cookies):
    print_test("Get Todos (With Data)")
    response = requests.get(f"{BASE_URL}/todos", cookies=cookies)
    print_response(response)
    assert response.status_code == 200
    assert len(response.json()["todos"]) > 0
    print("✅ Get todos with data passed")

def test_update_todo(todo_id, cookies):
    print_test("Update Todo")
    data = {
        "title": "Updated Test Todo",
        "description": "This todo has been updated"
    }

    response = requests.put(f"{BASE_URL}/todos/{todo_id}", json=data, cookies=cookies)
    print_response(response)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Test Todo"
    print("✅ Update todo passed")

def test_toggle_completion(todo_id, cookies):
    print_test("Toggle Todo Completion")
    response = requests.patch(f"{BASE_URL}/todos/{todo_id}/toggle", cookies=cookies)
    print_response(response)
    assert response.status_code == 200
    assert response.json()["todo"]["is_completed"] == True
    print("✅ Toggle completion passed")

    # Toggle back
    print("\nToggling back to incomplete...")
    response = requests.patch(f"{BASE_URL}/todos/{todo_id}/toggle", cookies=cookies)
    print_response(response)
    assert response.status_code == 200
    assert response.json()["todo"]["is_completed"] == False
    print("✅ Toggle back passed")

def test_create_multiple_todos(cookies):
    print_test("Create Multiple Todos")
    todos = [
        {"title": "Buy groceries", "description": "Milk, eggs, bread"},
        {"title": "Finish project", "description": None},
        {"title": "Call dentist", "description": "Schedule appointment"}
    ]

    created_ids = []
    for todo in todos:
        response = requests.post(f"{BASE_URL}/todos", json=todo, cookies=cookies)
        assert response.status_code == 201
        created_ids.append(response.json()["id"])
        print(f"Created: {todo['title']}")

    print("✅ Create multiple todos passed")
    return created_ids

def test_delete_todo(todo_id, cookies):
    print_test("Delete Todo")
    response = requests.delete(f"{BASE_URL}/todos/{todo_id}", cookies=cookies)
    print_response(response)
    assert response.status_code == 200
    assert "deleted successfully" in response.json()["message"]

    # Verify it's deleted
    print("\nVerifying todo is deleted...")
    response = requests.get(f"{BASE_URL}/todos", cookies=cookies)
    todos = response.json()["todos"]
    todo_ids = [t["id"] for t in todos]
    assert todo_id not in todo_ids
    print("✅ Delete todo passed")

def test_signout(cookies):
    print_test("User Signout")
    response = requests.post(f"{BASE_URL}/auth/signout", cookies=cookies)
    print_response(response)
    assert response.status_code == 200

    # Verify can't access todos after signout
    print("\nVerifying unauthorized access after signout...")
    response = requests.get(f"{BASE_URL}/todos", cookies=cookies)
    print(f"Status after signout: {response.status_code}")
    assert response.status_code == 401
    print("✅ Signout passed")

def test_invalid_credentials():
    print_test("Invalid Credentials")
    data = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    }

    response = requests.post(f"{BASE_URL}/auth/signin", json=data)
    print_response(response)
    assert response.status_code == 401
    print("✅ Invalid credentials test passed")

def run_all_tests():
    print("\n" + "="*60)
    print("STARTING END-TO-END API TESTS")
    print("="*60)

    try:
        # Test 1: Health check
        test_health_check()

        # Test 2: Signup
        email, password = test_signup()

        # Test 3: Signin
        cookies = test_signin(email, password)

        # Test 4: Get empty todos
        test_get_empty_todos(cookies)

        # Test 5: Create todo
        todo_id = test_create_todo(cookies)

        # Test 6: Get todos with data
        test_get_todos(cookies)

        # Test 7: Update todo
        test_update_todo(todo_id, cookies)

        # Test 8: Toggle completion
        test_toggle_completion(todo_id, cookies)

        # Test 9: Create multiple todos
        more_todo_ids = test_create_multiple_todos(cookies)

        # Test 10: Delete one todo
        test_delete_todo(more_todo_ids[0], cookies)

        # Test 11: Signout
        test_signout(cookies)

        # Test 12: Invalid credentials
        test_invalid_credentials()

        print("\n" + "="*60)
        print("🎉 ALL TESTS PASSED! 🎉")
        print("="*60)
        print("\nSummary:")
        print("✅ Health check")
        print("✅ User signup")
        print("✅ User signin")
        print("✅ Get empty todos")
        print("✅ Create todo")
        print("✅ Get todos")
        print("✅ Update todo")
        print("✅ Toggle completion")
        print("✅ Create multiple todos")
        print("✅ Delete todo")
        print("✅ User signout")
        print("✅ Invalid credentials handling")

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        raise
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        raise

if __name__ == "__main__":
    run_all_tests()
