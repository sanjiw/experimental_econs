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
        yield pages.Mpl, dict(a1=5, a2=4, a3=3, a4=2, a5=3, a6=9, a7=7, a8=15, a9=12, a10=12, a11=1)
        if self.round_number <= Constants.num_training_rounds:
            yield pages.TrainingResults
