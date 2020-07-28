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
            if p.participant.vars["p_app_sequence"]['game_type'][self.round_number-1] == "risky_setup_1":
                seq = [p.a1, p.a2, p.a3, p.a4, p.a5, p.a6, p.a7, p.a8, p.a9, p.a10, p.a11]
                p.participant.vars['decision_list'].append(seq)
            elif p.participant.vars["p_app_sequence"]['game_type'][self.round_number-1]== "risky_setup_3_ambi":
                seq = [p.a1, p.a2, p.a3, p.a4, p.a5, p.a6, p.a7, p.a8, p.a9]
                p.participant.vars['decision_list'].append(seq)
            elif p.participant.vars["p_app_sequence"]['game_type'][self.round_number-1] == "risky_setup_2":
                seq = [[p.a1, p.b1], [p.a2, p.b2], [p.a3, p.b3], [p.a4, p.b4], [p.a5, p.b5], [p.a6, p.b6],
                       [p.a7, p.b7], [p.a8, p.b8], [p.a9, p.b9], [p.a10, p.b10], [p.a11, p.b11]]
                p.participant.vars['decision_list'].append(seq)
            elif p.participant.vars["p_app_sequence"]['game_type'][self.round_number - 1] == "risky_setup_4_ambi":
                seq = [[p.a1, p.b1], [p.a2, p.b2], [p.a3, p.b3], [p.a4, p.b4], [p.a5, p.b5], [p.a6, p.b6],
                       [p.a7, p.b7], [p.a8, p.b8], [p.a9, p.b9]]
                p.participant.vars['decision_list'].append(seq)

class Group(BaseGroup):
    pass


class Player(BasePlayer):

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
