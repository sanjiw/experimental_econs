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
import pandas as pd

author = 'Putu Sanjiwacika Wibisana'

doc = """
Ambiguity Setup - Green and Brown
"""

class Constants(BaseConstants):
    setup_name = 'Partial Uncertainty - Two Goods'
    name_in_url = 'experiment_4'
    players_per_group = None
    num_rounds = 12
    num_training_rounds = 2
    endowment = c(25)
    endo = 25
    with open('bi_introduction_simple/Params.csv') as file:
        params = pd.read_csv(file)


class Subsession(BaseSubsession):

    training_round = models.BooleanField()
    x1G = models.FloatField()
    x2G = models.FloatField()
    unknown_prob_G = models.FloatField()
    x1B = models.FloatField()
    x2B = models.FloatField()
    unknown_prob_B = models.FloatField()
    t1G = models.IntegerField()
    t2G = models.IntegerField()
    t1B = models.IntegerField()
    t2B = models.IntegerField()

    def parameter_set(self):
        for p in self.get_players():
            p.endowment = Constants.endo
            if p.session.config["treatment_group"] == 3:
                p.participant.vars["random_image_url"] = 'bi_experiment/t3/jogja' + str(random.randint(1, 4)) + ".jpg"
            elif p.session.config["treatment_group"] == 4:
                p.participant.vars["random_image_url"] = 'bi_experiment/t4/netral' + str(random.randint(1, 4)) + ".jpeg"
            else:
                p.participant.vars["random_image_url"] = "None"
        params = Constants.params
        params_subgame = params[params['game_type'] == "risky_setup_4_ambi"]
        x1Gs_training = [1.5, 2]
        x2Gs_training = [0.5, 0.4]
        t1Gs_training = [1, 2]
        t2Gs_training = [2, 1]
        unknown_prob_Gs = [float(i) for i in list(params_subgame['unknown_prob_G'])]
        x1Bs_training = [1.6, 2.1]
        x2Bs_training = [0.4, 0.3]
        t1Bs_training = [1, 2]
        t2Bs_training = [2, 1]
        unknown_prob_Bs = [float(i) for i in list(params_subgame['unknown_prob_B'])]
        x1Gs = list(params_subgame['x1G'])
        x2Gs = list(params_subgame['x2G'])
        t1Gs = list(params_subgame['t1G'])
        t2Gs = list(params_subgame['t2G'])
        x1Bs = [float(i) for i in list(params_subgame['x1B'])]
        x2Bs = [float(i) for i in list(params_subgame['x2B'])]
        t1Bs = [int(i) for i in list(params_subgame['t1B'])]
        t2Bs = [int(i) for i in list(params_subgame['t2B'])]
        if self.round_number <= Constants.num_training_rounds:
            self.x1G = x1Gs_training[self.round_number - 1]
            self.x2G = x2Gs_training[self.round_number - 1]
            self.x1B = x1Bs_training[self.round_number - 1]
            self.x2B = x2Bs_training[self.round_number - 1]
            self.t1G = t1Gs_training[self.round_number - 1]
            self.t2G = t2Gs_training[self.round_number - 1]
            self.t1B = t1Bs_training[self.round_number - 1]
            self.t2B = t2Bs_training[self.round_number - 1]
            self.unknown_prob_G = unknown_prob_Gs[self.round_number - 1]
            self.unknown_prob_B = unknown_prob_Bs[self.round_number - 1]
            self.training_round = True
        elif self.round_number > Constants.num_training_rounds:
            self.x1G = x1Gs[self.round_number - (1 + Constants.num_training_rounds)]
            self.x2G = x2Gs[self.round_number - (1 + Constants.num_training_rounds)]
            self.x1B = x1Bs[self.round_number - (1 + Constants.num_training_rounds)]
            self.x2B = x2Bs[self.round_number - (1 + Constants.num_training_rounds)]
            self.t1G = t1Gs[self.round_number - (1 + Constants.num_training_rounds)]
            self.t2G = t2Gs[self.round_number - (1 + Constants.num_training_rounds)]
            self.t1B = t1Bs[self.round_number - (1 + Constants.num_training_rounds)]
            self.t2B = t2Bs[self.round_number - (1 + Constants.num_training_rounds)]
            self.unknown_prob_G = unknown_prob_Gs[self.round_number - (1 + Constants.num_training_rounds)]
            self.unknown_prob_B = unknown_prob_Bs[self.round_number - (1 + Constants.num_training_rounds)]
            self.training_round = False

    def realization(self):
        for p in self.get_players():
            seq = [[p.a1,p.b1],
                   [p.a2,p.b2],
                   [p.a3,p.b3],
                   [p.a4,p.b4],
                   [p.a5,p.b5],
                   [p.a6,p.b6],
                   [p.a7,p.b7],
                   [p.a8,p.b8],
                   [p.a9,p.b9]]
            if self.round_number <= Constants.num_training_rounds:
                pass
            elif self.round_number > Constants.num_training_rounds:
                p.participant.vars['decision_list'].append(seq)
                p.participant.vars['game_type'].append("risky_setup_4_ambi")
                p.participant.vars['x1G'].append(self.x1G)
                p.participant.vars['x2G'].append(self.x2G)
                p.participant.vars['unknown_prob_G'].append(self.unknown_prob_G)
                p.participant.vars['x1B'].append(self.x1B)
                p.participant.vars['x2B'].append(self.x2B)
                p.participant.vars['unknown_prob_B'].append(self.unknown_prob_B)
                p.participant.vars['t1G'].append(self.t1G)
                p.participant.vars['t2G'].append(self.t2G)
                p.participant.vars['t1B'].append(self.t1B)
                p.participant.vars['t2B'].append(self.t2B)

class Group(BaseGroup):
    pass

class Player(BasePlayer):

    endowment = models.IntegerField()

    a1 = models.IntegerField(min=0, max=Constants.endowment, label="")
    a2 = models.IntegerField(min=0, max=Constants.endowment, label="")
    a3 = models.IntegerField(min=0, max=Constants.endowment, label="")
    a4 = models.IntegerField(min=0, max=Constants.endowment, label="")
    a5 = models.IntegerField(min=0, max=Constants.endowment, label="")
    a6 = models.IntegerField(min=0, max=Constants.endowment, label="")
    a7 = models.IntegerField(min=0, max=Constants.endowment, label="")
    a8 = models.IntegerField(min=0, max=Constants.endowment, label="")
    a9 = models.IntegerField(min=0, max=Constants.endowment, label="")

    b1 = models.IntegerField(min=0, max=Constants.endowment, label="")
    b2 = models.IntegerField(min=0, max=Constants.endowment, label="")
    b3 = models.IntegerField(min=0, max=Constants.endowment, label="")
    b4 = models.IntegerField(min=0, max=Constants.endowment, label="")
    b5 = models.IntegerField(min=0, max=Constants.endowment, label="")
    b6 = models.IntegerField(min=0, max=Constants.endowment, label="")
    b7 = models.IntegerField(min=0, max=Constants.endowment, label="")
    b8 = models.IntegerField(min=0, max=Constants.endowment, label="")
    b9 = models.IntegerField(min=0, max=Constants.endowment, label="")