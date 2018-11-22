from otree.api import Currency as c, currency_range

from ._builtin import Page, WaitPage
from .models import Constants
import json
import random


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

class _1Dice(Page):
    form_model = 'player'
    form_fields = ['rand_selector']

    def vars_for_template(self):
        return {
            'rand_range': max(self.participant.vars['round_cut']),
            'round_range': random.shuffle([i for i in range(1,max(self.participant.vars['round_cut'])+1)])
        }

    def before_next_page(self):
        self.player.payoff_rand()

class _1Roulette(Page):
    form_model = 'player'
    form_fields = ['rand_selector']

    def vars_for_template(self):
        return {
            'rand_range': max(self.participant.vars['round_cut']),
            'round_range': [j+i for i, j in zip(range(1,max(self.participant.vars['round_cut'])+1), ['A2', 'B2'])]
        }

    def before_next_page(self):
        self.player.payoff_rand()

class _2ThankYou(Page):

    def vars_for_template(self):
        return {
            'total_earnings': self.participant.payoff_plus_participation_fee(),
            'payoff_game': self.player.rand_selector[0] + "2",
            'payoff_round': self.player.rand_selector[-1],
            'points_rand': self.player.points_rand * 0.5,
            'points_a1': self.player.points_A1 * 0.25,
            'points_b1': self.player.points_B1 * 0.25,
            'payoff_matrix': json.loads(self.player.result_matrix),
            'points_total': (self.player.points_rand * 0.5) + (self.player.points_A1 * 0.25) + (self.player.points_B1 * 0.25),
            'currency': self.session.config['real_world_currency_per_point'],
            'showup': self.session.config['participation_fee'],
        }

page_sequence = [
    _1Questionnaire,
    _1Dice,
    _2ThankYou
]
