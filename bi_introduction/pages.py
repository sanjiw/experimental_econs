from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class MyPage(Page):

    def before_next_page(self):
        self.subsession.cross_app_vars()

page_sequence = [MyPage]
