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
    form_fields = ['a1','a2','a3','a4','a5','a6','a7','a8','a9',
                   'b1','b2','b3','b4','b5','b6','b7','b8','b9']

    def vars_for_template(self):
        return {
            'treatment_group': self.session.config["treatment_group"],
            'random_image_url': self.participant.vars["random_image_url"],
            'endowment': Constants.endo,
            'round': self.subsession.round_number if (
                        self.subsession.training_round == True) else self.subsession.round_number - 2,
            'x1G': self.subsession.x1G,
            'x2G': self.subsession.x2G,
            'x1B': self.subsession.x1B,
            'x2B': self.subsession.x2B,
            'unknown_prob_G': self.subsession.unknown_prob_G,
            't1G': self.subsession.t1G,
            't1B': self.subsession.t1B,
            't2G': self.subsession.t2G,
            't2B': self.subsession.t2B,
            'unknown_prob_B': self.subsession.unknown_prob_B,
            'pagehold_timer': self.session.config['page_halt_seconds'],
            'pagehold_timer_ths': self.session.config['page_halt_seconds'] * 1000,
        }

    def error_message(self, values):
        if values['a1'] + values['b1'] > Constants.endo:
            return 'Total G + B untuk seluruh kolom harus tidak lebih dari' + str(Constants.endo)
        if values['a2'] + values['b2'] > Constants.endo:
            return 'Total G + B untuk seluruh kolom harus tidak lebih dari' + str(Constants.endo)
        if values['a3'] + values['b3'] > Constants.endo:
            return 'Total G + B untuk seluruh kolom harus tidak lebih dari' + str(Constants.endo)
        if values['a4'] + values['b4'] > Constants.endo:
            return 'Total G + B untuk seluruh kolom harus tidak lebih dari' + str(Constants.endo)
        if values['a5'] + values['b5'] > Constants.endo:
            return 'Total G + B untuk seluruh kolom harus tidak lebih dari' + str(Constants.endo)
        if values['a6'] + values['b6'] > Constants.endo:
            return 'Total G + B untuk seluruh kolom harus tidak lebih dari' + str(Constants.endo)
        if values['a7'] + values['b7'] > Constants.endo:
            return 'Total G + B untuk seluruh kolom harus tidak lebih dari' + str(Constants.endo)
        if values['a8'] + values['b8'] > Constants.endo:
            return 'Total G + B untuk seluruh kolom harus tidak lebih dari' + str(Constants.endo)
        if values['a9'] + values['b9'] > Constants.endo:
            return 'Total G + B untuk seluruh kolom harus tidak lebih dari' + str(Constants.endo)

class wait2(WaitPage):

    def after_all_players_arrive(self):
        pass
        self.subsession.realization()

class TrainingResults(Page):

    def is_displayed(self):
        return self.subsession.round_number <= Constants.num_training_rounds

    def vars_for_template(self):
        selector = random.choice(list(range(1, 10)))
        a_select = [self.player.a1, self.player.a2, self.player.a3, self.player.a4,
                    self.player.a5, self.player.a6, self.player.a7, self.player.a8,
                    self.player.a9][selector - 1]
        b_select = [self.player.b1, self.player.b2, self.player.b3, self.player.b4,
                    self.player.b5, self.player.b6, self.player.b7, self.player.b8,
                    self.player.b9][selector - 1]
        param_select_G = random.choice([[self.subsession.x1G, self.subsession.t1G],
                                      [self.subsession.x2G, self.subsession.t2G]])
        param_select_B = random.choice([[self.subsession.x1B, self.subsession.t1B],
                                        [self.subsession.x2B, self.subsession.t2B]])
        xG_select = param_select_G[0]
        tG_select = param_select_G[1]
        xB_select = param_select_B[0]
        tB_select = param_select_B[1]
        unknown_prob_G = float(random.randint(1, 20))/100
        unknown_prob_B = float(random.randint(1, 20))/100
        payoff_1 = a_select * xG_select
        payoff_2 = b_select * xB_select
        leftover = Constants.endo - a_select - b_select
        payoff = payoff_1 + payoff_2 + leftover

        return {
            'selector': selector,
            'xG_select': xG_select,
            'tG_select': tG_select,
            'xB_select': xB_select,
            'tB_select': tB_select,
            'choice_select_G': a_select,
            'choice_select_B': b_select,
            'unknown_prob_G': unknown_prob_G,
            'unknown_prob_B': unknown_prob_B,
            'payoff_1_multiplied': payoff_1,
            'payoff_2_multiplied': payoff_2,
            'payoff_leftover': leftover,
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
