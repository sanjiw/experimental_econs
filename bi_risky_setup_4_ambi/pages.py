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
    form_fields = ['a1','a2','a3','a4','a5','a6','a7','a8','a9',
                   'b1','b2','b3','b4','b5','b6','b7','b8','b9']

    def vars_for_template(self):
        return {
            'round': self.subsession.round_number if (self.subsession.training_round == True) else self.subsession.round_number - 2,
            'x1G': self.subsession.x1G,
            'x2G': self.subsession.x2G,
            'x1B': self.subsession.x1B,
            'x2B': self.subsession.x2B
        }

    def error_message(self, values):
        if values['a1'] + values['b1'] > 25:
            return 'Total G + B untuk seluruh kolom harus tidak lebih dari' + str(Constants.endowment)
        if values['a2'] + values['b2'] > 25:
            return 'Total G + B untuk seluruh kolom harus tidak lebih dari' + str(Constants.endowment)
        if values['a3'] + values['b3'] > 25:
            return 'Total G + B untuk seluruh kolom harus tidak lebih dari' + str(Constants.endowment)
        if values['a4'] + values['b4'] > 25:
            return 'Total G + B untuk seluruh kolom harus tidak lebih dari' + str(Constants.endowment)
        if values['a5'] + values['b5'] > 25:
            return 'Total G + B untuk seluruh kolom harus tidak lebih dari' + str(Constants.endowment)
        if values['a6'] + values['b6'] > 25:
            return 'Total G + B untuk seluruh kolom harus tidak lebih dari' + str(Constants.endowment)
        if values['a7'] + values['b7'] > 25:
            return 'Total G + B untuk seluruh kolom harus tidak lebih dari' + str(Constants.endowment)
        if values['a8'] + values['b8'] > 25:
            return 'Total G + B untuk seluruh kolom harus tidak lebih dari' + str(Constants.endowment)
        if values['a9'] + values['b9'] > 25:
            return 'Total G + B untuk seluruh kolom harus tidak lebih dari' + str(Constants.endowment)

class wait2(WaitPage):

    def after_all_players_arrive(self):
        pass
        self.subsession.payoff_realization()

class TrainingResults(Page):

    def is_displayed(self):
        return self.subsession.round_number <= Constants.num_training_rounds

    def vars_for_template(self):
        return {
            'selector'  : self.player.selector_index,
            'xG_select' : self.player.xG_select,
            'xB_select' : self.player.xB_select,
            'choice_select_G': self.player.choice_selection_G,
            'choice_select_B': self.player.choice_selection_B,
            'unknown_prob_G': self.player.unknown_prob_G,
            'unknown_prob_B': self.player.unknown_prob_B,
            'payoff_1_multiplied': self.player.xG_select * self.player.choice_selection_G,
            'payoff_2_multiplied': self.player.xB_select * self.player.choice_selection_B,
            'payoff_leftover': Constants.endowment - self.player.choice_selection_G - self.player.choice_selection_B,
            'payoff'    : self.player.payoff
        }


page_sequence = [Instruction,
                 wait1,
                 WarningPage,
                 Mpl,
                 wait2,
                 TrainingResults]
