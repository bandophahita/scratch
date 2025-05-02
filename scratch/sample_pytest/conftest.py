import pytest


class MyObj1:
    val = 5


class MyObj2:
    val = "hello dolly"


@pytest.fixture(scope="function")
def function_fixture():
    return MyObj1()


@pytest.fixture(scope="session")
def session_fixture():
    return MyObj2()
