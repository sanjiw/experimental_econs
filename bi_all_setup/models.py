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
    setup_name = 'All Setup'
    name_in_url = 'experiment'
    players_per_group = None
    num_rounds = 48
    num_training_rounds = 8
    num_real_rounds_per_session = 10
    endowment = c(25)
    endo = 25
    with open('bi_introduction_simple/Params12.csv') as file:
        params = pd.read_csv(file)


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):

    def sequence_setup(self):
        set1 = Constants.params[Constants.params['game_type'] == "risky_setup_1"]
        set2 = Constants.params[Constants.params['game_type'] == "risky_setup_2"]
        set3 = Constants.params[Constants.params['game_type'] == "risky_setup_3_ambi"]
        set4 = Constants.params[Constants.params['game_type'] == "risky_setup_4_ambi"]
        orgnl_sequence = [set1, set2, set3, set4]
        player_sequence = random.sample(orgnl_sequence, len(orgnl_sequence))
        player_params = player_sequence[0].append(player_sequence[1], ignore_index=True).append(player_sequence[2],
                                                                                                ignore_index=True).append(
            player_sequence[3], ignore_index=True)
        image_urls = []
        if self.session.config["treatment_group"] == 1:
            image_urls = [""]
        elif self.session.config["treatment_group"] == 2:
            image_urls = [""]
        elif self.session.config["treatment_group"] == 3:
            image_urls = ['bi_experiment/t3/Jogja ' + str(i) + ".jpeg" for i in [1, 2, 3, 4]]
        elif self.session.config["treatment_group"] == 4:
            image_urls = ['bi_experiment/t4/Netral ' + str(i) + ".jpeg" for i in [1, 2, 3, 4]]
        player_params['random_image_urls'] = random.choices(image_urls, k=48)
        player_params['treatment_group'] = [self.session.config["treatment_group"]] * 48
        self.participant.vars[
            "p_app_sequence"] = player_params  # Contains the dataframe for all parameters for all players

    def decision_records(self):
        if self.participant.vars["p_app_sequence"]['game_type'][self.round_number-1] == "risky_setup_1":
            seq = [self.a1, self.a2, self.a3, self.a4, self.a5, self.a6, self.a7, self.a8, self.a9, self.a10, self.a11]
            self.participant.vars['decision_list'].append(seq)
        elif self.participant.vars["p_app_sequence"]['game_type'][self.round_number-1] == "risky_setup_3_ambi":
            seq = [self.a1, self.a2, self.a3, self.a4, self.a5, self.a6, self.a7, self.a8, self.a9]
            self.participant.vars['decision_list'].append(seq)
        elif self.participant.vars["p_app_sequence"]['game_type'][self.round_number-1] == "risky_setup_2":
            seq = [[self.a1, self.b1], [self.a2, self.b2], [self.a3, self.b3], [self.a4, self.b4], [self.a5, self.b5], [self.a6, self.b6],
                   [self.a7, self.b7], [self.a8, self.b8], [self.a9, self.b9], [self.a10, self.b10], [self.a11, self.b11]]
            self.participant.vars['decision_list'].append(seq)
        elif self.participant.vars["p_app_sequence"]['game_type'][self.round_number-1] == "risky_setup_4_ambi":
            seq = [[self.a1, self.b1], [self.a2, self.b2], [self.a3, self.b3], [self.a4, self.b4], [self.a5, self.b5], [self.a6, self.b6],
                   [self.a7, self.b7], [self.a8, self.b8], [self.a9, self.b9]]
            self.participant.vars['decision_list'].append(seq)

    def param_record(self):
        self.game_type = self.participant.vars["p_app_sequence"]['game_type'][self.round_number - 1]
        self.x1G = self.participant.vars["p_app_sequence"]['x1G'][self.round_number - 1]
        self.x2G = self.participant.vars["p_app_sequence"]['x2G'][self.round_number - 1]
        self.unknown_prob_G = self.participant.vars["p_app_sequence"]['unknown_prob_G'][self.round_number - 1]
        self.t1G = self.participant.vars["p_app_sequence"]['t1G'][self.round_number - 1]
        self.t2G = self.participant.vars["p_app_sequence"]['t2G'][self.round_number - 1]
        self.x1B = self.participant.vars["p_app_sequence"]['x1B'][self.round_number - 1]
        self.x2B = self.participant.vars["p_app_sequence"]['x2B'][self.round_number - 1]
        self.unknown_prob_B = self.participant.vars["p_app_sequence"]['unknown_prob_B'][self.round_number - 1]
        self.t1B = self.participant.vars["p_app_sequence"]['t1B'][self.round_number - 1]
        self.t2B = self.participant.vars["p_app_sequence"]['t2B'][self.round_number - 1]

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

    training = models.BooleanField()

    game_type = models.StringField()

    # keeping all the parameters for B
    x1G = models.FloatField()
    x2G = models.FloatField()
    unknown_prob_G = models.FloatField()
    t1G = models.IntegerField()
    t2G = models.IntegerField()

    # keeping all the parameters for B
    x1B = models.FloatField()
    x2B = models.FloatField()
    unknown_prob_B = models.FloatField()
    t1B = models.IntegerField()
    t2B = models.IntegerField()
