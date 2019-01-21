from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import numpy as np


class PlayerBot(Bot):

    def play_round(self):
        if self.round_number == 1:
            yield (pages._1_Intro)
        else: pass
        yield (pages._2_Contribute, {'token_contributed': np.random.randint(1, 21)})
        yield (pages._3_Guess, {'guess_total_token': 99})
        yield (pages._4_Result)
        if self.round_number == Constants.num_rounds:
            yield (pages._5_FinalResult)
        else: pass
