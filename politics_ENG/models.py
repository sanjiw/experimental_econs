import random
import math
import numpy as np
from scipy import stats

from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range,
)

author = 'Putu Sanjiwacika Wibisana - Erasmus Universiteit Rotterdam'

doc = """Political Polarization"""


class Constants(BaseConstants):
    name_in_url = 'politics_ENG'
    players_per_group = None
    num_rounds = 1

    vignette = 'politics_ENG/Vignette.html'

    # payoff for a voter which supported candidate won
    payoff_win = 40
    payoff_impeach = 15
    payoff_lost = 0
    endowment = 40
    accuracy_multiplier = 50

    # exogenous probabilities
    p_guilty = 0.5
    p_impeach = 0.7
    p_good_person = 0.5
    p_good_outlet = 0.8
    p_bad_outlet = 0.5


class Subsession(BaseSubsession):

    def creating_session(self):
        for p in self.get_players():
            p.able_to_vote = self.session.config['treatment']

    total_vote_a = models.IntegerField()
    total_vote_b = models.IntegerField()
    winning_cand = models.StringField()

    def preference_setting(self):
        for p in self.get_players():
            pref_space = ['A', 'B']
            if p.id_in_group % 2 == 0:
                p.preferences = 'A'
            elif p.id_in_group % 2 != 0:
                p.preferences = 'B'

    def winner(self):
        for p in self.get_players():
            winner_space = ['A', 'B']
            if p.able_to_vote == 'yes':
                self.total_vote_a = [p.ballot for p in self.get_players()].count('A')
                self.total_vote_b = [p.ballot for p in self.get_players()].count('B')
                if self.total_vote_a > self.total_vote_b:
                    self.winning_cand = 'A'
                elif self.total_vote_a < self.total_vote_b:
                    self.winning_cand = 'B'
                elif self.total_vote_a == self.total_vote_b:
                    self.winning_cand = random.choice(winner_space)
            elif p.able_to_vote == 'no':
                self.winning_cand = random.choice(winner_space)

    prob_impeach = models.FloatField()
    d_impeach = models.BooleanField()
    d_bayes_prob = models.FloatField()

    def scoring_rules(self):
        self.d_bayes_prob = (float(Constants.p_impeach * Constants.p_good_outlet) / float(
                (Constants.p_impeach * Constants.p_good_outlet) + (
                float(1 - Constants.p_impeach) * float(1 - Constants.p_good_outlet))))
        for p in self.get_players():
            p.accuracy_score = Constants.accuracy_multiplier * (1/(abs(float(p.accuracy_est/100) - self.d_bayes_prob)*20+1))

    def payoff_rules(self):
        self.prob_impeach = (Constants.p_good_person * Constants.p_impeach) / (
                (Constants.p_good_person * Constants.p_impeach) + (
                    (1 - Constants.p_good_person) * (1 - Constants.p_impeach)))
        self.d_impeach = np.random.choice([True, False], p=[self.prob_impeach, 1 - self.prob_impeach])
        for p in self.get_players():
            if p.preferences == self.winning_cand and self.d_impeach == False:
                p.payoff_from_voting = Constants.payoff_win
                p.payoff = Constants.endowment + Constants.payoff_win + p.accuracy_score
            elif p.preferences == self.winning_cand and self.d_impeach == True:
                p.payoff_from_voting = Constants.payoff_impeach
                p.payoff = Constants.endowment + Constants.payoff_impeach + p.accuracy_score
            elif p.preferences != self.winning_cand and self.d_impeach == False:
                p.payoff_from_voting = Constants.payoff_lost
                p.payoff = Constants.endowment + Constants.payoff_lost + p.accuracy_score
            elif p.preferences != self.winning_cand and self.d_impeach == True:
                p.payoff_from_voting = Constants.payoff_impeach
                p.payoff = Constants.endowment + Constants.payoff_impeach + p.accuracy_score


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    preferences = models.StringField()
    able_to_vote = models.StringField()
    accuracy_score = models.FloatField()
    payoff_from_voting = models.IntegerField()

    ballot = models.StringField(
        choices=['A', 'B'],
        widget=widgets.RadioSelectHorizontal
    )

    opinion = models.IntegerField(initial=50, max=100,
                                  min=0,
                                  widget=widgets.Slider)
    accuracy_est = models.IntegerField(initial=0, max=100,
                                            min=0,
                                            widget=widgets.Slider)
