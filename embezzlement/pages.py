from ._builtin import Page, WaitPage
from .models import Constants, Player, Group
from otree.api import (Currency as c)
import numpy as np

from otreeutils.pages import AllGroupsWaitPage, ExtendedPage, UnderstandingQuestionsPage


class Introduction(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1
    def vars_for_template(self):
        return {
            'num_training_rounds': self.session.config['num_training_rounds'],
            'endowment': self.session.config['endowment'],
            'timeout': self.session.config['timeout_real']
        }

class TestQ(UnderstandingQuestionsPage):

    def is_displayed(self):
        return self.round_number == (self.session.config['num_training_rounds'] + 1)

    page_title = 'Uji Pemahaman Instrumen'
    set_correct_answers = False
    form_model = 'player'
    questions = [
        {
            'question': 'Anda punya poin awal 100. Anda menyumbang 10 poin, pemain lainnya masing-masing menyumbang'
                        ' 10 poin. Tidak ada pemain yang mengambil poin. Berapakah total nilai sumbangan?',
            'options': [10, 20, 30, 40],
            'correct': 30,
            'hint': 'Ingat, total sumbangan adalah jumlah poin yang disumbangkan seluruh pemain, dikurangi pengambilan'
                    '(jika ada pemain yang mengambil, siapapun itu)!'
        },
        {
            'question': 'Anda punya poin awal 100. Anda menyumbang 10 poin, pemain lainnya masing-masing menyumbang'
                        ' 10 poin. Salah satu pemain mengambil 15 poin. Berapakah total nilai sumbangan?',
            'options': [0, 5, 15, 25, 30],
            'correct': 15,
            'hint': 'Ingat, total sumbangan adalah jumlah poin yang disumbangkan seluruh pemain, dikurangi pengambilan'
                    '(jika ada pemain yang mengambil, siapapun itu)!'
        },
        {
            'question': 'Anda punya poin awal 100. Anda menyumbang 20, pemain lainnya menyumbang masing-masing'
                        ' 10 dan 20 poin. Anda mengambil 5 poin. Berapakah total nilai sumbangan?',
            'options': [0, 15, 25, 35, 45],
            'correct': 45,
            'hint': 'Ingat, total sumbangan adalah jumlah poin yang disumbangkan seluruh pemain, dikurangi pengambilan'
                    '(jika ada pemain yang mengambil, siapapun itu)!'
        },
        {
            'question': 'Anda punya poin awal 100. Anda menyumbang 20, pemain lainnya menyumbang masing-masing'
                        ' 10 dan 20 poin. Tidak ada yang mengambil poin. Angka pengganda adalah 1.5. Berapakah total nilai proyek bersama?',
            'options': [0, 25, 40, 75, 100],
            'correct': 75,
            'hint': 'Ingat, total proyek bersama adalah jumlah poin yang disumbangkan seluruh pemain setelah dikurangi pengambilan'
                    'dan dikalikan dengan angka pengganda ((20+10+20)*1.5=75)'
        },
        {
            'question': 'Anda punya poin awal 100. Anda menyumbang 20, pemain lainnya menyumbang masing-masing'
                        ' 10 dan 20 poin. Salah satu pemain mengambil 20 poin. Angka pengganda adalah 1.5. Berapakah total nilai proyek bersama?',
            'options': [0, 20, 45, 70, 95],
            'correct': 70,
            'hint': 'Ingat, total proyek bersama adalah jumlah poin yang disumbangkan seluruh pemain setelah dikurangi pengambilan'
                    'dan dikalikan dengan angka pengganda ((20+10+20-20)*1.5=45)'
        }
    ]

class RealGameWarning(Page):

    def is_displayed(self):
        return self.subsession.round_number == (self.session.config['num_training_rounds'] + 1)

class InitialWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.subsession.endowment_rule()
        self.group.endow_group()


class Contribute(Page):
    """ Player: How much to contribute in Public Goods (High or Low)"""
    form_model = 'player'
    form_fields = ['choice']
    timer_text = "Waktu yang tersisa di halaman ini:"

    def get_timeout_seconds(self):
        return self.group.timeout

    def choice_max(self):
        return self.group.endowment

    def before_next_page(self):
        self.player.set_contribute()
        if self.timeout_happened:
            self.player.choice = np.random.randint(0,self.session.config['endowment'])


class ContributionWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs1()
        self.group.prob_punishment()

    body_text = "Menunggu peserta lainnya..."

class Embezzlement(Page):
    """ Embezzler: How much to embezzle the public goods"""
    form_model = 'player'
    form_fields = ['amount_embezzled']
    timer_text = "Waktu yang tersisa di halaman ini:"

    def get_timeout_seconds(self):
        return self.group.timeout

    def amount_embezzled_max(self):
        return self.group.total_contribution

    def is_displayed(self):
        return self.player.embezzler == True

    def before_next_page(self):
        self.group.set_payoffs1()


class EmbezzlementWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs2()

    body_text = "Menunggu peserta lainnya..."

class  ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        pass

class Results(Page):
    """Players payoff: How much each has earned"""
    timer_text = "Waktu yang tersisa di halaman ini:"

    def vars_for_template(self):
        return {
            'total_earnings': self.player.payoff,
            'indv_share_project': self.group.social_welfare_embz / Constants.players_per_group,
            'point_left': self.player.endowment - self.player.contribution,
            'fine': self.session.config['punish_fine'],
            'social_cost': (self.group.social_welfare - self.group.social_welfare_embz) * self.session.config[
                'social_cost_multiplier'],

        }

    def get_timeout_seconds(self):
        return self.group.timeout

    def before_next_page(self):
        return self.player.payoff_vector_storage()


page_sequence = [
    Introduction,
    TestQ,
    RealGameWarning,
    InitialWaitPage,
    Contribute,
    ContributionWaitPage,
    Embezzlement,
    EmbezzlementWaitPage,
    ###CaughtPage,
    Results
]