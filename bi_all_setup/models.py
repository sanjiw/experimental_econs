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

    training_round = models.BooleanField()

    def sequence_setup(self):
        for p in self.get_players():
            set1 = Constants.params[Constants.params['game_type'] == "risky_setup_1"]
            set2 = Constants.params[Constants.params['game_type'] == "risky_setup_2"]
            set3 = Constants.params[Constants.params['game_type'] == "risky_setup_3_ambi"]
            set4 = Constants.params[Constants.params['game_type'] == "risky_setup_4_ambi"]
            orgnl_sequence = [set1, set2, set3, set4]
            player_sequence = random.sample(orgnl_sequence, len(orgnl_sequence))
            player_params = player_sequence[0].append(player_sequence[1], ignore_index = True).append(player_sequence[2], ignore_index = True).append(player_sequence[3],ignore_index = True)
            image_urls = []
            if self.session.config["treatment_group"] == 3:
                image_urls = ['bi_experiment/t3/jogja' + str(i) + ".jpg" for i in [1, 2, 3, 4]]
            elif self.session.config["treatment_group"] == 4:
                image_urls = ['bi_experiment/t4/netral' + str(i) + ".jpeg" for i in [1, 2, 3, 4]]
            player_params['random_image_urls'] = random.choices(image_urls, k=48)
            player_params['treatment_group'] = [self.session.config["treatment_group"]] * 48
            p.participant.vars["p_app_sequence"] = player_params                                                        # Contains the dataframe for all parameters for all players

    def decision_record(self):
        for p in self.get_players():
            p.game_type         = p.participant.vars["p_app_sequence"]['game_type'][self.round_number-1]
            p.x1G               = p.participant.vars["p_app_sequence"]['x1G'][self.round_number-1]
            p.x2G               = p.participant.vars["p_app_sequence"]['x2G'][self.round_number-1]
            p.unknown_prob_G    = p.participant.vars["p_app_sequence"]['unknown_prob_G'][self.round_number-1]
            p.t1G               = p.participant.vars["p_app_sequence"]['t1G'][self.round_number-1]
            p.t2G               = p.participant.vars["p_app_sequence"]['t2G'][self.round_number-1]
            p.x1B               = p.participant.vars["p_app_sequence"]['x1B'][self.round_number-1]
            p.x2B               = p.participant.vars["p_app_sequence"]['x2B'][self.round_number-1]
            p.unknown_prob_B    = p.participant.vars["p_app_sequence"]['unknown_prob_B'][self.round_number-1]
            p.t1B               = p.participant.vars["p_app_sequence"]['t1B'][self.round_number-1]
            p.t2B               = p.participant.vars["p_app_sequence"]['t2B'][self.round_number-1]


class Group(BaseGroup):
    pass


class Player(BasePlayer):

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


    a1 = models.IntegerField(min=0, max=Constants.endowment, label="", initial=3)
    a2 = models.IntegerField(min=0, max=Constants.endowment, label="", initial=3)
    a3 = models.IntegerField(min=0, max=Constants.endowment, label="", initial=3)
    a4 = models.IntegerField(min=0, max=Constants.endowment, label="", initial=3)
    a5 = models.IntegerField(min=0, max=Constants.endowment, label="", initial=3)
    a6 = models.IntegerField(min=0, max=Constants.endowment, label="", initial=3)
    a7 = models.IntegerField(min=0, max=Constants.endowment, label="", initial=3)
    a8 = models.IntegerField(min=0, max=Constants.endowment, label="", initial=3)
    a9 = models.IntegerField(min=0, max=Constants.endowment, label="", initial=3)
    a10 = models.IntegerField(min=0, max=Constants.endowment, label="", initial=3)
    a11 = models.IntegerField(min=0, max=Constants.endowment, label="", initial=3)

    b1 = models.IntegerField(min=0, max=Constants.endowment, label="", initial=3)
    b2 = models.IntegerField(min=0, max=Constants.endowment, label="", initial=3)
    b3 = models.IntegerField(min=0, max=Constants.endowment, label="", initial=3)
    b4 = models.IntegerField(min=0, max=Constants.endowment, label="", initial=3)
    b5 = models.IntegerField(min=0, max=Constants.endowment, label="", initial=3)
    b6 = models.IntegerField(min=0, max=Constants.endowment, label="", initial=3)
    b7 = models.IntegerField(min=0, max=Constants.endowment, label="", initial=3)
    b8 = models.IntegerField(min=0, max=Constants.endowment, label="", initial=3)
    b9 = models.IntegerField(min=0, max=Constants.endowment, label="", initial=3)
    b10 = models.IntegerField(min=0, max=Constants.endowment, label="", initial=3)
    b11 = models.IntegerField(min=0, max=Constants.endowment, label="", initial=3)

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
