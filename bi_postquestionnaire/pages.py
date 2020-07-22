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
            'round_range': len(self.participant.vars['player_dataframe']['decision_list']),
        }

    def before_next_page(self):
        self.subsession.round_selector()

class Payoff_UncertaintySelect(Page):

    def is_displayed(self):
        round_selected = self.participant.vars["round_selected"]
        return round_selected['game_type'][0] == "risky_setup_3_ambi" or \
               round_selected['game_type'][0] == "risky_setup_4_ambi"

    form_model = "player"
    form_fields = ["unct_selector_G",
                   "unct_selector_B"]

    def vars_for_template(self):
        round_selected = self.participant.vars["round_selected"]
        return {
            'show_uncertain_prob_B': True if round_selected["game_type"] == "risky_setup_4_ambi" else False,
            'max_uncertain_prob_G' : round_selected["unknown_prob_G"],
            'max_uncertain_prob_B' : round_selected["unknown_prob_B"],
            'ambiguous_list': Constants.Ambiguous_list
        }

class Payoff_DecisionSelect(Page):

    form_model = "player"
    form_fields = ["decision_selector"]

    def vars_for_template(self):
        round_selected = self.participant.vars["round_selected"]
        return {
            'decision_range': len(round_selected["decision_list"])
        }

    def before_next_page(self):
        self.subsession.decision_selector()

class Payoff_PaymentSelect(Page):

    form_model = "player"
    form_fields = ["urn_G",
                   "urn_B"]

    def vars_for_template(self):
        round_selected = self.participant.vars["round_selected"]
        return {
            "show_uncertain_prob_B": True if round_selected["game_type"] == "risky_setup_4_ambi" else False,
            "x1G_selected": self.participant.vars["x1G_selected"],
            "x2G_selected": self.participant.vars["x2G_selected"],
            "t1G_selected": self.participant.vars["t1G_selected"],
            "t2G_selected": self.participant.vars["t2G_selected"],
            "x1B_selected": self.participant.vars["x1B_selected"],
            "x2B_selected": self.participant.vars["x2B_selected"],
            "t1B_selected": self.participant.vars["t1B_selected"],
            "t2B_selected": self.participant.vars["t2B_selected"],
        }

    def before_next_page(self):
        self.subsession.payment_realization()

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
                "t2B"               : self.participant.vars['t2B'],

                "alloc_G"           : self.participant.vars["allocated_G"],
                "thres_G"           : self.participant.vars["threshold_G"],
                "alloc_B"           : self.participant.vars["allocated_B"],
                "thres_B"           : self.participant.vars["threshold_B"],

                "xG_final"          : self.participant.vars["xG_final"],
                "xB_final"          : self.participant.vars["xB_final"],
                "tG_final"          : self.participant.vars["tG_final"],
                "tB_final"          : self.participant.vars["tB_final"],
                "payoff_1"          : self.participant.vars["payoff_1"],
                "payoff_2"          : self.participant.vars["payoff_2"],
                "payoff_leftover"   : self.participant.vars["payoff_leftover"],
                "payoff_final"      : self.participant.vars["payoff_1"] + self.participant.vars["payoff_2"] + self.participant.vars["payoff_leftover"]
        }


page_sequence = [Questionnaire,
                 Payoff_RoundSelect,
                 Payoff_UncertaintySelect,
                 Payoff_DecisionSelect,
                 Payoff_PaymentSelect,
                 Results]

