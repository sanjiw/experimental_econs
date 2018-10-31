from otree.api import Currency as c, currency_range

from ._builtin import Page, WaitPage
from .models import Constants


class _1Questionnaire(Page):
    form_model = 'player'
    form_fields = ['fullname',
                   'age',
                   'year_entry',
                   'gender',
                   'faculty',
                   'seasoned',
                   'dwellings',
                   'work_status',
                   'pocket_money',
                   'faith','moral',
                   'brothers_rank','brothers_sum',
                   'perceived_wealth']

    def before_next_page(self):
        self.player.payoff_rand()

class _2ThankYou(Page):

    def vars_for_template(self):
        return {
            'total_earnings': self.participant.payoff_plus_participation_fee(),
            'payoff_round': self.player.payround,
        }

page_sequence = [
    _1Questionnaire,
    _2ThankYou
]
