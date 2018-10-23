from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import numpy as np
from random import shuffle

doc = """
Bribery Game dengan 4 pemain
"""

class Constants(BaseConstants):
    name_in_url = 'Eksperimen_Penyuapan'
    players_per_group = 3
    num_rounds = 3

    instructions_template = 'bribery_game_arya/Instructions.html'

    endowment = c(40)
    # multiplier= [0.5, 0.5, 0.5, 0.5, 0.5, 0.6, 0.6, 0.6, 0.6, 0.6, 0.7, 0.7, 0.7, 0.7, 0.7, 0.75, 0.75, 0.75,
    #               0.75, 0.75]
    multiplier = 0.5

class Subsession(BaseSubsession):
    def vars_for_admin_report(self):
        contributions = [p.contribution for p in self.get_players() if p.contribution != None]
        if contributions:
            return {
                'avg_contribution': sum(contributions)/len(contributions),
                'min_contribution': min(contributions),
                'max_contribution': max(contributions),
            }
        else:
            return {
                'avg_contribution': '(no data)',
                'min_contribution': '(no data)',
                'max_contribution': '(no data)',
            }

def creating_session(self):
    # matrix = [[5, 24, 10], [6, 3, 22], [13, 21, 4], [19, 7, 17], [18, 26, 23], [2, 16, 27], [8, 11, 1], [12, 20, 25], [14, 25, 9]]
    matrix = [[1, 2, 3]]
    self.set_group_matrix(matrix)
    self.get_group_matrix()


def make_field(amount):
    return models.BooleanField(
        widget=widgets.RadioSelectHorizontal,
        label='Would you accept an offer of {}?'.format(c(amount)))

class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()
    bribe_value1 = models.CurrencyField(min=0)
    bribe_value2 = models.CurrencyField(min=0)
    bribe_value_player1 = models.CurrencyField()
    bribe_ratio = models.FloatField()
    bribe_accepted = models.BooleanField()
    amount_left = models.CurrencyField()
    offer = models.StringField()

    # def multi(self):
    #     self.multiplier = Constants.multiplier_choice[self.round_number - 1]
    #     print(self.multiplier)

    def set_payoffs1(self):
        self.total_contribution = sum([p.contribution for p in self.get_players()])

    def set_payoffs2(self):
        self.bribe_ratio = float(self.bribe_value2)/float(self.bribe_value1)
        self.bribe_value_player1 = self.bribe_value1 - self.bribe_value2

    def set_payoffs3(self):
        self.individual_share = self.total_contribution * Constants.multiplier
        self.amount_left = Constants.multiplier * (self.total_contribution - self.bribe_value1)

        if self.bribe_ratio >= 0.28:
            self.bribe_accepted = True
        else:
            self.bribe_accepted = False

        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p3 = self.get_player_by_id(3)

        for p in self.get_players():
            if self.bribe_accepted is True:
                p1.payoff = (Constants.endowment - p1.contribution) + (self.bribe_value1 - self.bribe_value2) + self.amount_left
                p2.payoff = (Constants.endowment - p2.contribution) + self.amount_left
                p3.payoff = (Constants.endowment - p3.contribution) + self.amount_left
            else:
                p.payoff = (Constants.endowment - p.contribution) + self.individual_share

        if self.bribe_accepted == True:
            self.offer = 'Pihak ketiga menerima bagian kontribusi yang sudah ditawarkan'
        else:
            self.offer = 'Pihak ketiga menolak bagian kontribusi yang sudah ditawarkan'

class Player(BasePlayer):
    is_m = models.BooleanField()
    endowment = models.IntegerField()
    partners = models.StringField(default='')

    def set_bonus(self):
        players = self.get_players()
        for p in players:
            p.cumulative_payoff = sum([p.payoff for p in players.in_all_rounds()])
    choice = models.StringField(
        widget=widgets.RadioSelect,
        choices=['25% dari poin awal', '20% dari poin awal', '15% dari poin awal', '10% dari poin awal',
                 '5% dari poin awal']
    )
    contribution = models.CurrencyField()

    def set_contribute(self):
        if self.choice == '25% dari poin awal':
            self.contribution = 0.25 * Constants.endowment
        elif self.choice == '20% dari poin awal':
            self.contribution = 0.20 * Constants.endowment
        elif self.choice == '15% dari poin awal':
            self.contribution = 0.15 * Constants.endowment
        elif self.choice == '10% dari poin awal':
            self.contribution = 0.10 * Constants.endowment
        else:
            self.contribution = 0.05 * Constants.endowment

    def role(self):
        if self.id_in_group == 1:
            return 'Player1'
        elif self.id_in_group == 2:
            return 'Player2'
        else:
            return 'Player3'
