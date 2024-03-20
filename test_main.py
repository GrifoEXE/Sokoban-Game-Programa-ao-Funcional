from main import is_valid, is_goal, is_box, is_free, move

def test_is_valid():
    level = [
        ['#', '#', '#', '#', '#'],
        ['#', ' ', ' ', ' ', '#'],
        ['#', ' ', '$', ' ', '#'],
        ['#', '#', '#', '#', '#'],
    ]

    assert is_valid((1, 1), level).success == True
    assert is_valid((1, 4), level).success == False
    assert is_valid((2, 2), level).success == True
    assert is_valid((2, -1), level).success == False
    assert is_valid((4, 0), level).success == False

def test_is_goal():
    level = [
        ['#', '#', '#', '#', '#'],
        ['#', ' ', ' ', ' ', '#'],
        ['#', ' ', '$', '.', '#'],
        ['#', '#', '#', '#', '#'],
    ]

    is_goal_func = is_goal(level)
    assert is_goal_func((1, 1)) == False
    assert is_goal_func((3, 3)) == True
    assert is_goal_func((2, 2)) == False
    assert is_goal_func((1, 4)) == False

def test_is_box():
    level = [
        ['#', '#', '#', '#', '#'],
        ['#', ' ', ' ', ' ', '#'],
        ['#', ' ', '$', '.', '#'],
        ['#', '#', '#', '#', '#'],
    ]

    is_box_func = is_box(level)
    assert is_box_func((1, 1)) == False
    assert is_box_func((2, 2)) == True
    assert is_box_func((3, 3)) == False
    assert is_box_func((1, 4)) == False

def test_is_free():
    level = [
        ['#', '#', '#', '#', '#'],
        ['#', ' ', ' ', ' ', '#'],
        ['#', ' ', '$', '.', '#'],
        ['#', '#', '#', '#', '#'],
    ]

    is_free_func = is_free(level)
    assert is_free_func((1, 1)) == True
    assert is_free_func((2, 2)) == False
    assert is_free_func((3, 3)) == False
    assert is_free_func((1, 4)) == False

def test_move():
    assert move((1, 1), (0, 1)) == (1, 2)
    assert move((2, 2), (-1, 0)) == (1, 2)
    assert move((3, 3), (0, -1)) == (3, 2)
