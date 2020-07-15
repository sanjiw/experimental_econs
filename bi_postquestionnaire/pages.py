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

class Payoff(Page):

    form_model = "player"
    form_fields = ["round_selector"]

    def vars_for_template(self):
        return {
            'rand_range': 40
        }

class Results(Page):

    def vars_for_template(self):
        return {
            'payoff_vector_s1': self.participant.vars['payoff_vector_s1'],
            'game_type': self.participant.vars['game_type'],
            'MPL_selector_index': self.participant.vars['MPL_selector_index'],
            'Choice_selection_G': self.participant.vars["Choice_selection_G"],
            'Choice_selection_B': self.participant.vars["Choice_selection_B"],
            'xG_select': self.participant.vars["xG_select"],
            'xB_select': self.participant.vars["xB_select"],
            'unknown_prob_G': self.participant.vars["unknown_prob_G"],
            'unknown_prob_B': self.participant.vars["unknown_prob_B"]
        }


page_sequence = [Questionnaire, Payoff, Results]

