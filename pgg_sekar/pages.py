from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class _1_Intro(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        return {
            'endowment': Constants.endowment,
            'max_contribution': Constants.endowment * Constants.players_per_group,
            'num_players': Constants.players_per_group,
            'multiplier': Constants.multiplier,
            'sample1': 12,
            'sample2': 12 * Constants.multiplier,
        }


class Wait(WaitPage):

    def is_displayed(self):
        return self.subsession.round_number == 1


class _2_Contribute(Page):
    form_model = 'player'
    form_fields = ['token_contributed']

    def vars_for_template(self):
        return {
            'round': self.round_number,
        }


class _3_Guess(Page):
    form_model = 'player'
    form_fields = ['guess_total_token']

    def vars_for_template(self):
        return {
            'round': self.round_number,
        }


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoff()


class _4_Result(Page):

    def vars_for_template(self):
        return {
            'token_contributed': self.player.token_contributed,
            'payoff_thisround': int(self.player.payoff_thisround),
            'guess_total_token': self.player.guess_total_token,
            'total_token': self.group.total_token,
            'total_token_multiplied': self.group.total_token * Constants.multiplier,
            'round': self.round_number,
        }

    def before_next_page(self):
        if self.subsession.round_number == Constants.num_rounds:
            return {
                self.player.payoff_vector_storage(),
                self.player.payoff_final()
            }
        else:
            return self.player.payoff_vector_storage()


class _5_FinalResult(Page):

    def vars_for_template(self):
        return {
            'final_payoff': self.player.payoff
        }

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

page_sequence = [
    _1_Intro,
    Wait,
    _2_Contribute,
    _3_Guess,
    ResultsWaitPage,
    _4_Result,
    _5_FinalResult
]
