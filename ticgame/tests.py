from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Game

class Game_tests(TestCase):

    def test_get_classic_nothing(self):
        tstExample = Game(game="0128")
        self.assertIs(tstExample.check_for_win(),"n")
    def test_get_classic_x_win(self):
        tstExample = Game(game="01326")
        self.assertIs(tstExample.check_for_win(),"x")
    def test_get_classic_o_win(self):
        tstExample = Game(game="012437")
        self.assertIs(tstExample.check_for_win(),"o")
    def test_get_classic_zero(self):
        tstExample = Game(game="012345678")
        self.assertIs(tstExample.check_for_win(),"z")