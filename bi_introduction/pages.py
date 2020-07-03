from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random

class Initiation(Page):

    def before_next_page(self):
        self.subsession.cross_app_vars()

    def app_after_this_page(self, upcoming_apps):
        app_list = ['bi_risky_setup_1',
                    'bi_risky_setup_2',
                    'bi_risky_setup_3_ambi',
                    'bi_risky_setup_4_ambi']
        next_app = random.choice(app_list)
        self.participant.vars['finished_app'] = [next_app]
        return next_app


page_sequence = [Initiation]
