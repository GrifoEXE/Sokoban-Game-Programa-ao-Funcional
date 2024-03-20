import unittest
import keyboard
import asyncio
from main import move

class TestMovement(unittest.TestCase):
    def test_move_up(self):
        pos = (1, 1)
        delta = (-1, 0)
        new_pos = move(pos, delta)
        self.assertEqual(new_pos, (0, 1))

    def test_move_down(self):
        pos = (1, 1)
        delta = (1, 0)
        new_pos = move(pos, delta)
        self.assertEqual(new_pos, (2, 1))

    def test_move_left(self):
        pos = (1, 1)
        delta = (0, -1)
        new_pos = move(pos, delta)
        self.assertEqual(new_pos, (1, 0))

    def test_move_right(self):
        pos = (1, 1)
        delta = (0, 1)
        new_pos = move(pos, delta)
        self.assertEqual(new_pos, (1, 2))

if __name__ == '__main__':
    unittest.main()

