from ._builtin import Page, WaitPage
from .models import Constants, Player, Group
from otree.api import (Currency as c)
import numpy as np

class Introduction(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        return {
            'num_rounds': Constants.num_rounds - self.session.config['num_training_rounds'] - 1,
            'num_training_rounds': self.session.config['num_training_rounds'],
            'endowment': self.session.config['endowment'],
            'timeout': self.session.config['timeout_real']
        }


class IntroWaitPage(WaitPage):

    title_text = "Mohon menunggu:"
    body_text = "Menunggu peserta lainnya..."

    def is_displayed(self):
        return self.subsession.round_number == 1

class Instructions(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1

class RealGameWarning(Page):

    def is_displayed(self):
        return self.subsession.round_number == (self.session.config['num_training_rounds'] + 1)

class InitialWaitPage(WaitPage):

    title_text = "Mohon menunggu:"
    body_text = "Menunggu peserta lainnya..."

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
        #if self.timeout_happened:
        #    self.player.choice = np.random.randint(0, self.session.config['endowment'])
        #    self.player.contribution = self.player.choice

    def vars_for_template(self):
        return {
            'round': self.round_number - self.session.config['num_training_rounds'] - 1,
        }


class ContributionWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs1()

    title_text = "Mohon menunggu:"
    body_text = "Menunggu peserta lainnya..."


class Embezzlement(Page):
    """ Embezzler: How much to embezzle the public goods"""
    form_model = 'player'
    form_fields = ['amount_embezzled']
    timer_text = "Waktu yang tersisa di halaman ini:"

    def get_timeout_seconds(self):
        return self.group.timeout

    def is_displayed(self):
        return self.player.briber == True

    def before_next_page(self):
        return self.group.cal_embezzlement()

    def amount_embezzled_max(self):
        return self.group.total_contribution

    def vars_for_template(self):
        return {
            'round': self.round_number - self.session.config['num_training_rounds'] - 1,
        }


class Bribe(Page):

    form_model = 'player'
    form_fields = ['bribe_pct']
    timer_text = "Waktu yang tersisa di halaman ini:"

    def get_timeout_seconds(self):
        return self.group.timeout

    def is_displayed(self):
        return self.player.briber == True

    def before_next_page(self):
        self.player.money_alloc()

    def vars_for_template(self):
        return {
            'round': self.round_number - self.session.config['num_training_rounds'] - 1,
        }


class PostWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.bribe_acceptance_rule()
        self.group.prob_punishment()
        self.group.set_payoffs2()

    title_text = "Mohon menunggu:"
    body_text = "Menunggu peserta lainnya..."


class Results(Page):
    """Players payoff: How much each has earned"""
    def vars_for_template(self):
        return {
            'total_earnings': self.player.payoff,
            'indv_share_project': self.group.social_welfare_embz / Constants.players_per_group,
            'indv_share_project_full': self.group.social_welfare / Constants.players_per_group,
            'point_left': self.player.endowment - self.player.contribution,
            'fine': self.session.config['punish_fine'],
            'social_cost': (self.group.social_welfare - self.group.social_welfare_embz) * self.session.config['social_cost_multiplier'],
            'round': self.round_number - self.session.config['num_training_rounds'] - 1,
        }

    timer_text = "Waktu yang tersisa di halaman ini:"

    def get_timeout_seconds(self):
        return self.group.timeout

    def before_next_page(self):
        return self.player.payoff_vector_storage()


class  ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        pass
        #self.subsession.supplement()

    title_text = "Mohon menunggu:"
    body_text = "Menunggu peserta lainnya..."



page_sequence = [
    Introduction,
    IntroWaitPage,
    RealGameWarning,
    InitialWaitPage,
    Contribute,
    ContributionWaitPage,
    Embezzlement,
    Bribe,
    PostWaitPage,
    Results,
    ResultsWaitPage
]