from ._builtin import Page, WaitPage
from .models import Constants, Player, Group
from otree.api import (Currency as c)
import random


class Introduction(Page):
    """ Description of the game: How to play and returns expected"""
    pass

class Contribution(Page):
    """ How much the player contribute toward mutual project"""
    form_model = 'player'
    form_fields = ['choice']

    def before_next_page(self):
        self.player.set_contribute()


class Contributionwaitpage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs1()

    body_text = "Waiting for the other participants to contribute"


class Setbribery(Page):
    """ Defining the amount of the bribery offer to receiver"""
    form_model = 'group'
    form_fields = ['bribe_value1']

    def bribe_value1_max(self):
        return self.group.total_contribution

    def is_displayed(self):
        return self.player.id_in_group == 1

class Offerbribery(Page):
    form_model = 'group'
    form_fields = ['bribe_value2']

    def bribe_value2_max(self):
        return self.group.bribe_value1

    def is_displayed(self):
        return self.player.id_in_group == 1

class Offer_wait_page(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs2()

class Offeracceptedwaitpage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs3()
    body_text = "Waiting for the other participants to contribute"


class Results(Page):
    """Players payoff: How much each has earned"""
    pass


page_sequence = [
    Introduction,
    Contribution,
    Contributionwaitpage,
    Setbribery,
    Offerbribery,
    Offer_wait_page,
    Offeracceptedwaitpage,
    Results
]