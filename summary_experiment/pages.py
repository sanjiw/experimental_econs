from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from otree.models import Session, Participant

class EnterPage(Page):
    form_model = 'player'
    form_fields = ['session1code']

class MyPage(Page):
    def vars_for_template(self):
        pass

class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


class Results(Page):
    pass


page_sequence = [
    EnterPage,
    MyPage
    ]