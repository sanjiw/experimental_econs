from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants

class PlayerBot(Bot):
    def play_round(self):
        if self.round_number == Constants.num_training_rounds + 1:
            yield pages.WarningPage
        if self.round_number==1:
            yield pages.Instruction
        yield pages.Mpl, dict(a1=5, a2=4, a3=3, a4=2, a5=3, a6=9, a7=7, a8=15, a9=12, a10=12, a11=1,
                              b1=15, b2=3, b3=9, b4=1, b5=5, b6=10, b7=1, b8=5, b9=13, b10=5, b11=14)
        if self.round_number <= Constants.num_training_rounds:
            yield pages.TrainingResults