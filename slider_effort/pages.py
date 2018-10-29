from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class _1Intro(Page):
    def vars_for_template(self):
        return {
            'points_high': self.session.config['points_exact'],
            'points_low': self.session.config['points_near']
        }
    form_model = 'player'
    form_fields = ['test_slider']


class _2Quizzes(Page):
    timeout_seconds = 60
    timer_text = 'Waktu yang tersisa:'
    form_model = 'player'
    form_fields = ['slider_1',
                   'slider_2',
                   'slider_3',
                   'slider_4',
                   'slider_5',
                   'slider_6',
                   'slider_7',
                   'slider_8',
                   'slider_9',
                   'slider_10',
                   'slider_11',
                   'slider_12',
                   'slider_13',
                   'slider_14',
                   'slider_15',
                   'slider_16',
                   'slider_17',
                   'slider_18',
                   'slider_19',
                   'slider_20',
                   'slider_21',
                   'slider_22',
                   'slider_23',
                   'slider_24',
                   'slider_25']

    def before_next_page(self):
        return self.player.matrixing()

class _3Results(Page):
    def vars_for_template(self):
        return {
            'score': self.player.score_player
        }


page_sequence = [
    _1Intro,
    _2Quizzes,
    _3Results
]
