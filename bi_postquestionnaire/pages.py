from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

import json
import random
import pandas

class Questionnaire(Page):

    form_model = "player"
    form_fields = ["q1_a", "q1_b", "q1_c", "q1_d", "q1_e",
                   "q2_a", "q2_b", "q2_c", "q2_d", "q2_e",
                   "q3_a", "q3_b", "q3_c", "q3_d", "q3_e",
                   "q4_a", "q4_b", "q4_c", "q4_d", "q4_e"]

    def vars_for_template(self):
        return {
                "decision_list"     : self.participant.vars['decision_list'],
                "game_type"         : self.participant.vars['game_type'],
                "x1G"               : self.participant.vars['x1G'],
                "x2G"               : self.participant.vars['x2G'],
                "unknown_prob_G"    : self.participant.vars['unknown_prob_G'],
                "x1B"               : self.participant.vars['x1B'],
                "x2B"               : self.participant.vars['x2B'],
                "unknown_prob_B"    : self.participant.vars['unknown_prob_B'],
                "t1G"               : self.participant.vars['t1G'],
                "t2G"               : self.participant.vars['t2G'],
                "t1B"               : self.participant.vars['t1B'],
                "t2B"               : self.participant.vars['t2B']
        }

    def before_next_page(self):
        self.subsession.payoff_dataframe()

class Payoff_RoundSelect(Page):

    form_model = "player"
    form_fields = ["round_selector"]

    def vars_for_template(self):
        return {
            'round_range': len(self.participant.vars['decision_list']),
        }

    def before_next_page(self):
        self.subsession.round_selector()

class Payoff_ListSelect(Page):

    form_model = "player"
    form_fields = ["list_selector"]

    def vars_for_template(self):
        round_selected = self.participant.vars["round_selected"]
        return {
            'chosen_round': self.player.round_selector,
            'chosen_game': round_selected["game_type"],
            'chosen_list': round_selected[""],
            'list_range': len(round_selected),
        }

    def before_next_page(self):
        self.subsession.list_selector()

class Payoff_ProbSelect(Page):


    def is_displayed(self):
        return self.participant.vars["round_selected"]['game_type'][0] == "risky_setup_3_ambi" or \
               self.participant.vars["round_selected"]['game_type'][0] == "risky_setup_4_ambi"

    form_model = "player"
    form_fields = ["prob_selector"]

    def vars_for_template(self):
        return {
            'max_uncertain_prob_G' : self.participant.vars["round_selected"]["unknown_prob_G"][0],
            'max_uncertain_prob_B' : self.participant.vars["round_selected"]["unknown_prob_B"][0]
        }

    def before_next_page(self):
        self.subsession.prob_selector()

class Payoff_PaymentSelect(Page):

    form_model = "player"
    form_fields = ["payment_selector"]

    def vars_for_template(self):
        return {

        }

    def before_next_page(self):
        self.subsession.payment_selector()

class Results(Page):

    def vars_for_template(self):
        return {
                "decision_list"     : self.participant.vars['decision_list'],
                "game_type"         : self.participant.vars['game_type'],
                "x1G"               : self.participant.vars['x1G'],
                "x2G"               : self.participant.vars['x2G'],
                "unknown_prob_G"    : self.participant.vars['unknown_prob_G'],
                "x1B"               : self.participant.vars['x1B'],
                "x2B"               : self.participant.vars['x2B'],
                "unknown_prob_B"    : self.participant.vars['unknown_prob_B'],
                "t1G"               : self.participant.vars['t1G'],
                "t2G"               : self.participant.vars['t2G'],
                "t1B"               : self.participant.vars['t1B'],
                "t2B"               : self.participant.vars['t2B']
        }


page_sequence = [Questionnaire,
                 Payoff_RoundSelect,
                 Payoff_ListSelect,
                 Payoff_ProbSelect,
                 Payoff_PaymentSelect,
                 Results]

