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
    with open('bi_introduction_simple/Params.csv') as file:
        params = pd.read_csv(file)


class Subsession(BaseSubsession):

    training_round = models.BooleanField()
    x1G = models.FloatField()
    x2G = models.FloatField()
    t1G = models.IntegerField()
    t2G = models.IntegerField()
    unknown_prob_G = models.FloatField()

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
        params_subgame = params[params['game_type'] == "risky_setup_3_ambi"]
        x1Gs_training = [1.5, 2]
        x2Gs_training = [0.5, 0.4]
        t1Gs_training = [1, 2]
        t2Gs_training = [2, 1]
        x1Gs = list(params_subgame['x1G'])
        x2Gs = list(params_subgame['x2G'])
        t1Gs = list(params_subgame['t1G'])
        t2Gs = list(params_subgame['t2G'])
        unknown_prob_Gs = [float(i) for i in list(params_subgame['unknown_prob_G'])]
        if self.round_number <= Constants.num_training_rounds:
            self.x1G = x1Gs_training[self.round_number - 1]
            self.x2G = x2Gs_training[self.round_number - 1]
            self.t1G = t1Gs_training[self.round_number - 1]
            self.t2G = t2Gs_training[self.round_number - 1]
            self.unknown_prob_G = unknown_prob_Gs[self.round_number - 1]
            self.training_round = True
        elif self.round_number > Constants.num_training_rounds:
            self.x1G = x1Gs[self.round_number - (1 + Constants.num_training_rounds)]
            self.x2G = x2Gs[self.round_number - (1 + Constants.num_training_rounds)]
            self.t1G = t1Gs[self.round_number - (1 + Constants.num_training_rounds)]
            self.t2G = t2Gs[self.round_number - (1 + Constants.num_training_rounds)]
            self.unknown_prob_G = unknown_prob_Gs[self.round_number - (1 + Constants.num_training_rounds)]
            self.training_round = False

    def realization(self):
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
            if self.round_number <= Constants.num_training_rounds:
                pass
            elif self.round_number > Constants.num_training_rounds:
                p.participant.vars['decision_list'].append(seq)
                p.participant.vars['game_type'].append("risky_setup_3_ambi")
                p.participant.vars['x1G'].append(self.x1G)
                p.participant.vars['x2G'].append(self.x2G)
                p.participant.vars['unknown_prob_G'].append(self.unknown_prob_G)
                p.participant.vars['x1B'].append("N/A")
                p.participant.vars['x2B'].append("N/A")
                p.participant.vars['unknown_prob_B'].append("N/A")
                p.participant.vars['t1G'].append(self.t1G)
                p.participant.vars['t2G'].append(self.t2G)
                p.participant.vars['t1B'].append("N/A")
                p.participant.vars['t2B'].append("N/A")

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