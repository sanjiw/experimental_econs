from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Intro(Page):

    form_model = 'player'
    form_fields = ['participant_label']

    def vars_for_template(self):
        return {
            "participant_label": Constants.participant_label
        }

    def error_message(self, values):
        if values['participant_label'] != Constants.participant_label:
            return 'Anda memasukkan label partisipan yang salah. Gunakan kredensial yang sesuai dengan email dari ' \
                   'pelaksana eksperimen.'

    def before_next_page(self):
        self.player.payoff_dataframe()

class Payoff_RoundSelect(Page):

    form_model = "player"
    form_fields = ["round_selector"]

    def vars_for_template(self):
        return {
            'round_range': self.participant.vars['player_dataframe'].shape[0],
            'player_dataframe': self.participant.vars["player_dataframe"],
        }


    def before_next_page(self):
        self.player.round_selector_code()

class Payoff_UncertaintySelect(Page):

    def is_displayed(self):
        round_selected = self.participant.vars["round_selected"]
        return round_selected['player.game_type'] == "risky_setup_3_ambi" or round_selected['player.game_type'] == "risky_setup_4_ambi"

    form_model = "player"
    form_fields = ["unct_selector_G",
                   "unct_selector_B"]


    def vars_for_template(self):
        round_selected = self.participant.vars["round_selected"]
        return {
            'round_select': self.player.round_selector,
            'show_uncertain_prob_B': True if round_selected["player.game_type"] == "risky_setup_4_ambi" else False,
            'max_uncertain_prob_G' : round_selected["player.unknown_prob_G"],
            'max_uncertain_prob_B' : round_selected["player.unknown_prob_B"],
            'ambiguous_list': Constants.Ambiguous_list
        }

class Payoff_DecisionSelect(Page):

    form_model = "player"
    form_fields = ["decision_selector"]

    def vars_for_template(self):
        round_selected = self.participant.vars["round_selected"]
        decision_list = []
        if round_selected["player.game_type"] == "risky_setup_1":
            decision_list = [round_selected["player.a"+str(i)] for i in range(1,12)]
        elif round_selected["player.game_type"] == "risky_setup_2":
            decision_list = [[round_selected["player.a" + str(i)], round_selected["player.b" + str(i)]] for i in range(1, 12)]
        elif round_selected["player.game_type"] == "risky_setup_3_ambi":
            decision_list = [round_selected["player.a" + str(i)] for i in range(1, 10)]
        elif round_selected["player.game_type"] == "risky_setup_4_ambi":
            decision_list = [[round_selected["player.a" + str(i)], round_selected["player.b" + str(i)]] for i in range(1, 10)]
        self.participant.vars['decision_range'] = len(decision_list)
        return {
            'round_select': self.player.round_selector,
            'two_allocations': True if (round_selected["player.game_type"] == "risky_setup_4_ambi") or
                                       (round_selected["player.game_type"] == "risky_setup_2") else False,
            'decision_list' : decision_list,
            'decision_range': len(decision_list),
            'x1G_selected'  : self.participant.vars["x1G_selected"],
            'x2G_selected'  : self.participant.vars["x2G_selected"],
            'x1B_selected'  : self.participant.vars["x1B_selected"],
            'x2B_selected'  : self.participant.vars["x2B_selected"],
            't1G_selected'  : self.participant.vars["t1G_selected"],
            't2G_selected'  : self.participant.vars["t2G_selected"],
            't1B_selected'  : self.participant.vars["t1B_selected"],
            't2B_selected'  : self.participant.vars["t2B_selected"]
        }

    def before_next_page(self):
        self.player.decision_selector_code()

class Payoff_PaymentSelect(Page):

    form_model = "player"
    form_fields = ["urn_G",
                   "urn_B"]

    def vars_for_template(self):
        round_selected = self.participant.vars["round_selected"]
        return {
            'round_select': self.player.round_selector,
            'two_allocations': True if (round_selected["player.game_type"] == "risky_setup_4_ambi") or (
                        round_selected["player.game_type"] == "risky_setup_2") else False,
            'decision_range': self.participant.vars['decision_range'],
            'decision_selected': self.player.decision_selector,
            "show_uncertain_prob_B": True if round_selected["player.game_type"] == "risky_setup_4_ambi" else False,
            "x1G_selected": self.participant.vars["x1G_selected"],
            "x2G_selected": self.participant.vars["x2G_selected"],
            "t1G_selected": self.participant.vars["t1G_selected"],
            "t2G_selected": self.participant.vars["t2G_selected"],
            "x1B_selected": self.participant.vars["x1B_selected"],
            "x2B_selected": self.participant.vars["x2B_selected"],
            "t1B_selected": self.participant.vars["t1B_selected"],
            "t2B_selected": self.participant.vars["t2B_selected"],
            "threshold_G" : self.participant.vars["threshold_G"],
            "threshold_G_plus_1": self.participant.vars["threshold_G"] + 1,
            "threshold_B" : self.participant.vars["threshold_B"],
            "threshold_B_plus_1": self.participant.vars["threshold_B"] + 1,
            "allocated_G" : self.participant.vars["allocated_G"],
            "allocated_B" : self.participant.vars["allocated_B"],
            "leftover": Constants.endo - self.participant.vars["allocated_G"] - self.participant.vars["allocated_B"] if (round_selected["player.game_type"] == "risky_setup_4_ambi") or (
                        round_selected["player.game_type"] == "risky_setup_2") else Constants.endo - self.participant.vars["allocated_G"],
            "outcome_G1": self.participant.vars["x1G_selected"] * self.participant.vars["allocated_G"],
            "outcome_G2": self.participant.vars["x2G_selected"] * self.participant.vars["allocated_G"],
            "outcome_B1": self.participant.vars["x1B_selected"] * self.participant.vars["allocated_B"],
            "outcome_B2": self.participant.vars["x2B_selected"] * self.participant.vars["allocated_B"],
        }

    def before_next_page(self):
        self.player.payment_realization_code()

class Results(Page):

    def vars_for_template(self):
        round_selected = self.participant.vars["round_selected"]
        idr = self.session.config["real_world_currency_per_point"]
        return {'two_allocations': True if (round_selected["player.game_type"] == "risky_setup_4_ambi") or
                                           (round_selected["player.game_type"] == "risky_setup_2") else False,
                "idr" : self.session.config["real_world_currency_per_point"],

                "alloc_G"           : self.participant.vars["allocated_G"],
                "thres_G"           : self.participant.vars["threshold_G"],
                "alloc_B"           : self.participant.vars["allocated_B"],
                "thres_B"           : self.participant.vars["threshold_B"],

                "xG_final"          : self.participant.vars["xG_final"],
                "xB_final"          : self.participant.vars["xB_final"],
                "tG_final"          : self.participant.vars["tG_final"],
                "tB_final"          : self.participant.vars["tB_final"],
                "payoff_1"          : self.participant.vars["payoff_1"],
                "payoff_2"          : self.participant.vars["payoff_2"],
                "payoff_leftover"   : self.participant.vars["payoff_leftover"],
                "payoff_final"      : self.participant.vars["payoff_1"] + self.participant.vars["payoff_2"] + self.participant.vars["payoff_leftover"] + Constants.quest_fee,
                "payoff_1_idr"          : self.participant.vars["payoff_1"] * idr,
                "payoff_2_idr"          : self.participant.vars["payoff_2"] * idr,
                "payoff_leftover_idr"   : self.participant.vars["payoff_leftover"] * idr,
                "payoff_final_idr"      : int(((self.participant.vars["payoff_1"] +
                                            self.participant.vars["payoff_2"] +
                                            self.participant.vars["payoff_leftover"]) * idr) +
                                            self.session.config["participation_fee"]) + Constants.quest_fee,
                "quest_fee"             : Constants.quest_fee,
                "show_up_fee"           : int(self.session.config["participation_fee"]),
        }



page_sequence = [Intro,
                 Payoff_RoundSelect,
                 Payoff_UncertaintySelect,
                 Payoff_DecisionSelect,
                 Payoff_PaymentSelect,
                 Results]
