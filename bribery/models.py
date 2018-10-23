from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import numpy as np
from random import shuffle

doc = """
Bribery Game dengan 3 pemain per grup per ronde
"""

class Constants(BaseConstants):
    name_in_url = 'Eksperimen_penyuapan'
    players_per_group = 3
    num_rounds = 4
    instructions_template = 'bribery/Instructions.html'
    endowment_high = 40
    endowment_low = 40
    strategy_space = [50, 40, 30, 20, 10]


class Subsession(BaseSubsession):

    multiplier = models.FloatField()

    def creating_session(self):
        #matrix = [[[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15], [16, 17, 18], [19, 20, 21], [24, 23, 22], [25, 26, 27], [30, 29, 28], [32, 31, 33], [34, 35, 36], [37, 38, 39], [40, 41, 42]],
    #              [[26, 22, 42], [35, 32, 16], [6, 12, 24], [38, 34, 31], [14, 10, 5], [11, 33, 25], [20, 1, 7], [4, 37, 40], [39, 29, 17], [8, 3, 28], [15, 19, 30], [2, 41, 36], [23, 21, 13], [27, 18, 9]],
    #              [[35, 11, 20], [7, 41, 10], [37, 15, 3], [30, 39, 18], [23, 27, 12], [1, 4, 36], [34, 19, 17], [25, 8, 31], [40, 33, 24], [6, 26, 29], [2, 16, 9], [14, 28, 21], [32, 42, 38], [22, 13, 5]],
    #              [[15, 8, 2], [42, 28, 24], [26, 10, 13], [9, 38, 19], [34, 7, 12], [27, 33, 14], [4, 18, 3], [21, 35, 40], [11, 22, 36], [6, 39, 25], [5, 32, 1], [31, 41, 37], [20, 16, 29], [17, 30, 23]],
    #              [[17, 38, 22], [31, 19, 23], [6, 27, 30], [40, 13, 34], [26, 7, 5], [25, 20, 14], [8, 42, 11], [41, 12, 3], [9, 4, 39], [21, 33, 1], [32, 15, 29], [24, 10, 16], [18, 2, 35], [36, 37, 28]],
    #              [[34, 14, 37], [1, 27, 41], [30, 2, 4], [3, 32, 11], [22, 35, 15], [10, 29, 23], [31, 36, 40], [13, 19, 28], [26, 9, 20], [39, 5, 12], [33, 8, 16], [7, 6, 17], [38, 18, 24], [42, 21, 25]],
    #              [[16, 27, 13], [3, 40, 38], [28, 39, 15], [10, 42, 2], [7, 29, 36], [23, 20, 4], [18, 14, 22], [11, 21, 6], [24, 8, 17], [12, 37, 33], [30, 35, 25], [5, 31, 9], [19, 26, 1], [41, 32, 34]],
    #              [[16, 14, 6], [19, 11, 24], [33, 9, 15], [28, 17, 12], [37, 30, 7], [36, 23, 38], [8, 40, 20], [5, 41, 18], [21, 31, 10], [29, 3, 42], [35, 39, 13], [4, 27, 32], [2, 34, 26], [1, 22, 25]],
    #              [[12, 2, 29], [33, 6, 13], [42, 16, 1], [41, 4, 22], [28, 27, 31], [15, 21, 38], [20, 17, 5], [40, 10, 25], [30, 36, 9], [39, 24, 34], [37, 23, 26], [18, 7, 11], [3, 14, 35], [19, 32, 8]],
    #              [[15, 27, 11], [12, 18, 21], [13, 37, 24], [5, 35, 33], [36, 20, 42], [41, 6, 23], [10, 39, 8], [9, 14, 1], [31, 7, 16], [22, 32, 30], [28, 34, 4], [38, 29, 25], [2, 19, 40], [3, 26, 17]],
    #              [[26, 11, 16], [12, 4, 31], [9, 28, 41], [27, 2, 38], [35, 42, 37], [23, 39, 7], [8, 6, 36], [33, 10, 30], [20, 3, 22], [34, 25, 18], [21, 32, 24], [1, 13, 17], [29, 19, 14], [15, 5, 40]],
    #              [[17, 33, 36], [19, 35, 41], [25, 9, 32], [14, 12, 30], [10, 34, 1], [20, 28, 18], [39, 40, 27], [42, 15, 23], [31, 26, 24], [22, 6, 2], [5, 37, 8], [38, 7, 13], [21, 3, 16], [29, 11, 4]],
    #              [[13, 2, 20], [17, 31, 42], [24, 5, 30], [16, 15, 12], [33, 34, 22], [18, 10, 19], [35, 23, 9], [11, 41, 39], [14, 36, 26], [32, 40, 28], [27, 21, 29], [6, 37, 1], [8, 4, 38], [25, 7, 3]],
    #              [[39, 26, 33], [7, 27, 24], [22, 10, 9], [38, 28, 11], [36, 3, 5], [18, 6, 15], [29, 35, 8], [31, 20, 30], [4, 42, 13], [40, 1, 12], [17, 41, 21], [2, 14, 32], [37, 19, 25], [16, 23, 34]],
    #              [[14, 39, 31], [3, 10, 6], [27, 34, 20], [24, 4, 35], [28, 22, 7], [12, 38, 26], [36, 16, 19], [13, 30, 11], [23, 8, 1], [21, 2, 5], [32, 37, 17], [41, 15, 25], [42, 18, 33], [29, 9, 40]]]
        matrix = [[1, 2, 3]], [[3, 2, 1]], [[2, 3, 1]], [[3, 1, 2]]
        self.set_group_matrix(matrix[self.round_number - 1])
        self.get_group_matrix()
        for p in self.get_players():
            p.treatmentgroup = self.session.config['treatment']
            ### Treatment group: Control (0), Treatment 1 (1), Treatment 2 (2)

        #player_id_matrix = list(range(1, (Constants.players_per_group + 1)))
        #equal_prob_matrix = [1 / Constants.players_per_group] * Constants.players_per_group
        #pid_briber = np.random.choice(player_id_matrix, 1, p=equal_prob_matrix)
        for p in self.get_players():
            if p.id_in_group == 1:
                p.briber = True
            else:
                p.briber = False

        self.multiplier = self.session.config['soc_welf_multiplier']
        for p in self.get_players():
            if self.round_number <= self.session.config['num_training_rounds']:
                p.training_round = True
            else:
                p.training_round = False


    def vars_for_admin_report(self):
        contributions = [p.contribution for p in self.get_players() if p.contribution != None]
        if contributions:
            return {
                'avg_contribution': sum(contributions)/len(contributions),
                'min_contribution': min(contributions),
                'max_contribution': max(contributions),
            }
        else:
            return {
                'avg_contribution': '(no data)',
                'min_contribution': '(no data)',
                'max_contribution': '(no data)',
            }

    def endowment_rule(self):
        for p in self.get_players():
            if p.id_in_group == 3:
                p.endowment = Constants.endowment_high
            else:
                p.endowment = Constants.endowment_low


class Group(BaseGroup):
    total_contribution = models.FloatField()
    social_welfare = models.FloatField()
    social_welfare_embz = models.FloatField(min=0)
    contribution_left = models.FloatField()
    amt_embezzled_g = models.FloatField()
    punish = models.BooleanField()
    bribe_acc = models.BooleanField()

    def set_payoffs1(self):
        self.total_contribution = sum([p.contribution for p in self.get_players()])

    def bribe_acceptance_rule(self):
        bribe = 0
        for p in self.get_players():
            bribe += p.bribe_pct
        if bribe >= self.session.config['bribe_threshold']:
            self.bribe_acc = True
        else:
            self.bribe_acc = False

    def cal_embezzlement(self):
        embz = 0
        for p in self.get_players():
            embz += p.amount_embezzled
        self.amt_embezzled_g = embz

    def prob_punishment(self):
        punish_prob = self.session.config['punishment_prob']
        if self.bribe_acc == True:
            self.punish = np.random.choice([True, False], 1, p=[punish_prob, 1-punish_prob])
        else:
            self.punish = False

    def set_payoffs2(self):
        mpcr = self.session.config['soc_welf_multiplier']
        #### NO EMBEZZLEMENT
        self.social_welfare = self.total_contribution * mpcr
        ### EMBEZZLED PARAMETERS
        self.contribution_left = self.total_contribution - self.amt_embezzled_g
        self.social_welfare_embz = self.contribution_left * mpcr

        for p in self.get_players():
            ######## CONTROL GROUP: NO PUNISHMENT                                ########
            if p.treatmentgroup == '0':
                if self.amt_embezzled_g > 0 and self.bribe_acc == True:
                    p.payoff_thisround = (p.endowment - p.contribution) + p.bribe_self + (self.social_welfare_embz /
                                                                                      Constants.players_per_group)
                else:
                    p.payoff_thisround = (p.endowment - p.contribution) + (self.social_welfare / Constants.players_per_group)
            ######## TREATMENT GROUP 1: PROBABILISTIC PUNISHMENT - FINES         ########
            elif p.treatmentgroup == '1':
                if self.amt_embezzled_g > 0:
                    if p.briber == True and self.bribe_acc == True and self.punish == True:
                        p.payoff_thisround = (p.endowment - p.contribution) + p.bribe_self + \
                                   (self.social_welfare_embz / Constants.players_per_group) - self.session.config['punish_fine']
                    elif p.briber == True and self.bribe_acc == True and self.punish == False:
                        p.payoff_thisround = (p.endowment - p.contribution) + p.bribe_self + \
                                   (self.social_welfare_embz / Constants.players_per_group)
                    elif p.briber == True and self.bribe_acc == False:
                        p.payoff_thisround = (p.endowment - p.contribution) + (self.social_welfare / Constants.players_per_group)
                    elif p.briber == False and self.bribe_acc == True:
                        p.payoff_thisround = (p.endowment - p.contribution) + (self.social_welfare_embz / Constants.players_per_group)
                    elif p.briber == False and self.bribe_acc == False:
                        p.payoff_thisround = (p.endowment - p.contribution) + (self.social_welfare / Constants.players_per_group)
                else:
                    p.payoff_thisround = (p.endowment - p.contribution) + (self.social_welfare / Constants.players_per_group)
            ######## TREATMENT GROUP 2: PROBABILISTIC PUNISHMENT - SOCIAL COST   ########
            elif p.treatmentgroup == '2':
                if self.amt_embezzled_g > 0:
                    if p.briber == True and self.bribe_acc == True and self.punish == True:
                        if (p.endowment - p.contribution) - ((self.social_welfare - self.social_welfare_embz) *
                                                                         self.session.config['social_cost_multiplier']) < 0:
                            p.payoff_thisround = 0
                        else:
                            p.payoff_thisround = (p.endowment - p.contribution) - ((self.social_welfare - self.social_welfare_embz) *
                                                                         self.session.config['social_cost_multiplier'])
                    elif p.briber == True and self.bribe_acc == True and self.punish == False:
                        p.payoff_thisround = (p.endowment - p.contribution) + p.bribe_self + \
                                   (self.social_welfare_embz / Constants.players_per_group)
                    elif p.briber == True and self.bribe_acc == False:
                        p.payoff_thisround = (p.endowment - p.contribution) + (self.social_welfare / Constants.players_per_group)
                    elif p.briber == False and self.bribe_acc == True:
                        p.payoff_thisround = (p.endowment - p.contribution) + (self.social_welfare_embz / Constants.players_per_group)
                    elif p.briber == False and self.bribe_acc == False:
                        p.payoff_thisround = (p.endowment - p.contribution) + (self.social_welfare / Constants.players_per_group)
                else:
                    p.payoff_thisround = (p.endowment - p.contribution) + (self.social_welfare / Constants.players_per_group)

class Player(BasePlayer):

    choice = models.StringField(
        widget=widgets.RadioSelect,
        choices=[str(i) + '%' for i in Constants.strategy_space]
    )
    bribe_pct = models.IntegerField(default=0,
        widget=widgets.Slider,
        min=0, max=100
    )
    contribution = models.FloatField()
    endowment = models.FloatField()
    treatmentgroup = models.StringField()
    briber = models.BooleanField()
    amount_embezzled = models.FloatField(default=0, min=0, max=Group.total_contribution)
    bribe_self = models.FloatField(default=0)
    bribe_AI = models.FloatField(default=0)
    payoff_thisround = models.FloatField()
    training_round = models.BooleanField()
    dump = models.StringField()
    dump2 = models.StringField()
    dump3 = models.StringField()

    def payoff_vector_storage(self):
        #### Cross-app data collection protocol
        if self.round_number == 1 and len(self.participant.vars['payoff_vct']) == 0:
            self.participant.vars['payoff_vct'] = [self.payoff_thisround]
            self.participant.vars['training'] = [self.training_round]
            self.participant.vars['round_all_vct'] = [1]
        else:
            self.participant.vars['payoff_vct'].append(self.payoff_thisround)
            self.participant.vars['training'].append(self.training_round)
            vct = self.participant.vars['round_all_vct']
            self.participant.vars['round_all_vct'].append(vct[-1] + 1)
        #### dumps are for debugging purposes. No real use
        self.dump = str(self.participant.vars['payoff_vct'])
        self.dump2 = str(self.participant.vars['training'])
        self.dump3 = str(self.participant.vars['round_all_vct'])

    def money_alloc(self):
        self.bribe_self = float((100 - self.bribe_pct)/100) * self.amount_embezzled
        self.bribe_AI = float(self.bribe_pct/100) * self.amount_embezzled

    def set_contribute(self):
        choice = [str(i) + '%' for i in Constants.strategy_space]
        if self.choice == choice[0]:
            self.contribution = (Constants.strategy_space[0] * self.endowment / 100)
        elif self.choice == choice[1]:
            self.contribution = (Constants.strategy_space[1] * self.endowment / 100)
        elif self.choice == choice[2]:
            self.contribution = (Constants.strategy_space[2] * self.endowment / 100)
        elif self.choice == choice[3]:
            self.contribution = (Constants.strategy_space[3] * self.endowment / 100)
        else:
            self.contribution = (Constants.strategy_space[4] * self.endowment / 100)

    def role(self):
        if self.briber == True:
            return 'briber'
        else:
            return 'innocent'

