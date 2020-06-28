from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Initiation(Page):

    def before_next_page(self):
        self.subsession.cross_app_vars()

page_sequence = [Initiation]
