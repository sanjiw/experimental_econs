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
import random
import csv
import json
import pandas as pd


author = 'Putu Sanjiwacika Wibisana'

doc = """
Risky Setup - Green Only
"""


class Constants(BaseConstants):
    name_in_url = 'bi_introduction1'
    players_per_group = None
    num_rounds = 1
    with open('bi_introduction_simple/Params.csv') as file:
        params = pd.read_csv(file)


class Subsession(BaseSubsession):

    def cross_app_vars(self):
        for p in self.get_players():
            p.participant.vars['decision_list'] = []

class Group(BaseGroup):
    pass

class Player(BasePlayer):

    def cross_app_vars(self):
        self.participant.vars['decision_list'] = []
