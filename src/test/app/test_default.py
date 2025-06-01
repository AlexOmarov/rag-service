"""
Example of pytest tests
"""


def _setup():
    print("basic setup into module")


def _teardown():
    print("basic teardown into module")


def _setup_module(module):
    print("module setup " + module)


def _teardown_module(module):
    print("module teardown " + module)


def _setup_function(function):
    print("function setup " + function)


def _teardown_function(function):
    print("function teardown " + function)


def test_numbers_3_4():
    """
    Assert simple int multiply
    """
    assert 3 * 4 == 12


def test_strings_a_3():
    """
    Assert string/int multiply
    """
    assert 'a' * 3 == 'aaa'
