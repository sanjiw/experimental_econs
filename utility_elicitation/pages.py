from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class _1Introduction(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1

    form_model = 'player'
    form_fields = ['choosePEorCE']

    def before_next_page(self):
        return self.player.ExtendOptions()

class _2PE(Page):

    def is_displayed(self):
        return self.participant.vars['elic_type'][self.subsession.round_number-1] == "PE"

    form_model = 'player'
    form_fields = ['PESwitchingPoint']

    def vars_for_template(self):
        return {
            'E_range': list(zip(list(range(len(self.session.vars['prob_E_range']))),self.session.vars['prob_E_range'],
                                self.session.vars['prob_cE_range'])),
            'prospect_max': self.session.config['PE_prospect_max'],
            'prospect_min': self.session.config['PE_prospect_min'],
            'CE': self.session.config['PE_certainamount'][self.subsession.round_number-1]
        }

    def before_next_page(self):
        return self.player.compile()


class _3CE(Page):

    def is_displayed(self):
        return self.participant.vars['elic_type'][self.subsession.round_number - 1] == "CE"

    form_model = 'player'
    form_fields = ['CESwitchingPoint']

    def vars_for_template(self):
        return {
            'E_range': list(zip(list(range(len(self.session.vars['CE_range']))),(self.session.vars['CE_range']))),
            'CE_P': round((self.session.config['CE_prob_P'][self.subsession.round_number-1])*100, 2),
            'CE_cP': round((1 - self.session.config['CE_prob_P'][self.subsession.round_number-1])*100, 2),
            'CE_P_pts': self.session.config['CE_P_points'],
            'CE_cP_pts': self.session.config['CE_cP_points']
        }

    def before_next_page(self):
        return self.player.compile()


class _4Results(Page):

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {
            'data': self.session.vars['series'],
            'elic_type': self.participant.vars['elic_type'][self.round_number == 1],
        }


page_sequence = [
    _1Introduction,
    _2PE,
    _3CE,
    _4Results,
]
