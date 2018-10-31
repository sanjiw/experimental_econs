from ._builtin import Page, WaitPage
from .models import Constants, Player, Group
from otree.api import (Currency as c)
import numpy as np


class Introduction(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1
    def vars_for_template(self):
        return {
            'num_training_rounds': self.session.config['num_training_rounds'],
            'endowment': self.session.config['endowment']
        }


class InitialWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.subsession.endowment_rule()
        self.group.endow_group()


class Contribute(Page):
    """ Player: How much to contribute in Public Goods (High or Low)"""
    form_model = 'player'
    form_fields = ['choice']
    timer_text = "Waktu yang tersisa di halaman ini:"

    def get_timeout_seconds(self):
        return self.group.timeout

    def choice_max(self):
        return self.group.endowment

    def before_next_page(self):
        self.player.set_contribute()
        if self.timeout_happened:
            self.player.choice = np.random.randint(0,self.session.config['endowment'])


class ContributionWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs1()
        self.group.prob_punishment()

    body_text = "Menunggu peserta lainnya..."

class Embezzlement(Page):
    """ Embezzler: How much to embezzle the public goods"""
    form_model = 'player'
    form_fields = ['amount_embezzled']
    timer_text = "Waktu yang tersisa di halaman ini:"

    def get_timeout_seconds(self):
        return self.group.timeout

    def amount_embezzled_max(self):
        return self.group.total_contribution

    def is_displayed(self):
        return self.player.embezzler == True

    def before_next_page(self):
        self.group.set_payoffs1()


class EmbezzlementWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs2()

    body_text = "Menunggu peserta lainnya..."

class  ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        pass

class Results(Page):
    """Players payoff: How much each has earned"""
    timer_text = "Waktu yang tersisa di halaman ini:"

    def get_timeout_seconds(self):
        return self.group.timeout

    def before_next_page(self):
        return self.player.payoff_vector_storage()


page_sequence = [
    Introduction,
    InitialWaitPage,
    Contribute,
    ContributionWaitPage,
    Embezzlement,
    EmbezzlementWaitPage,
    ###CaughtPage,
    Results
]