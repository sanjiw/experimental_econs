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


author = 'Putu Sanjiwacika Wibisana'

doc = """
Risky Setup - Green Only
"""


class Constants(BaseConstants):
    name_in_url = 'bi_introduction'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):

    def cross_app_vars(self):
        for p in self.get_players():
            p.participant.vars['payoff_vector_s1'] = []
            p.participant.vars['game_type'] = []
            p.participant.vars['MPL_selector_index'] = []
            p.participant.vars["Choice_selection_G"] = []
            p.participant.vars["Choice_selection_B"] = []
            p.participant.vars["xG_select"] = []
            p.participant.vars["xB_select"] = []
            p.participant.vars["unknown_prob_G"] = []
            p.participant.vars["unknown_prob_B"] = []


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass
