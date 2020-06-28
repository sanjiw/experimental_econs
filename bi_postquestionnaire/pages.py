from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Questionnaire(Page):
    form_model = "player"
    form_fields = ["q1_a","q1_b","q1_c","q1_d","q1_e",
                   "q2_a","q2_b","q2_c","q2_d","q2_e",
                   "q3_a","q3_b","q3_c","q3_d","q3_e",
                   "q4_a","q4_b","q4_c","q4_d","q4_e"]

class Results(Page):

    def vars_for_template(self):
        return {
            "payoff_list": self.participant.vars['payoff_vector_s1'],
        }


page_sequence = [Questionnaire, Results]
