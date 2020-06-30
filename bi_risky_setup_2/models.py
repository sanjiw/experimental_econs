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
Risky Setup - Green and Brown
"""

class Constants(BaseConstants):
    setup_name = 'Risky - Two Goods'
    name_in_url = 'experiment_2'
    players_per_group = None
    num_rounds = 12
    num_training_rounds = 2
    endowment = c(25)
    endo = 25


class Subsession(BaseSubsession):

    training_round = models.BooleanField()
    x1G = models.FloatField()
    x2G = models.FloatField()
    x1B = models.FloatField()
    x2B = models.FloatField()

    def parameter_set(self):
        for p in self.get_players():
            p.endowment = Constants.endo
        x1Gs_training = [1.5, 2]
        x2Gs_training = [0.5, 0.4]
        x1Bs_training = [1.6, 2.1]
        x2Bs_training = [0.4, 0.3]
        x1Gs = [1.5, 2, 2.5, 3, 3.5, 1.5, 2, 2.5, 3, 3.5]
        x2Gs = [0.5, 0.4, 0.3, 0.2, 0.1, 0.5, 0.4, 0.3, 0.2, 0.1]
        x1Bs = [1.6, 2.1, 2.6, 3.1, 3.6, 1.6, 2.1, 2.6, 3.1, 3.6]
        x2Bs = [0.4, 0.3, 0.2, 0.1, 0.0, 0.4, 0.3, 0.2, 0.1, 0.0]
        if self.round_number <= Constants.num_training_rounds:
            self.x1G = x1Gs_training[self.round_number - 1]
            self.x2G = x2Gs_training[self.round_number - 1]
            self.x1B = x1Bs_training[self.round_number - 1]
            self.x2B = x2Bs_training[self.round_number - 1]
            self.training_round = True
        elif self.round_number > Constants.num_training_rounds:
            self.x1G = x1Gs[self.round_number - (1+Constants.num_training_rounds)]
            self.x2G = x2Gs[self.round_number - (1+Constants.num_training_rounds)]
            self.x1B = x1Bs[self.round_number - (1 + Constants.num_training_rounds)]
            self.x2B = x2Bs[self.round_number - (1 + Constants.num_training_rounds)]
            self.training_round = False

    def payoff_realization(self):
        for p in self.get_players():
            seq = [[p.a1,p.b1],
                   [p.a2,p.b2],
                   [p.a3,p.b3],
                   [p.a4,p.b4],
                   [p.a5,p.b5],
                   [p.a6,p.b6],
                   [p.a7,p.b7],
                   [p.a8,p.b8],
                   [p.a9,p.b9],
                   [p.a10,p.b10],
                   [p.a11,p.b11]]
            prob = np.linspace(0,1,11)
            choice_randomizer = random.randint(1,11)
            p.selector = choice_randomizer
            choice_selection = seq[choice_randomizer-1]
            p.choice_selection_G = choice_selection[0]
            p.choice_selection_B = choice_selection[1]
            p.xG_select = np.random.choice([self.x1G, self.x2G],
                                         p=[prob[choice_randomizer-1], 1-prob[choice_randomizer-1]])
            p.xB_select = np.random.choice([self.x1B, self.x2B],
                                         p=[prob[choice_randomizer-1], 1-prob[choice_randomizer-1]])
            p.payoff = (choice_selection[0] * p.xG_select) + \
                       (choice_selection[1] * p.xB_select) + \
                       (Constants.endowment - (sum(choice_selection)))
            if self.round_number <= Constants.num_training_rounds:
                pass
            elif self.round_number > Constants.num_training_rounds:
                p.participant.vars['payoff_vector_s1'].append(p.payoff)
                p.participant.vars['game_type'].append(Constants.setup_name)

class Group(BaseGroup):
    pass

class Player(BasePlayer):

    endowment = models.IntegerField()
    choice_selection_G = models.IntegerField()
    choice_selection_B = models.IntegerField()
    xG_select = models.FloatField()
    xB_select = models.FloatField()
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

    b1 = models.IntegerField(min=0, max=Constants.endowment, label="")
    b2 = models.IntegerField(min=0, max=Constants.endowment, label="")
    b3 = models.IntegerField(min=0, max=Constants.endowment, label="")
    b4 = models.IntegerField(min=0, max=Constants.endowment, label="")
    b5 = models.IntegerField(min=0, max=Constants.endowment, label="")
    b6 = models.IntegerField(min=0, max=Constants.endowment, label="")
    b7 = models.IntegerField(min=0, max=Constants.endowment, label="")
    b8 = models.IntegerField(min=0, max=Constants.endowment, label="")
    b9 = models.IntegerField(min=0, max=Constants.endowment, label="")
    b10 = models.IntegerField(min=0, max=Constants.endowment, label="")
    b11 = models.IntegerField(min=0, max=Constants.endowment, label="")