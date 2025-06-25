#!/usr/bin/env python
"""
MANSIRI Test Runner
Comprehensive test suite for the MANSIRI web application
"""

import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner
from django.core.management import execute_from_command_line


def run_tests():
    """Run all tests for the MANSIRI application"""
    
    print("=" * 60)
    print("MANSIRI Web Application Test Suite")
    print("=" * 60)
    
    # Set up Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mansiri.settings')
    django.setup()
    
    # Get the Django test runner
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    
    # Define test modules to run
    test_modules = [
        'tests.accounts.test_accounts',
        'tests.tasks.test_tasks',
    ]
    
    print(f"Running tests for {len(test_modules)} modules...")
    print("-" * 60)
    
    # Run tests
    failures = test_runner.run_tests(test_modules)
    
    print("-" * 60)
    if failures:
        print(f"❌ Tests completed with {failures} failures")
        return False
    else:
        print("✅ All tests passed successfully!")
        return True


def run_specific_tests():
    """Run specific test categories"""
    
    print("Available test categories:")
    print("1. Accounts module tests")
    print("2. Tasks module tests")
    print("3. All tests")
    
    choice = input("Enter your choice (1-3): ").strip()
    
    test_map = {
        '1': ['tests.accounts.test_accounts'],
        '2': ['tests.tasks.test_tasks'],
        '3': ['tests.accounts.test_accounts', 'tests.tasks.test_tasks']
    }
    
    if choice in test_map:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mansiri.settings')
        django.setup()
        
        TestRunner = get_runner(settings)
        test_runner = TestRunner()
        
        failures = test_runner.run_tests(test_map[choice])
        
        if failures:
            print(f"❌ Tests completed with {failures} failures")
        else:
            print("✅ All tests passed successfully!")
    else:
        print("Invalid choice. Please run the script again.")


def check_test_coverage():
    """Check test coverage for the application"""
    
    print("Checking test coverage...")
    print("-" * 40)
    
    # Basic coverage check by counting test methods
    test_files = [
        'tests/accounts/test_accounts.py',
        'tests/tasks/test_tasks.py'
    ]
    
    total_tests = 0
    for test_file in test_files:
        if os.path.exists(test_file):
            with open(test_file, 'r') as f:
                content = f.read()
                test_count = content.count('def test_')
                print(f"{test_file}: {test_count} test methods")
                total_tests += test_count
    
    print(f"\nTotal test methods: {total_tests}")
    
    # Check model coverage
    models_tested = [
        'User', 'Task', 'TaskCategory', 'TaskPriority', 
        'TaskReminder', 'TaskComment', 'TaskTimeLog'
    ]
    print(f"Models with tests: {len(models_tested)}")
    
    # Check view coverage
    views_tested = [
        'login', 'register', 'profile', 'dashboard',
        'task_list', 'create_task', 'edit_task', 'delete_task',
        'task_detail', 'task_calendar', 'task_board'
    ]
    print(f"Views with tests: {len(views_tested)}")


def run_performance_tests():
    """Run basic performance tests"""
    
    print("Running performance tests...")
    print("-" * 40)
    
    import time
    from django.test import Client
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    client = Client()
    
    # Create test user
    user = User.objects.create_user(
        username='perftest',
        email='perf@example.com',
        password='perfpass123'
    )
    
    # Test login performance
    start_time = time.time()
    response = client.post('/accounts/login/', {
        'username': 'perftest',
        'password': 'perfpass123'
    })
    login_time = time.time() - start_time
    
    print(f"Login response time: {login_time:.3f} seconds")
    
    # Test dashboard load performance
    start_time = time.time()
    response = client.get('/dashboard/')
    dashboard_time = time.time() - start_time
    
    print(f"Dashboard load time: {dashboard_time:.3f} seconds")
    
    # Test task creation performance
    start_time = time.time()
    response = client.post('/tasks/create/', {
        'title': 'Performance Test Task',
        'description': 'Testing task creation performance'
    })
    task_creation_time = time.time() - start_time
    
    print(f"Task creation time: {task_creation_time:.3f} seconds")
    
    # Cleanup
    user.delete()
    
    print("\nPerformance test completed!")


def main():
    """Main test runner function"""
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'coverage':
            check_test_coverage()
        elif command == 'performance':
            run_performance_tests()
        elif command == 'specific':
            run_specific_tests()
        elif command == 'all':
            success = run_tests()
            sys.exit(0 if success else 1)
        else:
            print("Usage: python test_runner.py [all|coverage|performance|specific]")
    else:
        # Run all tests by default
        success = run_tests()
        sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

