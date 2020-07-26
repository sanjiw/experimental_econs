from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random

class Instruction(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1

    def before_next_page(self):
        self.subsession.parameter_set()

    def vars_for_template(self):
        return {
            'pagehold_timer': self.session.config['page_halt_seconds'],
            'pagehold_timer_ths': self.session.config['page_halt_seconds'] * 1000,
        }

class wait1(WaitPage):

    def after_all_players_arrive(self):
        self.subsession.parameter_set()

class WarningPage(Page):

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_training_rounds + 1

class Mpl(Page):

    form_model = 'player'
    form_fields = ['a1','a2','a3','a4','a5','a6','a7','a8','a9','a10','a11']

    def vars_for_template(self):
        return {
            'treatment_group': self.session.config["treatment_group"],
            'random_image_url': self.participant.vars["random_image_url"],
            'endowment': Constants.endo,
            'round': self.subsession.round_number if (self.subsession.training_round == True) else self.subsession.round_number - 2,
            'x1G': self.subsession.x1G,
            'x2G': self.subsession.x2G,
            't1G': self.subsession.t1G,
            't2G': self.subsession.t2G,
            'pagehold_timer': self.session.config['page_halt_seconds'],
            'pagehold_timer_ths': self.session.config['page_halt_seconds']*1000,
        }

class wait2(WaitPage):

    def after_all_players_arrive(self):
        pass
        self.subsession.realization()

class TrainingResults(Page):

    def is_displayed(self):
        return self.subsession.round_number <= Constants.num_training_rounds

    def vars_for_template(self):
        selector = random.choice(list(range(1,12)))
        a_select = [self.player.a1, self.player.a2, self.player.a3, self.player.a4,
                    self.player.a5, self.player.a6, self.player.a7, self.player.a8,
                    self.player.a9, self.player.a10, self.player.a11][selector-1]
        param_select = random.choice([[self.subsession.x1G, self.subsession.t1G],
                                   [self.subsession.x2G, self.subsession.t2G]])
        xG_select = param_select[0]
        tG_select = param_select[1]
        payoff_1 = a_select * xG_select
        payoff_2 = Constants.endo - a_select
        payoff = payoff_1 + payoff_2
        return {
            'selector': selector,
            'a_select': a_select,
            'xG_select': xG_select,
            'tG_select': tG_select,
            'payoff_1_multiplied': payoff_1,
            'payoff_2_leftover': payoff_2,
            'payoff': payoff,
            'pagehold_timer': self.session.config['page_halt_seconds'],
            'pagehold_timer_ths': self.session.config['page_halt_seconds'] * 1000,
        }



page_sequence = [Instruction,
                 wait1,
                 WarningPage,
                 Mpl,
                 wait2,
                 TrainingResults]
