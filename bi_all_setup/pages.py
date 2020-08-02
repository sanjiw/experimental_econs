from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

import random

class Intro(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        return {
            'pagehold_timer'                : self.session.config['page_halt_seconds'],
            'pagehold_timer_ths'            : self.session.config['page_halt_seconds'] * 1000,
        }

    def before_next_page(self):
        self.player.sequence_setup()

class Instruction(Page):

    def is_displayed(self):
        return self.subsession.round_number in [1, 13, 25, 37]

    def vars_for_template(self):
        return {
            'setup': self.participant.vars["p_app_sequence"]['game_type'][self.round_number-1],
            'round_number': self.subsession.round_number,
            'treatment_group': self.participant.vars["p_app_sequence"]['treatment_group'][self.round_number - 1],
            'pagehold_timer'                : self.session.config['page_halt_seconds'],
            'pagehold_timer_ths'            : self.session.config['page_halt_seconds'] * 1000,
        }

class Mpl_setup1(Page):

    def is_displayed(self):
        return self.participant.vars["p_app_sequence"]['game_type'][self.round_number-1] == "risky_setup_1"

    form_model = 'player'
    form_fields = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'a10', 'a11']

    def vars_for_template(self):
        return {
            'game_type'             : self.participant.vars["p_app_sequence"]['game_type'][self.round_number-1],
            'training'              : True if self.participant.vars["p_app_sequence"]['training'][self.round_number-1] == "TRUE" else False,
            'treatment_group'       : self.participant.vars["p_app_sequence"]['treatment_group'][self.round_number-1],
            'random_image_url'      : self.participant.vars["p_app_sequence"]['random_image_urls'][self.round_number-1],
            'endowment'             : Constants.endo,
            'round'                 : self.participant.vars["p_app_sequence"]['round_num'][self.round_number-1],
            'x1G'                   : self.participant.vars["p_app_sequence"]['x1G'][self.round_number-1],
            'x2G'                   : self.participant.vars["p_app_sequence"]['x2G'][self.round_number-1],
            'x1B'                   : self.participant.vars["p_app_sequence"]['x1B'][self.round_number-1],
            'x2B'                   : self.participant.vars["p_app_sequence"]['x2B'][self.round_number-1],
            'unknown_prob_G'        : self.participant.vars["p_app_sequence"]['unknown_prob_G'][self.round_number-1],
            't1G'                   : self.participant.vars["p_app_sequence"]['t1G'][self.round_number-1],
            't1B'                   : self.participant.vars["p_app_sequence"]['t1B'][self.round_number-1],
            't2G'                   : self.participant.vars["p_app_sequence"]['t2G'][self.round_number-1],
            't2B'                   : self.participant.vars["p_app_sequence"]['t2B'][self.round_number-1],
            'unknown_prob_B'        : self.participant.vars["p_app_sequence"]['unknown_prob_B'][self.round_number-1],
            'pagehold_timer'        : self.session.config['page_halt_seconds'],
            'pagehold_timer_ths'    : self.session.config['page_halt_seconds'] * 1000,
            'params'                : self.participant.vars["p_app_sequence"],
            'decision_list'         : self.participant.vars['decision_list']
        }

    def before_next_page(self):
        self.player.param_record()
        self.player.decision_records()

class Mpl_setup2(Page):

    def is_displayed(self):
        return self.participant.vars["p_app_sequence"]['game_type'][self.round_number-1] == "risky_setup_2"

    form_model = 'player'
    form_fields = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'a10', 'a11',
                   'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'b10', 'b11']

    def vars_for_template(self):
        return {
            'game_type'             : self.participant.vars["p_app_sequence"]['game_type'][self.round_number-1],
            'training': True if self.participant.vars["p_app_sequence"]['training'][
                                    self.round_number - 1] == "TRUE" else False,
            'treatment_group': self.participant.vars["p_app_sequence"]['treatment_group'][self.round_number - 1],
            'random_image_url': self.participant.vars["p_app_sequence"]['random_image_urls'][self.round_number - 1],
            'endowment': Constants.endo,
            'round': self.participant.vars["p_app_sequence"]['round_num'][self.round_number - 1],
            'x1G': self.participant.vars["p_app_sequence"]['x1G'][self.round_number - 1],
            'x2G': self.participant.vars["p_app_sequence"]['x2G'][self.round_number - 1],
            'x1B': self.participant.vars["p_app_sequence"]['x1B'][self.round_number - 1],
            'x2B': self.participant.vars["p_app_sequence"]['x2B'][self.round_number - 1],
            'unknown_prob_G': self.participant.vars["p_app_sequence"]['unknown_prob_G'][self.round_number - 1],
            't1G': self.participant.vars["p_app_sequence"]['t1G'][self.round_number - 1],
            't1B': self.participant.vars["p_app_sequence"]['t1B'][self.round_number - 1],
            't2G': self.participant.vars["p_app_sequence"]['t2G'][self.round_number - 1],
            't2B': self.participant.vars["p_app_sequence"]['t2B'][self.round_number - 1],
            'unknown_prob_B': self.participant.vars["p_app_sequence"]['unknown_prob_B'][self.round_number - 1],
            'pagehold_timer': self.session.config['page_halt_seconds'],
            'pagehold_timer_ths': self.session.config['page_halt_seconds'] * 1000,
            'params': self.participant.vars["p_app_sequence"],
            'decision_list': self.participant.vars['decision_list']
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
        if values['a10'] + values['b10'] > Constants.endo:
            return 'Total G + B untuk seluruh kolom harus tidak lebih dari' + str(Constants.endo)
        if values['a11'] + values['b11'] > Constants.endo:
            return 'Total G + B untuk seluruh kolom harus tidak lebih dari' + str(Constants.endo)

    def before_next_page(self):
        self.player.param_record()
        self.player.decision_records()


class Mpl_setup3(Page):

    def is_displayed(self):
        return self.participant.vars["p_app_sequence"]['game_type'][self.round_number-1] == "risky_setup_3_ambi"

    form_model = 'player'
    form_fields = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9']

    def vars_for_template(self):
        return {
            'game_type'             : self.participant.vars["p_app_sequence"]['game_type'][self.round_number-1],
            'training': True if self.participant.vars["p_app_sequence"]['training'][
                                    self.round_number - 1] == "TRUE" else False,
            'treatment_group': self.participant.vars["p_app_sequence"]['treatment_group'][self.round_number - 1],
            'random_image_url': self.participant.vars["p_app_sequence"]['random_image_urls'][self.round_number - 1],
            'endowment': Constants.endo,
            'round': self.participant.vars["p_app_sequence"]['round_num'][self.round_number - 1],
            'x1G': self.participant.vars["p_app_sequence"]['x1G'][self.round_number - 1],
            'x2G': self.participant.vars["p_app_sequence"]['x2G'][self.round_number - 1],
            'x1B': self.participant.vars["p_app_sequence"]['x1B'][self.round_number - 1],
            'x2B': self.participant.vars["p_app_sequence"]['x2B'][self.round_number - 1],
            'unknown_prob_G': self.participant.vars["p_app_sequence"]['unknown_prob_G'][self.round_number - 1],
            't1G': self.participant.vars["p_app_sequence"]['t1G'][self.round_number - 1],
            't1B': self.participant.vars["p_app_sequence"]['t1B'][self.round_number - 1],
            't2G': self.participant.vars["p_app_sequence"]['t2G'][self.round_number - 1],
            't2B': self.participant.vars["p_app_sequence"]['t2B'][self.round_number - 1],
            'unknown_prob_B': self.participant.vars["p_app_sequence"]['unknown_prob_B'][self.round_number - 1],
            'pagehold_timer': self.session.config['page_halt_seconds'],
            'pagehold_timer_ths': self.session.config['page_halt_seconds'] * 1000,
            'params': self.participant.vars["p_app_sequence"],
            'decision_list': self.participant.vars['decision_list']
        }

    def before_next_page(self):
        self.player.param_record()
        self.player.decision_records()

class Mpl_setup4(Page):

    def is_displayed(self):
        return self.participant.vars["p_app_sequence"]['game_type'][self.round_number-1] == "risky_setup_4_ambi"

    form_model = 'player'
    form_fields = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9',
                   'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9']

    def vars_for_template(self):
        return {
            'game_type'             : self.participant.vars["p_app_sequence"]['game_type'][self.round_number-1],
            'training': True if self.participant.vars["p_app_sequence"]['training'][
                                    self.round_number - 1] == "TRUE" else False,
            'treatment_group': self.participant.vars["p_app_sequence"]['treatment_group'][self.round_number - 1],
            'random_image_url': self.participant.vars["p_app_sequence"]['random_image_urls'][self.round_number - 1],
            'endowment': Constants.endo,
            'round': self.participant.vars["p_app_sequence"]['round_num'][self.round_number - 1],
            'x1G': self.participant.vars["p_app_sequence"]['x1G'][self.round_number - 1],
            'x2G': self.participant.vars["p_app_sequence"]['x2G'][self.round_number - 1],
            'x1B': self.participant.vars["p_app_sequence"]['x1B'][self.round_number - 1],
            'x2B': self.participant.vars["p_app_sequence"]['x2B'][self.round_number - 1],
            'unknown_prob_G': self.participant.vars["p_app_sequence"]['unknown_prob_G'][self.round_number - 1],
            't1G': self.participant.vars["p_app_sequence"]['t1G'][self.round_number - 1],
            't1B': self.participant.vars["p_app_sequence"]['t1B'][self.round_number - 1],
            't2G': self.participant.vars["p_app_sequence"]['t2G'][self.round_number - 1],
            't2B': self.participant.vars["p_app_sequence"]['t2B'][self.round_number - 1],
            'unknown_prob_B': self.participant.vars["p_app_sequence"]['unknown_prob_B'][self.round_number - 1],
            'pagehold_timer': self.session.config['page_halt_seconds'],
            'pagehold_timer_ths': self.session.config['page_halt_seconds'] * 1000,
            'params': self.participant.vars["p_app_sequence"],
            'decision_list': self.participant.vars['decision_list']
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

    def before_next_page(self):
        self.player.param_record()
        self.player.decision_records()

class TrainingResults1(Page):

    def is_displayed(self):
        return self.participant.vars["p_app_sequence"]['training'][self.round_number - 1] == True and self.participant.vars["p_app_sequence"]['game_type'][self.round_number-1] == "risky_setup_1"

    def vars_for_template(self):
        selector = random.choice(list(range(1, 12)))
        a_select = [self.player.a1, self.player.a2, self.player.a3, self.player.a4,
                    self.player.a5, self.player.a6, self.player.a7, self.player.a8,
                    self.player.a9, self.player.a10, self.player.a11][selector - 1]
        param_select = random.choice([[self.participant.vars["p_app_sequence"]['x1G'][self.round_number - 1],
                                       self.participant.vars["p_app_sequence"]['t1G'][self.round_number - 1]],
                                      [self.participant.vars["p_app_sequence"]['x2G'][self.round_number - 1],
                                       self.participant.vars["p_app_sequence"]['t2G'][self.round_number - 1]]])
        xG_select = param_select[0]
        tG_select = param_select[1]
        payoff_1 = a_select * xG_select
        payoff_2 = Constants.endo - a_select
        payoff = payoff_1 + payoff_2
        return {
            'game_type': self.participant.vars["p_app_sequence"]['game_type'][self.round_number - 1],
            'selector': selector,
            'a_select': a_select,
            'xG_select': xG_select,
            'tG_select': tG_select,
            'payoff_1_multiplied': payoff_1,
            'payoff_2_leftover': payoff_2,
            'payoff': payoff,
            'pagehold_timer': self.session.config['page_halt_seconds'],
            'pagehold_timer_ths': self.session.config['page_halt_seconds'] * 1000,
            'training': True if self.participant.vars["p_app_sequence"]['training'][
                                    self.round_number - 1] == "TRUE" else False,
            'treatment_group': self.participant.vars["p_app_sequence"]['treatment_group'][self.round_number - 1],
            'random_image_url': self.participant.vars["p_app_sequence"]['random_image_urls'][self.round_number - 1],
            'endowment': Constants.endo,
            'round': self.participant.vars["p_app_sequence"]['round_num'][self.round_number - 1],
            'x1G': self.participant.vars["p_app_sequence"]['x1G'][self.round_number - 1],
            'x2G': self.participant.vars["p_app_sequence"]['x2G'][self.round_number - 1],
            'x1B': self.participant.vars["p_app_sequence"]['x1B'][self.round_number - 1],
            'x2B': self.participant.vars["p_app_sequence"]['x2B'][self.round_number - 1],
            'unknown_prob_G': self.participant.vars["p_app_sequence"]['unknown_prob_G'][self.round_number - 1],
            't1G': self.participant.vars["p_app_sequence"]['t1G'][self.round_number - 1],
            't1B': self.participant.vars["p_app_sequence"]['t1B'][self.round_number - 1],
            't2G': self.participant.vars["p_app_sequence"]['t2G'][self.round_number - 1],
            't2B': self.participant.vars["p_app_sequence"]['t2B'][self.round_number - 1],
            'unknown_prob_B': self.participant.vars["p_app_sequence"]['unknown_prob_B'][self.round_number - 1],
        }

class TrainingResults2(Page):

    def is_displayed(self):
        return self.participant.vars["p_app_sequence"]['training'][self.round_number - 1] == True and self.participant.vars["p_app_sequence"]['game_type'][self.round_number-1] == "risky_setup_2"

    def vars_for_template(self):
        selector = random.choice(list(range(1, 12)))
        a_select = [self.player.a1, self.player.a2, self.player.a3, self.player.a4,
                    self.player.a5, self.player.a6, self.player.a7, self.player.a8,
                    self.player.a9, self.player.a10, self.player.a11][selector - 1]
        b_select = [self.player.b1, self.player.b2, self.player.b3, self.player.b4,
                    self.player.b5, self.player.b6, self.player.b7, self.player.b8,
                    self.player.b9, self.player.b10, self.player.b11][selector - 1]
        param_select_G = random.choice([[self.participant.vars["p_app_sequence"]['x1G'][self.round_number - 1],
                                         self.participant.vars["p_app_sequence"]['t1G'][self.round_number - 1]],
                                        [self.participant.vars["p_app_sequence"]['x2G'][self.round_number - 1],
                                         self.participant.vars["p_app_sequence"]['t2G'][self.round_number - 1]]])
        param_select_B = random.choice([[self.participant.vars["p_app_sequence"]['x1B'][self.round_number - 1],
                                         self.participant.vars["p_app_sequence"]['t1B'][self.round_number - 1]],
                                        [self.participant.vars["p_app_sequence"]['x2B'][self.round_number - 1],
                                         self.participant.vars["p_app_sequence"]['t2B'][self.round_number - 1]]])
        xG_select = param_select_G[0]
        tG_select = param_select_G[1]
        xB_select = param_select_B[0]
        tB_select = param_select_B[1]
        payoff_1 = a_select * xG_select
        payoff_2 = b_select * xB_select
        leftover = Constants.endo - a_select - b_select
        payoff = payoff_1 + payoff_2 + leftover

        return {
            'game_type': self.participant.vars["p_app_sequence"]['game_type'][self.round_number - 1],
            'selector': selector,
            'xG_select': xG_select,
            'tG_select': tG_select,
            'xB_select': xB_select,
            'tB_select': tB_select,
            'choice_select_G': a_select,
            'choice_select_B': b_select,
            'payoff_1_multiplied': payoff_1,
            'payoff_2_multiplied': payoff_2,
            'payoff_leftover': leftover,
            'payoff': payoff,
            'pagehold_timer': self.session.config['page_halt_seconds'],
            'pagehold_timer_ths': self.session.config['page_halt_seconds'] * 1000,
            'training': True if self.participant.vars["p_app_sequence"]['training'][
                                    self.round_number - 1] == "TRUE" else False,
            'treatment_group': self.participant.vars["p_app_sequence"]['treatment_group'][self.round_number - 1],
            'random_image_url': self.participant.vars["p_app_sequence"]['random_image_urls'][self.round_number - 1],
            'endowment': Constants.endo,
            'round': self.participant.vars["p_app_sequence"]['round_num'][self.round_number - 1],
            'x1G': self.participant.vars["p_app_sequence"]['x1G'][self.round_number - 1],
            'x2G': self.participant.vars["p_app_sequence"]['x2G'][self.round_number - 1],
            'x1B': self.participant.vars["p_app_sequence"]['x1B'][self.round_number - 1],
            'x2B': self.participant.vars["p_app_sequence"]['x2B'][self.round_number - 1],
            'unknown_prob_G': self.participant.vars["p_app_sequence"]['unknown_prob_G'][self.round_number - 1],
            't1G': self.participant.vars["p_app_sequence"]['t1G'][self.round_number - 1],
            't1B': self.participant.vars["p_app_sequence"]['t1B'][self.round_number - 1],
            't2G': self.participant.vars["p_app_sequence"]['t2G'][self.round_number - 1],
            't2B': self.participant.vars["p_app_sequence"]['t2B'][self.round_number - 1],
            'unknown_prob_B': self.participant.vars["p_app_sequence"]['unknown_prob_B'][self.round_number - 1],
        }

class TrainingResults3(Page):

    def is_displayed(self):
        return self.participant.vars["p_app_sequence"]['training'][self.round_number - 1] == True and self.participant.vars["p_app_sequence"]['game_type'][self.round_number-1] == "risky_setup_3_ambi"

    def vars_for_template(self):
        selector = random.choice(list(range(1, 10)))
        a_select = [self.player.a1, self.player.a2, self.player.a3, self.player.a4,
                    self.player.a5, self.player.a6, self.player.a7, self.player.a8,
                    self.player.a9][selector - 1]
        param_select = random.choice([[self.participant.vars["p_app_sequence"]['x1G'][self.round_number - 1],
                                       self.participant.vars["p_app_sequence"]['t1G'][self.round_number - 1]],
                                      [self.participant.vars["p_app_sequence"]['x2G'][self.round_number - 1],
                                       self.participant.vars["p_app_sequence"]['t2G'][self.round_number - 1]]])
        unknown_prob = float(random.randint(1, 20)) / 100
        xG_select = param_select[0]
        tG_select = param_select[1]
        payoff_1 = a_select * xG_select
        payoff_2 = Constants.endo - a_select
        payoff = payoff_1 + payoff_2
        return {
            'game_type': self.participant.vars["p_app_sequence"]['game_type'][self.round_number - 1],
            'selector': selector,
            'a_select': a_select,
            'xG_select': xG_select,
            'tG_select': tG_select,
            'unknown_p': self.participant.vars["p_app_sequence"]['unknown_prob_G'][self.round_number - 1],
            'payoff_1_multiplied': payoff_1,
            'payoff_2_leftover': payoff_2,
            'payoff': payoff,
            'pagehold_timer': self.session.config['page_halt_seconds'],
            'pagehold_timer_ths': self.session.config['page_halt_seconds'] * 1000,
            'training': True if self.participant.vars["p_app_sequence"]['training'][
                                    self.round_number - 1] == "TRUE" else False,
            'treatment_group': self.participant.vars["p_app_sequence"]['treatment_group'][self.round_number - 1],
            'random_image_url': self.participant.vars["p_app_sequence"]['random_image_urls'][self.round_number - 1],
            'endowment': Constants.endo,
            'round': self.participant.vars["p_app_sequence"]['round_num'][self.round_number - 1],
            'x1G': self.participant.vars["p_app_sequence"]['x1G'][self.round_number - 1],
            'x2G': self.participant.vars["p_app_sequence"]['x2G'][self.round_number - 1],
            'x1B': self.participant.vars["p_app_sequence"]['x1B'][self.round_number - 1],
            'x2B': self.participant.vars["p_app_sequence"]['x2B'][self.round_number - 1],
            'unknown_prob_G': self.participant.vars["p_app_sequence"]['unknown_prob_G'][self.round_number - 1],
            't1G': self.participant.vars["p_app_sequence"]['t1G'][self.round_number - 1],
            't1B': self.participant.vars["p_app_sequence"]['t1B'][self.round_number - 1],
            't2G': self.participant.vars["p_app_sequence"]['t2G'][self.round_number - 1],
            't2B': self.participant.vars["p_app_sequence"]['t2B'][self.round_number - 1],
            'unknown_prob_B': self.participant.vars["p_app_sequence"]['unknown_prob_B'][self.round_number - 1],
        }

class TrainingResults4(Page):

    def is_displayed(self):
        return self.participant.vars["p_app_sequence"]['training'][self.round_number - 1] == True and self.participant.vars["p_app_sequence"]['game_type'][self.round_number-1] == "risky_setup_4_ambi"

    def vars_for_template(self):
        selector = random.choice(list(range(1, 10)))
        a_select = [self.player.a1, self.player.a2, self.player.a3, self.player.a4,
                    self.player.a5, self.player.a6, self.player.a7, self.player.a8,
                    self.player.a9][selector - 1]
        b_select = [self.player.b1, self.player.b2, self.player.b3, self.player.b4,
                    self.player.b5, self.player.b6, self.player.b7, self.player.b8,
                    self.player.b9][selector - 1]
        param_select_G = random.choice([[self.participant.vars["p_app_sequence"]['x1G'][self.round_number - 1],
                                         self.participant.vars["p_app_sequence"]['t1G'][self.round_number - 1]],
                                        [self.participant.vars["p_app_sequence"]['x2G'][self.round_number - 1],
                                         self.participant.vars["p_app_sequence"]['t2G'][self.round_number - 1]]])
        param_select_B = random.choice([[self.participant.vars["p_app_sequence"]['x1B'][self.round_number - 1],
                                         self.participant.vars["p_app_sequence"]['t1B'][self.round_number - 1]],
                                        [self.participant.vars["p_app_sequence"]['x2B'][self.round_number - 1],
                                         self.participant.vars["p_app_sequence"]['t2B'][self.round_number - 1]]])
        xG_select = param_select_G[0]
        tG_select = param_select_G[1]
        xB_select = param_select_B[0]
        tB_select = param_select_B[1]
        unknown_prob_G = float(random.randint(1, 20)) / 100
        unknown_prob_B = float(random.randint(1, 20)) / 100
        payoff_1 = a_select * xG_select
        payoff_2 = b_select * xB_select
        leftover = Constants.endo - a_select - b_select
        payoff = payoff_1 + payoff_2 + leftover

        return {
            'game_type': self.participant.vars["p_app_sequence"]['game_type'][self.round_number - 1],
            'selector': selector,
            'xG_select': xG_select,
            'tG_select': tG_select,
            'xB_select': xB_select,
            'tB_select': tB_select,
            'choice_select_G': a_select,
            'choice_select_B': b_select,
            'payoff_1_multiplied': payoff_1,
            'payoff_2_multiplied': payoff_2,
            'payoff_leftover': leftover,
            'payoff': payoff,
            'pagehold_timer': self.session.config['page_halt_seconds'],
            'pagehold_timer_ths': self.session.config['page_halt_seconds'] * 1000,
            'training': True if self.participant.vars["p_app_sequence"]['training'][
                                    self.round_number - 1] == "TRUE" else False,
            'treatment_group': self.participant.vars["p_app_sequence"]['treatment_group'][self.round_number - 1],
            'random_image_url': self.participant.vars["p_app_sequence"]['random_image_urls'][self.round_number - 1],
            'endowment': Constants.endo,
            'round': self.participant.vars["p_app_sequence"]['round_num'][self.round_number - 1],
            'x1G': self.participant.vars["p_app_sequence"]['x1G'][self.round_number - 1],
            'x2G': self.participant.vars["p_app_sequence"]['x2G'][self.round_number - 1],
            'x1B': self.participant.vars["p_app_sequence"]['x1B'][self.round_number - 1],
            'x2B': self.participant.vars["p_app_sequence"]['x2B'][self.round_number - 1],
            'unknown_prob_G': self.participant.vars["p_app_sequence"]['unknown_prob_G'][self.round_number - 1],
            't1G': self.participant.vars["p_app_sequence"]['t1G'][self.round_number - 1],
            't1B': self.participant.vars["p_app_sequence"]['t1B'][self.round_number - 1],
            't2G': self.participant.vars["p_app_sequence"]['t2G'][self.round_number - 1],
            't2B': self.participant.vars["p_app_sequence"]['t2B'][self.round_number - 1],
            'unknown_prob_B': self.participant.vars["p_app_sequence"]['unknown_prob_B'][self.round_number - 1],
        }


class WarningPage(Page):

    def is_displayed(self):
        return self.subsession.round_number in [2, 14, 26, 38]

    def vars_for_template(self):
        return {
            'pagehold_timer'        : self.session.config['page_halt_seconds'],
            'pagehold_timer_ths'    : self.session.config['page_halt_seconds'] * 1000,
        }

page_sequence = [Intro,
                 Instruction,
                 Mpl_setup1,
                 Mpl_setup2,
                 Mpl_setup3,
                 Mpl_setup4,
                 TrainingResults1,
                 TrainingResults2,
                 TrainingResults3,
                 TrainingResults4,
                 WarningPage]
