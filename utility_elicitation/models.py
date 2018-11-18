from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from flask import json
import flask


author = 'Putu Sanjiwacika Wibisana'

doc = """
Demonstration of several utility measurement method.
"""


class Constants(BaseConstants):
    name_in_url = 'utility_elicitation'
    players_per_group = None
    num_rounds = 9


class Subsession(BaseSubsession):

    def creating_session(self):
        # For Probability Equivalent
        self.session.vars['prob_E_range'] = [100-(5*i) for i in range(0,21)]
        self.session.vars['prob_cE_range'] = [(5*i) for i in range(0, 21)]
        # For Certainty Equivalent
        self.session.vars['CE_range'] = [round(self.session.config['CE_max']-((self.session.config['CE_max']/
                                                                               len(range(0,21)))*i),2) for i in range(0,21)]


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    choosePEorCE = models.StringField()

    def ExtendOptions(self):
        self.participant.vars['elic_type'] = [self.choosePEorCE for _ in range(Constants.num_rounds)]
        self.choosePEorCE = self.participant.vars['elic_type'][self.round_number]

    def compile(self):
        if self.participant.vars['elic_type'][0] == "PE":
            if self.round_number == 1:
                self.participant.vars['switching_points'] = [int(self.PESwitchingPoint[:-1])]
            else: self.participant.vars['switching_points'].append(int(self.PESwitchingPoint[:-1]))
        else:
            if self.round_number == 1:
                self.participant.vars['switching_points'] = [int(self.CESwitchingPoint[:-1])]
            else: self.participant.vars['switching_points'].append(int(self.CESwitchingPoint[:-1]))
        #self.dump = str(self.participant.vars['switching_points'])
        self.participant.vars['PE_chosen'] = [self.session.vars['prob_E_range'][i-1] for i in self.participant.vars['switching_points']]
        self.participant.vars['CE_chosen'] = [self.session.vars['CE_range'][i-1] for i in self.participant.vars['switching_points']]
        if self.participant.vars['elic_type'][0] == "PE":
            self.dump = str(self.participant.vars['PE_chosen'])
        else: self.dump = str(self.participant.vars['CE_chosen'])
        #should go separate function?
        self.participant.vars['matrix'] = []
        if self.round_number == Constants.num_rounds:
            if self.participant.vars['elic_type'][0] == "PE":
                self.participant.vars['matrix'] = list(zip(self.participant.vars['switching_points'],[i/100 for i in self.participant.vars['PE_chosen']],
                                  self.session.config['PE_certainamount']))
            else:
                self.participant.vars['matrix'] = list(zip(self.participant.vars['switching_points'],[i/100 for i in self.session.config['CE_prob_P']],
                                  self.participant.vars['CE_chosen']))
        else: pass
        data = [list(x) for x in zip([i[2] for i in self.participant.vars['matrix']],
                                     [i[1] for i in self.participant.vars['matrix']])]
        self.session.vars['series'] = [['X', 'U'], [0, 0], [100, 1]] + data



    PESwitchingPoint = models.StringField()
    CESwitchingPoint = models.StringField()

    dump = models.StringField()
    dump2 = models.StringField()

    PE_EU_CARA = models.FloatField()
    PE_RDU_CARA = models.FloatField()

    CE_EU_CARA = models.FloatField()
    CE_RDU_CARA = models.FloatField()
