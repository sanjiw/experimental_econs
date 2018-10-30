from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Sanjiwacika Wibisana - UGM'

doc = """
Welcome screen
"""


class Constants(BaseConstants):
    name_in_url = 'intro_screen'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass
