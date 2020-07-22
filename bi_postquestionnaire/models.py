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

import pandas as pd
import numpy as np
import random

author = 'Your name here'

doc = """
Your app description
"""
import csv

class Constants(BaseConstants):
    name_in_url = 'bi_postquestionnaire'
    players_per_group = None
    num_rounds = 1
    endo = 25
    with open('bi_postquestionnaire/Ambiguity.csv') as csvFile:
        reader = csv.reader(csvFile)
        Ambiguous_list = next(reader)

class Subsession(BaseSubsession):

    def payoff_dataframe(self):
        for p in self.get_players():
            p.participant.vars["player_dataframe"] = pd.DataFrame(list(zip(p.participant.vars['decision_list'],
                                                                           p.participant.vars['game_type'],
                                                                           p.participant.vars['x1G'],
                                                                           p.participant.vars['x2G'],
                                                                           p.participant.vars['unknown_prob_G'],
                                                                           p.participant.vars['x1B'],
                                                                           p.participant.vars['x2B'],
                                                                           p.participant.vars['unknown_prob_B'],
                                                                           p.participant.vars['t1G'],
                                                                           p.participant.vars['t2G'],
                                                                           p.participant.vars['t1B'],
                                                                           p.participant.vars['t2B'])),
                                                                  columns =['decision_list', 'game_type', 'x1G', 'x2G',
                                                                            'unknown_prob_G', 'x1B', 'x2B', 'unknown_prob_B',
                                                                            't1G', 't2G', 't1B', 't2B'])

    def round_selector(self):
        for p in self.get_players():
            p.participant.vars["round_selected"] = p.participant.vars["player_dataframe"].loc[p.round_selector-1]
            p.participant.vars["x1G_selected"] = p.participant.vars["round_selected"]["x1G"]
            p.participant.vars["x2G_selected"] = p.participant.vars["round_selected"]["x2G"]
            p.participant.vars["x1B_selected"] = p.participant.vars["round_selected"]["x1B"]
            p.participant.vars["x2B_selected"] = p.participant.vars["round_selected"]["x2B"]
            p.participant.vars["t1G_selected"] = p.participant.vars["round_selected"]["t1G"]
            p.participant.vars["t2G_selected"] = p.participant.vars["round_selected"]["t2G"]
            p.participant.vars["t1B_selected"] = p.participant.vars["round_selected"]["t1B"]
            p.participant.vars["t2B_selected"] = p.participant.vars["round_selected"]["t2B"]

    def decision_selector(self):
        for p in self.get_players():
            x = p.participant.vars["round_selected"]
            if x["game_type"] == "risky_setup_1":
                p.participant.vars["allocated_G"] = x["decision_list"][p.decision_selector-1]
                p.participant.vars["threshold_G"] = list(range(0, 101, 10))[::-1][p.decision_selector - 1]
            elif x["game_type"] == "risky_setup_2":
                p.participant.vars["allocated_G"] = x["decision_list"][p.decision_selector - 1][0]
                p.participant.vars["threshold_G"] = list(range(0, 81, 10))[::-1][p.decision_selector - 1]
                p.participant.vars["allocated_B"] = x["decision_list"][p.decision_selector - 1][1]
                p.participant.vars["threshold_B"] = list(range(0, 81, 10))[::-1][p.decision_selector - 1]
            elif x["game_type"] == "risky_setup_3_ambi":
                p.participant.vars["allocated_G"] = x["decision_list"][p.decision_selector - 1]
                p.participant.vars["threshold_G"] = list(range(0, 101, 10))[::-1][p.decision_selector - 1] + p.unct_selector_G
            elif x["game_type"] == "risky_setup_4_ambi":
                p.participant.vars["allocated_G"] = x["decision_list"][p.decision_selector - 1][0]
                p.participant.vars["threshold_G"] = list(range(0, 81, 10))[::-1][p.decision_selector - 1] + p.unct_selector_G
                p.participant.vars["allocated_B"] = x["decision_list"][p.decision_selector - 1][1]
                p.participant.vars["threshold_B"] = list(range(0, 81, 10))[::-1][p.decision_selector - 1] + p.unct_selector_B

    def payment_realization(self):
        for p in self.get_players():
            x = p.participant.vars["round_selected"]
            alloc_G = p.participant.vars["allocated_G"]
            thres_G = p.participant.vars["threshold_G"]
            alloc_B = p.participant.vars["allocated_B"]
            thres_B = p.participant.vars["threshold_B"]
            if x["game_type"] == "risky_setup_1" or x["game_type"] == "risky_setup_3_ambi":
                if p.urn_G <= thres_G:
                    p.participant.vars["xG_final"] = p.participant.vars["x1G_selected"]
                    p.participant.vars['tG_final'] = p.participant.vars["t1G_selected"]
                    p.participant.vars["payoff_1"] = alloc_G * p.participant.vars["x1G_selected"]
                elif p.urn_G > thres_G:
                    p.participant.vars["xG_final"] = p.participant.vars["x2G_selected"]
                    p.participant.vars['tG_final'] = p.participant.vars["t2G_selected"]
                    p.participant.vars["payoff_1"] = alloc_G * p.participant.vars["x2G_selected"]
                p.participant.vars["payoff_2"] = 0
                p.participant.vars["payoff_leftover"] = Constants.endo - alloc_G
            elif x["game_type"] == "risky_setup_2" or x["game_type"] == "risky_setup_4_ambi":
                if p.urn_G <= thres_G:
                    p.participant.vars["xG_final"] = p.participant.vars["x1G_selected"]
                    p.participant.vars['tG_final'] = p.participant.vars["t1G_selected"]
                    p.participant.vars["payoff_1"] = alloc_G * p.participant.vars["x1G_selected"]
                elif p.urn_G > thres_G:
                    p.participant.vars["xG_final"] = p.participant.vars["x2G_selected"]
                    p.participant.vars['tG_final'] = p.participant.vars["t2G_selected"]
                    p.participant.vars["payoff_1"] = alloc_G * p.participant.vars["x2G_selected"]
                if p.urn_B <= thres_B:
                    p.participant.vars["xB_final"] = p.participant.vars["x1B_selected"]
                    p.participant.vars['tB_final'] = p.participant.vars["t1B_selected"]
                    p.participant.vars["payoff_2"] = alloc_B * p.participant.vars["x1B_selected"]
                elif p.urn_B > thres_B:
                    p.participant.vars["xB_final"] = p.participant.vars["x2B_selected"]
                    p.participant.vars['tB_final'] = p.participant.vars["t2B_selected"]
                    p.participant.vars["payoff_2"] = alloc_B * p.participant.vars["x2B_selected"]
                p.participant.vars["payoff_leftover"] = Constants.endo - alloc_G - alloc_B
            p.payoff = p.participant.vars["payoff_1"] + p.participant.vars["payoff_2"] + p.participant.vars["payoff_leftover"]

class Group(BaseGroup):
    pass

def make_field(label):
    return models.IntegerField(
        choices=[1, 2, 3, 4, 5, 6],
        label=label,
        widget=widgets.RadioSelect,
    )

class Player(BasePlayer):

    round_selector = models.IntegerField()
    decision_selector = models.IntegerField()
    unct_selector_G = models.IntegerField(initial=0)
    unct_selector_B = models.IntegerField(initial=0)
    urn_G = models.IntegerField()
    urn_B = models.IntegerField()

    q1_a = make_field("I support the use of eco-friendly products for toiletries and washing dishes; e.g., recycled toilet paper.")
    q1_b = make_field("I support to reduce the use of fossil energy; e.g., switch to renewable energy.")
    q1_c = make_field("I support using the eco-friendly products for fashion; e.g., reused clothes.")
    q1_d = make_field("I support using the eco-friendly products for agricultural industry (e.g., organic fertiliser).")
    q1_e = make_field("I support using the eco-friendly products for laundrette (e.g., detergent).")
    q2_a = make_field("I would be willing to use (pay the price) the green products for my toiletries and washing dishes; e.g., recycled toilet paper, eco-friendly dishwasher and eco-friendly dish soap.")
    q2_b = make_field("I would be willing to reduce fossil energy consumption and to switch to renewable energy; e.g., use more public transport and use solar panel.")
    q2_c = make_field("I would be willing to use (pay the price) any kinds of green product for my fashion; e.g., recycled and reused clothes.")
    q2_d = make_field("I would be willing to consume organic food in a regular basis; e.g., daily, or weekly or monthly shopping for organic food/groceries.")
    q2_e = make_field("I would be willing to use (pay the price) eco-friendly detergent and eco-friendly whitener for my laundrette.")
    q3_a = make_field("The use of renewable energy (e.g. solar panel or biodiesel) can significantly reduce the risk of public health.")
    q3_b = make_field("An increase use of public transport can significantly reduce the environmental damages.")
    q3_c = make_field("The environmental damages from using recycled and reused products is significantly less than using newly-branded clothes.")
    q3_d = make_field("Chemical products used in eco products are significantly less harmful to the environment than that of non-eco-friendly products.")
    q3_e = make_field("Consuming organic foods in a regular basis can significantly increase my health and immune.")
    q4_a = make_field("I think the energy providers in Indonesia (PLN and Pertamina) have good intentions in managing country’s energy supply with an eco-friendly system.")
    q4_b = make_field("I believe companies that produce eco-friendly products (e.g., refrigerator, AC and dishwasher) use environment-friendly materials.")
    q4_c = make_field("I believe we will all move on to use more green products in the near future for a better individual health.")
    q4_d = make_field("I trust public to do anything necessary to reduce the pollution level in my area and country.")
    q4_e = make_field("I trust the government (both central and local) to promote more green products in the near future for a better public health.")





























