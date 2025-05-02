"""demonstrating that updating the fixture value does not work beyond the function"""


def test_1(session_fixture, function_fixture):
    assert session_fixture.val == "hello dolly"
    assert function_fixture.val == 5

    session_fixture.val = "hello world"
    function_fixture.val = 8


def test_2(session_fixture, function_fixture):
    assert session_fixture.val == "hello dolly"
    assert function_fixture.val == 5
