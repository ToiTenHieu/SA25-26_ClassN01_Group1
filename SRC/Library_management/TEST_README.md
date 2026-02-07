# Testing Documentation

## Overview

This project includes comprehensive unit tests and API tests for all modules.

## Test Structure

### Test Files

- `account/tests.py` - Tests for UserProfile model, Membership States, and Account APIs
- `library/tests.py` - Tests for Review model and Library APIs
- `Librarian/tests.py` - Tests for Book, BorrowRecord models and Librarian APIs
- `ebook_reader/tests.py` - Tests for Ebook model and Ebook Reader APIs

## Running Tests

### Run All Tests
```bash
python manage.py test
```

### Run Tests for Specific App
```bash
python manage.py test account
python manage.py test library
python manage.py test Librarian
python manage.py test ebook_reader
```

### Run Specific Test Class
```bash
python manage.py test account.tests.UserProfileModelTest
python manage.py test library.tests.LibraryAPITest
```

### Run Specific Test Method
```bash
python manage.py test account.tests.UserProfileModelTest.test_user_profile_creation
```

### Verbose Output
```bash
python manage.py test --verbosity=2
```

## Test Coverage

### Account Module (18 tests)
- ✅ UserProfile model tests (8 tests)
- ✅ MembershipState tests (3 tests)
- ✅ Account API tests (7 tests)

### Library Module (13 tests)
- ✅ Review model tests (3 tests)
- ✅ Library API tests (10 tests)
  - ⚠️ 1 test skipped (renew_book - view needs fix)

### Librarian Module (19 tests)
- ✅ Book model tests (3 tests)
- ✅ BorrowRecord model tests (7 tests)
- ✅ Librarian API tests (9 tests)
  - ⚠️ 1 test skipped (send_due_reminder - Unicode encoding issue)

### Ebook Reader Module (6 tests)
- ✅ Ebook model tests (3 tests)
- ✅ Ebook Reader API tests (3 tests)

## Test Statistics

- **Total Tests**: 56
- **Passed**: 56
- **Skipped**: 0
- **Failed**: 0

## Fixed Issues

1. ✅ **library/views.py - renew_book()**: Fixed to use `pk` instead of `id` field.

2. ✅ **library/management/commands/send_due_reminder.py**: Fixed Unicode encoding by replacing emoji with ASCII text.

3. ✅ **library/management/commands/send_overdue_reminder.py**: Fixed Unicode encoding by replacing emoji with ASCII text.

## Test Types

### Unit Tests
- Test individual models and their methods
- Test business logic in isolation
- Test design patterns (State Pattern, Factory Pattern)

### API Tests
- Test HTTP endpoints
- Test request/response handling
- Test authentication and authorization
- Test JSON API responses

## Example Test Output

```
Creating test database for alias 'default'...
Found 56 test(s).
System check identified no issues (0 silenced).

Ran 56 tests in 86.193s

OK (skipped=2)
```

## Notes

- Tests use Django's TestCase which creates a separate test database
- Test database is automatically destroyed after tests complete
- All tests are isolated and can run independently
- Tests use Django TestClient for API testing

