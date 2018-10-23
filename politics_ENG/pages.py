from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Intro1(Page):

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'conversion': self.session.config['real_world_currency_per_point'],
        }


class IntroWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.subsession.preference_setting()

    body_text = "Waiting for all other participants to proceed."


class Intro2(Page):
    pass


class Elect(Page):
    #player cast their vote.
    def is_displayed(self):
        return self.player.able_to_vote == 'yes'

    form_model = 'player'
    form_fields = ['ballot']

class UnElect(Page):

    def is_displayed(self):
        return self.player.able_to_vote == 'no'

class ElectionWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.subsession.winner()

    body_text = "Waiting for all other participants to proceed."


class Elect_r(Page):
    # Election outcome.

    def vars_for_template(self):
        return {
            'Election winner': self.subsession.winner,
            'payoff_total_win': Constants.endowment + Constants.payoff_win,
            'payoff_total_lost': Constants.endowment + Constants.payoff_lost,
        }


class General_wait(WaitPage):

    body_text = "Waiting for all other participants to proceed."


class Corrupt_o(Page):
    # player cast their impeachment opinion.
    def vars_for_template(self):
        return {
            'payoff_win': Constants.payoff_win,
            'payoff_lost': Constants.payoff_lost,
            'reliability': (Constants.p_good_outlet * 100),
            'pct_impeach': (Constants.p_impeach * 100)
        }
    form_model = 'player'
    form_fields = ['opinion']

    def checkslider_error_message(self, value):
        if not value:
            return 'Please make your decision using slider'

class Corrupt_o2(Page):
    # player cast their impeachment opinion.
    def vars_for_template(self):
        return {
            'payoff_win': Constants.payoff_win,
            'payoff_lost': Constants.payoff_lost,
            'reliability': (Constants.p_good_outlet * 100),
            'pct_impeach': (Constants.p_impeach * 100),
            'guilty_prob': (Constants.p_guilty * 100)
        }
    form_model = 'player'
    form_fields = ['accuracy_est']

    def checkslider_error_message(self, value):
        if not value:
            return 'Please make your decision using slider'



class CorruptWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.subsession.scoring_rules()
        self.subsession.payoff_rules()


class Corrupt_r(Page):

    def vars_for_template(self):
        return {
            'election_winner': self.subsession.winning_cand,
            'acc_score': round(self.player.accuracy_score),
            'impeach_prob': round(self.subsession.prob_impeach,2)*100,
            'bayes_prob': round(self.subsession.d_bayes_prob,2)*100
        }


page_sequence = [ Intro1,
                  IntroWaitPage,
                  Intro2,
                  General_wait,
                  Elect,
                  UnElect,
                  ElectionWaitPage,
                  Elect_r,
                  General_wait,
                  Corrupt_o,
                  Corrupt_o2,
                  CorruptWaitPage,
                  Corrupt_r]