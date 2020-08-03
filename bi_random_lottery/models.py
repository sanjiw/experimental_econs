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
import csv
import pandas as pd

author = 'Putu Sanjiwacika Wibisana'

doc = """
Your app description
"""

class Constants(BaseConstants):
    name_in_url = 'bi_random_lottery'
    players_per_group = None
    quest_fee = 15000
    num_rounds = 1
    endo = 25
    with open('bi_random_lottery/Participant.csv') as PartsCsv:
        player_df = pd.read_csv(PartsCsv)
    with open('bi_postquestionnaire_simple/Ambiguity.csv') as csvFile:
        reader = csv.reader(csvFile)
        Ambiguous_list = [int(i) for i in next(reader)]
    participant_label = player_df.loc[0]["participant.label"]

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):

    participant_label = models.StringField(label="Masukkan kode peserta yang Anda gunakan tempo hari dalam eksperimen:")
    round_selector = models.IntegerField()
    decision_selector = models.IntegerField()
    unct_selector_G = models.IntegerField(initial=0)
    unct_selector_B = models.IntegerField(initial=0)
    urn_G = models.IntegerField()
    urn_B = models.IntegerField()
    xG_final = models.FloatField()
    xB_final = models.FloatField()
    tG_final = models.FloatField()
    tB_final = models.FloatField()
    payoff_A = models.FloatField()
    payoff_B = models.FloatField()
    payoff_now = models.FloatField()

    def payoff_dataframe(self):
        x = Constants.player_df.reset_index()
        self.participant.vars["player_dataframe"] = x.drop([0, 1, 12, 13, 24, 25, 36, 37]).reset_index()

    def round_selector_code(self):
        self.participant.vars["round_selected"] = self.participant.vars["player_dataframe"].loc[self.round_selector - 1]
        self.participant.vars["x1G_selected"] = self.participant.vars["round_selected"]["player.x1G"]
        self.participant.vars["x2G_selected"] = self.participant.vars["round_selected"]["player.x2G"]
        self.participant.vars["x1B_selected"] = self.participant.vars["round_selected"]["player.x1B"]
        self.participant.vars["x2B_selected"] = self.participant.vars["round_selected"]["player.x2B"]
        self.participant.vars["t1G_selected"] = self.participant.vars["round_selected"]["player.t1G"]
        self.participant.vars["t2G_selected"] = self.participant.vars["round_selected"]["player.t2G"]
        self.participant.vars["t1B_selected"] = self.participant.vars["round_selected"]["player.t1B"]
        self.participant.vars["t2B_selected"] = self.participant.vars["round_selected"]["player.t2B"]

    def decision_selector_code(self):
        x = self.participant.vars["round_selected"]
        if x["player.game_type"] == "risky_setup_1":
            self.participant.vars["allocated_G"] = x["player.a" + str(self.decision_selector)]
            self.participant.vars["threshold_G"] = list(range(0, 101, 10))[::-1][self.decision_selector - 1]
            self.participant.vars["allocated_B"] = 0
            self.participant.vars["threshold_B"] = 0
        elif x["player.game_type"] == "risky_setup_2":
            self.participant.vars["allocated_G"] = x["player.a" + str(self.decision_selector)]
            self.participant.vars["threshold_G"] = list(range(0, 81, 10))[::-1][self.decision_selector - 1]
            self.participant.vars["allocated_B"] = x["player.b" + str(self.decision_selector)]
            self.participant.vars["threshold_B"] = list(range(0, 81, 10))[::-1][self.decision_selector - 1]
        elif x["player.game_type"] == "risky_setup_3_ambi":
            self.participant.vars["allocated_G"] = x["player.a" + str(self.decision_selector)]
            self.participant.vars["threshold_G"] = list(range(0, 101, 10))[::-1][
                                                       self.decision_selector - 1] + self.unct_selector_G
            self.participant.vars["allocated_B"] = 0
            self.participant.vars["threshold_B"] = 0
        elif x["player.game_type"] == "risky_setup_4_ambi":
            self.participant.vars["allocated_G"] = x["player.a" + str(self.decision_selector)]
            self.participant.vars["threshold_G"] = list(range(0, 81, 10))[::-1][
                                                       self.decision_selector - 1] + self.unct_selector_G
            self.participant.vars["allocated_B"] = x["player.b" + str(self.decision_selector)]
            self.participant.vars["threshold_B"] = list(range(0, 81, 10))[::-1][
                                                       self.decision_selector - 1] + self.unct_selector_B

    def payment_realization_code(self):
        x = self.participant.vars["round_selected"]
        alloc_G = self.participant.vars["allocated_G"]
        thres_G = self.participant.vars["threshold_G"]
        alloc_B = self.participant.vars["allocated_B"]
        thres_B = self.participant.vars["threshold_B"]
        if x["player.game_type"] == "risky_setup_1" or x["player.game_type"] == "risky_setup_3_ambi":
            if self.urn_G <= thres_G:
                self.participant.vars["xG_final"] = self.participant.vars["x1G_selected"]
                self.participant.vars['tG_final'] = self.participant.vars["t1G_selected"]
                self.participant.vars["payoff_1"] = alloc_G * self.participant.vars["x1G_selected"]
            elif self.urn_G > thres_G:
                self.participant.vars["xG_final"] = self.participant.vars["x2G_selected"]
                self.participant.vars['tG_final'] = self.participant.vars["t2G_selected"]
                self.participant.vars["payoff_1"] = alloc_G * self.participant.vars["x2G_selected"]
            self.participant.vars["xB_final"] = 0
            self.participant.vars['tB_final'] = 0
            self.participant.vars["payoff_2"] = 0
            self.participant.vars["payoff_leftover"] = Constants.endo - alloc_G
        elif x["player.game_type"] == "risky_setup_2" or x["player.game_type"] == "risky_setup_4_ambi":
            if self.urn_G <= thres_G:
                self.participant.vars["xG_final"] = self.participant.vars["x1G_selected"]
                self.participant.vars['tG_final'] = self.participant.vars["t1G_selected"]
                self.participant.vars["payoff_1"] = alloc_G * self.participant.vars["x1G_selected"]
            elif self.urn_G > thres_G:
                self.participant.vars["xG_final"] = self.participant.vars["x2G_selected"]
                self.participant.vars['tG_final'] = self.participant.vars["t2G_selected"]
                self.participant.vars["payoff_1"] = alloc_G * self.participant.vars["x2G_selected"]
            if self.urn_B <= thres_B:
                self.participant.vars["xB_final"] = self.participant.vars["x1B_selected"]
                self.participant.vars['tB_final'] = self.participant.vars["t1B_selected"]
                self.participant.vars["payoff_2"] = alloc_B * self.participant.vars["x1B_selected"]
            elif self.urn_B > thres_B:
                self.participant.vars["xB_final"] = self.participant.vars["x2B_selected"]
                self.participant.vars['tB_final'] = self.participant.vars["t2B_selected"]
                self.participant.vars["payoff_2"] = alloc_B * self.participant.vars["x2B_selected"]
            self.participant.vars["payoff_leftover"] = Constants.endo - alloc_G - alloc_B
        self.xG_final = self.participant.vars["xG_final"]
        self.xB_final = self.participant.vars["xB_final"]
        self.tG_final = self.participant.vars['tG_final']
        self.tB_final = self.participant.vars['tB_final']
        self.payoff_A = self.participant.vars["payoff_1"] * self.session.config["real_world_currency_per_point"]
        self.payoff_B = self.participant.vars["payoff_2"] * self.session.config["real_world_currency_per_point"]
        self.payoff_now = (self.participant.vars["payoff_leftover"] * float(self.session.config["real_world_currency_per_point"])) + float(Constants.quest_fee) + float(self.session.config['participation_fee'])
