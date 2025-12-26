import sys
import os

# Add parent directories to path to avoid circular imports when running directly
if __name__ == '__main__':
    # Get the CS50xFP directory (3 levels up from this file)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cs50xfp_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
    if cs50xfp_dir not in sys.path:
        sys.path.insert(0, cs50xfp_dir)

from CS50xFP.utils.socket.builders import gen_msg
from CS50xFP.utils.socket.protocol import MessageTypes, MessageData
from utils.tests.testdata import create_test_user, create_test_scp


# === Test Data Generators ===

def get_valid_auth_request_data() -> MessageData.AuthRequestData:
    return {'user_id': 123, 'password': 'secure_pass'}

def get_valid_auth_failed_data() -> MessageData.AuthFailedData:
    return {'field': 'user_id'}

def get_valid_auth_success_data() -> MessageData.AuthSuccessData:
    mock_user = create_test_user()
    return {'user': mock_user}

def get_valid_access_request_data() -> MessageData.AccessRequestData:
    return {'f_type': 'scp', 'f_id': 173}

def get_valid_access_redacted_data() -> MessageData.AccessRedactedData:
    return {
        'user_clear': 'Level 2',
        'user_hex': '#FF0000',
        'needed_clear': 'Level 4',
        'needed_hex': '#00FF00'
    }

def get_valid_access_expunged_data() -> MessageData.AccessExpungedData:
    return {'f_type': 'scp', 'f_id': 682}

def get_valid_access_granted_data() -> MessageData.AccessGrantedData:
    mock_scp = create_test_scp()
    return {'file': mock_scp}


# === Test Runner Utilities ===

class TestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []

    def assert_equal(self, actual, expected, message=""):
        if actual != expected:
            raise AssertionError(f"{message}\nExpected: {expected}\nActual: {actual}")

    def assert_true(self, condition, message=""):
        if not condition:
            raise AssertionError(f"{message}\nCondition was False")

    def assert_in(self, item, container, message=""):
        if item not in container:
            raise AssertionError(f"{message}\n{item} not in {container}")

    def assert_is_instance(self, obj, cls, message=""):
        if not isinstance(obj, cls):
            raise AssertionError(f"{message}\n{obj} is not instance of {cls}")

    def assert_raises(self, exception_type, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
            raise AssertionError(f"Expected {exception_type.__name__} but no exception was raised")
        except exception_type as e:
            print(f"    ↳ Raised {exception_type.__name__}: {e}")
            pass
        except Exception as e:
            raise AssertionError(f"Expected {exception_type.__name__} but got {type(e).__name__}: {e}")

    def assert_raises_with_message(self, exception_type, message_part, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
            raise AssertionError(f"Expected {exception_type.__name__} but no exception was raised")
        except exception_type as e:
            print(f"    ↳ Raised {exception_type.__name__}: {e}")
            if message_part not in str(e).lower():
                raise AssertionError(f"Expected '{message_part}' in error message, got: {e}")
        except Exception as e:
            raise AssertionError(f"Expected {exception_type.__name__} but got {type(e).__name__}: {e}")

    def run_test(self, test_name, test_func, show_details=True):
        try:
            test_func()
            self.passed += 1
            print(f"✓ {test_name}")
        except Exception as e:
            self.failed += 1
            error_msg = str(e)
            self.errors.append((test_name, error_msg))
            print(f"✗ {test_name}")
            if show_details:
                print(f"  Error: {error_msg}")

    def print_summary(self):
        total = self.passed + self.failed
        print("\n" + "=" * 70)
        print(f"Test Results: {self.passed}/{total} passed")
        if self.failed > 0:
            print(f"\nFailed Tests ({self.failed}):")
            for name, error in self.errors:
                print(f"  - {name}")
                print(f"    {error}")
        print("=" * 70)


# === Success Tests ===

class TestValidMessages:
    """Test successful message generation with valid data"""

    def __init__(self, runner: TestRunner):
        self.runner = runner

    def test_auth_request_message(self):
        data = get_valid_auth_request_data()
        result = gen_msg(MessageTypes.AUTH_REQUEST, data)

        self.runner.assert_equal(result['type'], 'auth_request')
        self.runner.assert_equal(result['data'], data)
        self.runner.assert_equal(result['data']['user_id'], 123)
        self.runner.assert_equal(result['data']['password'], 'secure_pass')

    def test_auth_failed_message(self):
        data = get_valid_auth_failed_data()
        result = gen_msg(MessageTypes.AUTH_FAILED, data)

        self.runner.assert_equal(result['type'], 'auth_failed')
        self.runner.assert_equal(result['data']['field'], 'user_id')

    def test_auth_success_message(self):
        data = get_valid_auth_success_data()
        result = gen_msg(MessageTypes.AUTH_SUCCESS, data)

        self.runner.assert_equal(result['type'], 'auth_success')
        self.runner.assert_in('user', result['data'])

    def test_access_request_message(self):
        data = get_valid_access_request_data()
        result = gen_msg(MessageTypes.ACCESS_REQUEST, data)

        self.runner.assert_equal(result['type'], 'access_request')
        self.runner.assert_equal(result['data']['f_type'], 'scp')
        self.runner.assert_equal(result['data']['f_id'], 173)

    def test_access_redacted_message(self):
        data = get_valid_access_redacted_data()
        result = gen_msg(MessageTypes.ACCESS_REDACTED, data)

        self.runner.assert_equal(result['type'], 'access_redacted')
        self.runner.assert_equal(result['data']['user_clear'], 'Level 2')
        self.runner.assert_equal(result['data']['needed_clear'], 'Level 4')

    def test_access_expunged_message(self):
        data = get_valid_access_expunged_data()
        result = gen_msg(MessageTypes.ACCESS_EXPUNGED, data)

        self.runner.assert_equal(result['type'], 'access_expunged')
        self.runner.assert_equal(result['data']['f_id'], 682)

    def test_access_granted_message(self):
        data = get_valid_access_granted_data()
        result = gen_msg(MessageTypes.ACCESS_GRANTED, data)

        self.runner.assert_equal(result['type'], 'access_granted')
        self.runner.assert_in('file', result['data'])

    def run_all(self):
        self.runner.run_test("test_auth_request_message", self.test_auth_request_message)
        self.runner.run_test("test_auth_failed_message", self.test_auth_failed_message)
        self.runner.run_test("test_auth_success_message", self.test_auth_success_message)
        self.runner.run_test("test_access_request_message", self.test_access_request_message)
        self.runner.run_test("test_access_redacted_message", self.test_access_redacted_message)
        self.runner.run_test("test_access_expunged_message", self.test_access_expunged_message)
        self.runner.run_test("test_access_granted_message", self.test_access_granted_message)


# === Invalid Message Type Tests ===

class TestInvalidMessageType:
    """Test error handling for invalid message types"""

    def __init__(self, runner: TestRunner):
        self.runner = runner

    def test_none_message_type(self):
        data = get_valid_auth_request_data()
        self.runner.assert_raises_with_message(
            TypeError, 'message_type',
            gen_msg, None, data
        )

    def test_string_message_type(self):
        data = get_valid_auth_request_data()
        self.runner.assert_raises_with_message(
            TypeError, 'message_type',
            gen_msg, 'auth_request', data
        )

    def test_int_message_type(self):
        data = get_valid_auth_request_data()
        self.runner.assert_raises_with_message(
            TypeError, 'message_type',
            gen_msg, 123, data
        )

    def run_all(self):
        self.runner.run_test("test_none_message_type", self.test_none_message_type)
        self.runner.run_test("test_string_message_type", self.test_string_message_type)
        self.runner.run_test("test_int_message_type", self.test_int_message_type)


# === Invalid Data Tests ===

class TestInvalidDataType:
    """Test error handling for invalid data types"""

    def __init__(self, runner: TestRunner):
        self.runner = runner

    def test_none_data(self):
        self.runner.assert_raises(TypeError, gen_msg, MessageTypes.AUTH_REQUEST, None)

    def test_string_data(self):
        self.runner.assert_raises(TypeError, gen_msg, MessageTypes.AUTH_REQUEST, "not a dict")

    def test_list_data(self):
        self.runner.assert_raises(TypeError, gen_msg, MessageTypes.AUTH_REQUEST, [1, 2, 3])

    def test_int_data(self):
        self.runner.assert_raises(TypeError, gen_msg, MessageTypes.AUTH_REQUEST, 123)

    def run_all(self):
        self.runner.run_test("test_none_data", self.test_none_data)
        self.runner.run_test("test_string_data", self.test_string_data)
        self.runner.run_test("test_list_data", self.test_list_data)
        self.runner.run_test("test_int_data", self.test_int_data)


# === Missing Keys Tests ===

class TestMissingKeys:
    """Test error handling for missing required keys"""

    def __init__(self, runner: TestRunner):
        self.runner = runner

    def test_auth_request_missing_user_id(self):
        self.runner.assert_raises_with_message(
            ValueError, 'user_id',
            gen_msg, MessageTypes.AUTH_REQUEST, {'password': 'test'}
        )

    def test_auth_request_missing_password(self):
        self.runner.assert_raises_with_message(
            ValueError, 'password',
            gen_msg, MessageTypes.AUTH_REQUEST, {'user_id': 123}
        )

    def test_access_request_missing_f_type(self):
        self.runner.assert_raises_with_message(
            ValueError, 'f_type',
            gen_msg, MessageTypes.ACCESS_REQUEST, {'f_id': 173}
        )

    def test_access_redacted_missing_multiple_keys(self):
        self.runner.assert_raises(
            ValueError,
            gen_msg, MessageTypes.ACCESS_REDACTED, {'user_clear': 'Level 2'}
        )

    def run_all(self):
        self.runner.run_test("test_auth_request_missing_user_id", self.test_auth_request_missing_user_id)
        self.runner.run_test("test_auth_request_missing_password", self.test_auth_request_missing_password)
        self.runner.run_test("test_access_request_missing_f_type", self.test_access_request_missing_f_type)
        self.runner.run_test("test_access_redacted_missing_multiple_keys", self.test_access_redacted_missing_multiple_keys)


# === Extra Keys Tests ===

class TestExtraKeys:
    """Test error handling for unexpected extra keys"""

    def __init__(self, runner: TestRunner):
        self.runner = runner

    def test_auth_request_extra_key(self):
        self.runner.assert_raises_with_message(
            ValueError, 'extra',
            gen_msg, MessageTypes.AUTH_REQUEST,
            {'user_id': 123, 'password': 'test', 'extra': 'field'}
        )

    def test_access_request_extra_keys(self):
        self.runner.assert_raises(
            ValueError,
            gen_msg, MessageTypes.ACCESS_REQUEST,
            {'f_type': 'scp', 'f_id': 173, 'bonus': 'data', 'more': 'stuff'}
        )

    def run_all(self):
        self.runner.run_test("test_auth_request_extra_key", self.test_auth_request_extra_key)
        self.runner.run_test("test_access_request_extra_keys", self.test_access_request_extra_keys)


# === Wrong Type Tests ===

class TestWrongValueTypes:
    """Test error handling for wrong value types"""

    def __init__(self, runner: TestRunner):
        self.runner = runner

    def test_auth_request_string_user_id(self):
        self.runner.assert_raises_with_message(
            TypeError, 'user_id',
            gen_msg, MessageTypes.AUTH_REQUEST,
            {'user_id': 'not_an_int', 'password': 'test'}
        )

    def test_auth_request_int_password(self):
        self.runner.assert_raises_with_message(
            TypeError, 'password',
            gen_msg, MessageTypes.AUTH_REQUEST,
            {'user_id': 123, 'password': 12345}
        )

    def test_access_request_int_f_type(self):
        self.runner.assert_raises_with_message(
            TypeError, 'f_type',
            gen_msg, MessageTypes.ACCESS_REQUEST,
            {'f_type': 123, 'f_id': 173}
        )

    def test_access_request_string_f_id(self):
        self.runner.assert_raises_with_message(
            TypeError, 'f_id',
            gen_msg, MessageTypes.ACCESS_REQUEST,
            {'f_type': 'scp', 'f_id': '173'}
        )

    def run_all(self):
        self.runner.run_test("test_auth_request_string_user_id", self.test_auth_request_string_user_id)
        self.runner.run_test("test_auth_request_int_password", self.test_auth_request_int_password)
        self.runner.run_test("test_access_request_int_f_type", self.test_access_request_int_f_type)
        self.runner.run_test("test_access_request_string_f_id", self.test_access_request_string_f_id)


# === Empty Data Tests ===

class TestEmptyData:
    """Test error handling for empty dictionaries"""

    def __init__(self, runner: TestRunner):
        self.runner = runner

    def test_empty_dict(self):
        self.runner.assert_raises(ValueError, gen_msg, MessageTypes.AUTH_REQUEST, {})

    def run_all(self):
        self.runner.run_test("test_empty_dict", self.test_empty_dict)


# === Non-String Keys Tests ===

class TestNonStringKeys:
    """Test error handling for non-string dictionary keys"""

    def __init__(self, runner: TestRunner):
        self.runner = runner

    def test_int_keys(self):
        self.runner.assert_raises_with_message(
            TypeError, 'key',
            gen_msg, MessageTypes.AUTH_REQUEST,
            {1: 123, 2: 'password'}
        )

    def test_mixed_keys(self):
        self.runner.assert_raises(
            TypeError,
            gen_msg, MessageTypes.AUTH_REQUEST,
            {'user_id': 123, 2: 'password'}
        )

    def run_all(self):
        self.runner.run_test("test_int_keys", self.test_int_keys)
        self.runner.run_test("test_mixed_keys", self.test_mixed_keys)


# === Edge Cases ===

class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    def __init__(self, runner: TestRunner):
        self.runner = runner

    def test_zero_user_id(self):
        result = gen_msg(
            MessageTypes.AUTH_REQUEST,
            {'user_id': 0, 'password': 'test'}
        )
        self.runner.assert_equal(result['data']['user_id'], 0)

    def test_negative_f_id(self):
        result = gen_msg(
            MessageTypes.ACCESS_REQUEST,
            {'f_type': 'scp', 'f_id': -1}
        )
        self.runner.assert_equal(result['data']['f_id'], -1)

    def test_empty_string_password(self):
        result = gen_msg(
            MessageTypes.AUTH_REQUEST,
            {'user_id': 123, 'password': ''}
        )
        self.runner.assert_equal(result['data']['password'], '')

    def test_empty_string_field(self):
        result = gen_msg(
            MessageTypes.AUTH_FAILED,
            {'field': ''}
        )
        self.runner.assert_equal(result['data']['field'], '')

    def test_unicode_in_strings(self):
        result = gen_msg(
            MessageTypes.AUTH_REQUEST,
            {'user_id': 123, 'password': '密码🔒'}
        )
        self.runner.assert_equal(result['data']['password'], '密码🔒')

    def run_all(self):
        self.runner.run_test("test_zero_user_id", self.test_zero_user_id)
        self.runner.run_test("test_negative_f_id", self.test_negative_f_id)
        self.runner.run_test("test_empty_string_password", self.test_empty_string_password)
        self.runner.run_test("test_empty_string_field", self.test_empty_string_field)
        self.runner.run_test("test_unicode_in_strings", self.test_unicode_in_strings)


# === Return Type Tests ===

class TestReturnTypes:
    """Test that return values have correct structure"""

    def __init__(self, runner: TestRunner):
        self.runner = runner

    def test_returns_dict(self):
        data = get_valid_auth_request_data()
        result = gen_msg(MessageTypes.AUTH_REQUEST, data)
        self.runner.assert_is_instance(result, dict)

    def test_has_type_key(self):
        data = get_valid_auth_request_data()
        result = gen_msg(MessageTypes.AUTH_REQUEST, data)
        self.runner.assert_in('type', result)

    def test_has_data_key(self):
        data = get_valid_auth_request_data()
        result = gen_msg(MessageTypes.AUTH_REQUEST, data)
        self.runner.assert_in('data', result)

    def test_type_is_string(self):
        data = get_valid_auth_request_data()
        result = gen_msg(MessageTypes.AUTH_REQUEST, data)
        self.runner.assert_is_instance(result['type'], str)

    def test_data_is_dict(self):
        data = get_valid_auth_request_data()
        result = gen_msg(MessageTypes.AUTH_REQUEST, data)
        self.runner.assert_is_instance(result['data'], dict)

    def run_all(self):
        self.runner.run_test("test_returns_dict", self.test_returns_dict)
        self.runner.run_test("test_has_type_key", self.test_has_type_key)
        self.runner.run_test("test_has_data_key", self.test_has_data_key)
        self.runner.run_test("test_type_is_string", self.test_type_is_string)
        self.runner.run_test("test_data_is_dict", self.test_data_is_dict)


# === Main Test Runner ===

def run_all_tests():
    """Run all test suites and print results"""
    print("=" * 70)
    print("Running Message Generator Tests")
    print("=" * 70)
    print("\nThis will run all tests and show error messages.")
    print("Press Enter after each section to continue...\n")

    runner = TestRunner()

    # print("\n" + "=" * 70)
    # print("--- Valid Messages Tests ---")
    # print("=" * 70)
    # TestValidMessages(runner).run_all()
    # input("\nPress Enter to continue to next section...")

    # print("\n" + "=" * 70)
    # print("--- Invalid Message Type Tests ---")
    # print("=" * 70)
    # TestInvalidMessageType(runner).run_all()
    # input("\nPress Enter to continue to next section...")

    print("\n" + "=" * 70)
    print("--- Invalid Data Type Tests ---")
    print("=" * 70)
    TestInvalidDataType(runner).run_all()
    input("\nPress Enter to continue to next section...")

    print("\n" + "=" * 70)
    print("--- Missing Keys Tests ---")
    print("=" * 70)
    TestMissingKeys(runner).run_all()
    input("\nPress Enter to continue to next section...")

    print("\n" + "=" * 70)
    print("--- Extra Keys Tests ---")
    print("=" * 70)
    TestExtraKeys(runner).run_all()
    input("\nPress Enter to continue to next section...")

    print("\n" + "=" * 70)
    print("--- Wrong Value Types Tests ---")
    print("=" * 70)
    TestWrongValueTypes(runner).run_all()
    input("\nPress Enter to continue to next section...")

    print("\n" + "=" * 70)
    print("--- Empty Data Tests ---")
    print("=" * 70)
    TestEmptyData(runner).run_all()
    input("\nPress Enter to continue to next section...")

    print("\n" + "=" * 70)
    print("--- Non-String Keys Tests ---")
    print("=" * 70)
    TestNonStringKeys(runner).run_all()
    input("\nPress Enter to continue to next section...")

    print("\n" + "=" * 70)
    print("--- Edge Cases Tests ---")
    print("=" * 70)
    TestEdgeCases(runner).run_all()
    input("\nPress Enter to continue to next section...")

    print("\n" + "=" * 70)
    print("--- Return Type Tests ---")
    print("=" * 70)
    TestReturnTypes(runner).run_all()

    runner.print_summary()

    return runner.failed == 0


if __name__ == '__main__':
    import sys
    success = run_all_tests()
    sys.exit(0 if success else 1)
