from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random

class Instruction(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1

    def before_next_page(self):
        self.subsession.parameter_set()

class wait1(WaitPage):

    def after_all_players_arrive(self):
        self.subsession.parameter_set()

class WarningPage(Page):

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_training_rounds + 1

class Mpl(Page):

    form_model = 'player'
    form_fields = ['a1','a2','a3','a4','a5','a6','a7','a8','a9']

    def vars_for_template(self):
        return {
            'round': self.subsession.round_number if (self.subsession.training_round == True) else self.subsession.round_number - 2,
            'x1G': self.subsession.x1G,
            'x2G': self.subsession.x2G,
        }

class wait2(WaitPage):

    def after_all_players_arrive(self):
        pass
        self.subsession.payoff_realization()

class TrainingResults(Page):

    def is_displayed(self):
        return self.subsession.round_number <= Constants.num_training_rounds

    def vars_for_template(self):
        return {
            'selector': self.player.selector_index,
            'a_select': self.player.selected_a,
            'xG_select': self.player.selected_xG,
            'unknown_p': self.player.unknown_prob,
            'payoff_1_multiplied': self.player.selected_xG * self.player.selected_a,
            'payoff_2_leftover': Constants.endowment - self.player.selected_a,
            'payoff': self.player.payoff
        }


page_sequence = [Instruction,
                 wait1,
                 WarningPage,
                 Mpl,
                 wait2,
                 TrainingResults]