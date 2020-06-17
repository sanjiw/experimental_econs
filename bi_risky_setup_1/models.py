from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
import numpy as np
import random


author = 'Putu Sanjiwacika Wibisana'

doc = """
Risky Setup - Green Only
"""


class Constants(BaseConstants):
    name_in_url = 'experiment_1'
    players_per_group = None
    num_rounds = 10
    endowment = c(25)


class Subsession(BaseSubsession):

    x1G = models.FloatField()
    x2G = models.FloatField()

    def parameter_set(self):
        x1Gs = [1.5, 2, 2.5, 3, 3.5, 1.5, 2, 2.5, 3, 3.5]
        x2Gs = [0.5, 0.4, 0.3, 0.2, 0.1, 0.5, 0.4, 0.3, 0.2, 0.1]
        self.x1G = x1Gs[self.round_number-1]
        self.x2G = x2Gs[self.round_number-1]

    def payoff_realization(self):
        for p in self.get_players():
            seq = [p.a1,
                   p.a2,
                   p.a3,
                   p.a4,
                   p.a5,
                   p.a6,
                   p.a7,
                   p.a8,
                   p.a9,
                   p.a10,
                   p.a11]
            prob = np.linspace(0,1,11)
            choice_randomizer = random.randint(1,11)
            p.selector = choice_randomizer
            p.a_select = seq[choice_randomizer-1]
            p.xG_select = np.random.choice([self.x1G, self.x2G],
                                         p=[prob[choice_randomizer-1], 1-prob[choice_randomizer-1]])
            p.payoff = (p.a_select * p.xG_select) + (Constants.endowment - p.a_select)

class Group(BaseGroup):
    pass


class Player(BasePlayer):

    a_select = models.IntegerField()
    xG_select = models.FloatField()
    selector = models.IntegerField()

    a1 = models.IntegerField(min=0, max=Constants.endowment, label="")
    a2 = models.IntegerField(min=0, max=Constants.endowment, label="")
    a3 = models.IntegerField(min=0, max=Constants.endowment, label="")
    a4 = models.IntegerField(min=0, max=Constants.endowment, label="")
    a5 = models.IntegerField(min=0, max=Constants.endowment, label="")
    a6 = models.IntegerField(min=0, max=Constants.endowment, label="")
    a7 = models.IntegerField(min=0, max=Constants.endowment, label="")
    a8 = models.IntegerField(min=0, max=Constants.endowment, label="")
    a9 = models.IntegerField(min=0, max=Constants.endowment, label="")
    a10 = models.IntegerField(min=0, max=Constants.endowment, label="")
    a11 = models.IntegerField(min=0, max=Constants.endowment, label="")