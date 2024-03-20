import unittest
import keyboard
import asyncio
from main import is_valid

class TestCollision(unittest.TestCase):
    def test_out_of_bounds(self):
        pos = (-1, 1)
        level = [['#', ' ', '#'],
                 ['#', ' ', '#']]
        result = is_valid(pos, level)
        self.assertFalse(result.success)
        self.assertEqual(result.error, 'Out of bounds')

    def test_wall_collision(self):
        pos = (0, 0)
        level = [['#', ' ', '#'],
                 ['#', ' ', '#']]
        result = is_valid(pos, level)
        self.assertFalse(result.success)

if __name__ == '__main__':
    unittest.main()
