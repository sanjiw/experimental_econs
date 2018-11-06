from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class MyPage(Page):
    def vars_for_template(self):
        session1 = self.session.config['session_code1']
        session2 = self.session.config['session_code2']
        session3 = self.session.config['session_code3']


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


class Results(Page):
    pass


page_sequence = [
    MyPage,
    ResultsWaitPage,
    Results
]
