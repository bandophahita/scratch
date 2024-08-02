#!/usr/bin/env python3

from unittest import mock

class Foo():
    def __init__(self):
        self.stuff = 1

mock_foo = mock.create_autospec(Foo)

def add_attribute(mock_foo):
    mock_foo.new_var = 34
    return mock_foo


new_mock_foo = add_attribute(mock_foo)

assert new_mock_foo.new_var == 34

