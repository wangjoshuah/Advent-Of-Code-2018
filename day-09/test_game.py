from unittest import TestCase
from .solution import Game


class TestGame(TestCase):
    def test_example(self):
        game = Game(9)
        high_score = game.play_until(25)
        self.assertEqual(high_score, 32)

    def test_case1(self):
        game = Game(13)
        high_score = game.play_until(7999)
        self.assertEqual(high_score, 146373)

    def test_case2(self):
        game = Game(17)
        high_score = game.play_until(1104)
        self.assertEqual(high_score, 2764)

    def test_case3(self):
        game = Game(21)
        high_score = game.play_until(6111)
        self.assertEqual(high_score, 54718)

    def test_case4(self):
        game = Game(30)
        high_score = game.play_until(5807)
        self.assertEqual(high_score, 37305)

