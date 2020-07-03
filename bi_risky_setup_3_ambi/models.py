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
    setup_name = 'Partial Uncertainty - One Good'
    name_in_url = 'experiment_3'
    players_per_group = None
    num_rounds = 12
    num_training_rounds = 2
    endowment = c(25)
    endo = 25


class Subsession(BaseSubsession):

    training_round = models.BooleanField()
    x1G = models.FloatField()
    x2G = models.FloatField()

    def parameter_set(self):
        for p in self.get_players():
            p.endowment = Constants.endo
        x1Gs_training = [1.5, 2]
        x2Gs_training = [0.5, 0.4]
        x1Gs = [1.5, 2, 2.5, 3, 3.5, 1.5, 2, 2.5, 3, 3.5]
        x2Gs = [0.5, 0.4, 0.3, 0.2, 0.1, 0.5, 0.4, 0.3, 0.2, 0.1]
        if self.round_number <= Constants.num_training_rounds:
            self.x1G = x1Gs_training[self.round_number - 1]
            self.x2G = x2Gs_training[self.round_number - 1]
            self.training_round = True
        elif self.round_number > Constants.num_training_rounds:
            self.x1G = x1Gs[self.round_number - (1+Constants.num_training_rounds)]
            self.x2G = x2Gs[self.round_number - (1+Constants.num_training_rounds)]
            self.training_round = False

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
                   p.a9]
            prob = np.linspace(0,0.8,9)
            p.selector_index = random.randint(1,9)
            p.selected_a = seq[p.selector_index-1]
            p.unknown_prob = round(np.random.choice(np.linspace(0,0.2,100)),3)
            r = random.randint(1, 9) - 1
            p.selected_xG = np.random.choice([self.x1G, self.x2G],
                                             p=[prob[r] + p.unknown_prob,
                                                0.8 - prob[r] + (0.2 - p.unknown_prob)])
            p.payoff = (p.selected_a * p.selected_xG) + (Constants.endowment - p.selected_a)
            if self.round_number <= Constants.num_training_rounds:
                pass
            elif self.round_number > Constants.num_training_rounds:
                p.participant.vars['payoff_vector_s1'].append(p.payoff)
                p.participant.vars['game_type'].append(Constants.setup_name)
                p.participant.vars['MPL_selector_index'].append(p.selector_index)
                p.participant.vars["Choice_selection_G"].append(p.selected_a)
                p.participant.vars["Choice_selection_B"].append("N/A")
                p.participant.vars["xG_select"].append(p.selected_xG)
                p.participant.vars["xB_select"].append("N/A")
                p.participant.vars["unknown_prob_G"].append(p.unknown_prob)
                p.participant.vars["unknown_prob_B"].append(0)

class Group(BaseGroup):
    pass

class Player(BasePlayer):

    endowment = models.IntegerField()
    selected_a = models.IntegerField()
    selected_xG = models.FloatField()
    selector_index = models.IntegerField()
    unknown_prob = models.FloatField()

    a1 = models.IntegerField(min=0, max=Constants.endowment, label="")
    a2 = models.IntegerField(min=0, max=Constants.endowment, label="")
    a3 = models.IntegerField(min=0, max=Constants.endowment, label="")
    a4 = models.IntegerField(min=0, max=Constants.endowment, label="")
    a5 = models.IntegerField(min=0, max=Constants.endowment, label="")
    a6 = models.IntegerField(min=0, max=Constants.endowment, label="")
    a7 = models.IntegerField(min=0, max=Constants.endowment, label="")
    a8 = models.IntegerField(min=0, max=Constants.endowment, label="")
    a9 = models.IntegerField(min=0, max=Constants.endowment, label="")