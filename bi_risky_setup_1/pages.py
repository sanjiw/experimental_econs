from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Instruction(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1

    def before_next_page(self):
        self.subsession.parameter_set()

class wait1(WaitPage):

    def after_all_players_arrive(self):
        self.subsession.parameter_set()

class Mpl(Page):

    form_model = 'player'
    form_fields = ['a1','a2','a3','a4','a5','a6','a7','a8','a9','a10','a11']

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


class Results(Page):

    def vars_for_template(self):
        return {
            'selector': self.player.selector,
            'a_select': self.player.a_select,
            'xG_select': self.player.xG_select,
            'payoff_1_multiplied': self.player.xG_select * self.player.a_select,
            'payoff_2_leftover': Constants.endowment - self.player.a_select,
            'payoff': self.player.payoff
        }


page_sequence = [Instruction,
                 wait1,
                 Mpl,
                 wait2,
                 Results]
