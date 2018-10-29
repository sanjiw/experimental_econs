from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import numpy as np


author = 'Sanjiwacika'

doc = """
Real Effort Task - Slider. Get points_exact for accurate answer, points_near for answers within +3 or -3, and 0 for miss.
"""


class Constants(BaseConstants):
    name_in_url = 'slider_effort'
    players_per_group = None
    num_rounds = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    score_player = models.IntegerField()

    def matrixing(self):
        slider_matrix = [self.slider_1, self.slider_2, self.slider_3, self.slider_4, self.slider_5,
                              self.slider_6, self.slider_7, self.slider_8, self.slider_9, self.slider_10,
                              self.slider_11, self.slider_12, self.slider_13, self.slider_14, self.slider_15,
                              self.slider_16, self.slider_17, self.slider_18, self.slider_19, self.slider_20,
                              self.slider_21, self.slider_22, self.slider_23, self.slider_24, self.slider_25,]
        correct_matrix = [98,-71,33,-9,32,-97,18,26,28,-91,65,-69,94,18,3,82,81,53,58,-33,-45,58,93,-31,50]
        value_matrix = list(abs(np.array(slider_matrix) - np.array(correct_matrix)))
        score_matrix = [self.session.config['points_exact'] if i==0 else self.session.config['points_near']
        if i<3 else 0 for i in value_matrix]
        self.score_player = sum(score_matrix)

    test_slider = models.IntegerField(
        label='Masukkan angka 45! (Jika Anda benar menempatkan slider pada angka 45, poin Anda akan bertambah)',
        widget=widgets.Slider,
        default=0, min=-100, max=100)

    slider_1 = models.IntegerField(
        label='Masukkan angka 98!',
        widget=widgets.Slider,
        default=0, min=-100, max=100)

    slider_2 = models.IntegerField(
        label='Masukkan angka -71!',
        widget=widgets.Slider,
        default=0, min=-100, max=100)

    slider_3 = models.IntegerField(
        label='Masukkan angka 33!',
        widget=widgets.Slider,
        default=0, min=-100, max=100)

    slider_4 = models.IntegerField(
        label='Masukkan angka -9!',
        widget=widgets.Slider,
        default=0, min=-100, max=100)

    slider_5 = models.IntegerField(
        label='Masukkan angka -32!',
        widget=widgets.Slider,
        default=0, min=-100, max=100)

    slider_6 = models.IntegerField(
        label='Masukkan angka -97!',
        widget=widgets.Slider,
        default=0, min=-100, max=100)

    slider_7 = models.IntegerField(
        label='Masukkan angka 18!',
        widget=widgets.Slider,
        default=0, min=-100, max=100)

    slider_8 = models.IntegerField(
        label='Masukkan angka 26!',
        widget=widgets.Slider,
        default=0, min=-100, max=100)

    slider_9 = models.IntegerField(
        label='Masukkan angka 28!',
        widget=widgets.Slider,
        default=0, min=-100, max=100)

    slider_10 = models.IntegerField(
        label='Masukkan angka -91!',
        widget=widgets.Slider,
        default=0, min=-100, max=100)

    slider_11 = models.IntegerField(
        label='Masukkan angka 65!',
        widget=widgets.Slider,
        default=0, min=-100, max=100)

    slider_12 = models.IntegerField(
        label='Masukkan angka -69!',
        widget=widgets.Slider,
        default=0, min=-100, max=100)

    slider_13 = models.IntegerField(
        label='Masukkan angka 94!',
        widget=widgets.Slider,
        default=0, min=-100, max=100)

    slider_14 = models.IntegerField(
        label='Masukkan angka 18!',
        widget=widgets.Slider,
        default=0, min=-100, max=100)

    slider_15 = models.IntegerField(
        label='Masukkan angka 3!',
        widget=widgets.Slider,
        default=0, min=-100, max=100)

    slider_16 = models.IntegerField(
        label='Masukkan angka 82!',
        widget=widgets.Slider,
        default=0, min=-100, max=100)

    slider_17 = models.IntegerField(
        label='Masukkan angka 81!',
        widget=widgets.Slider,
        default=0, min=-100, max=100)

    slider_18 = models.IntegerField(
        label='Masukkan angka 53!',
        widget=widgets.Slider,
        default=0, min=-100, max=100)

    slider_19 = models.IntegerField(
        label='Masukkan angka 58!',
        widget=widgets.Slider,
        default=0, min=-100, max=100)

    slider_20 = models.IntegerField(
        label='Masukkan angka -33!',
        widget=widgets.Slider,
        default=0, min=-100, max=100)

    slider_21 = models.IntegerField(
        label='Masukkan angka -45!',
        widget=widgets.Slider,
        default=0, min=-100, max=100)

    slider_22 = models.IntegerField(
        label='Masukkan angka 58!',
        widget=widgets.Slider,
        default=0, min=-100, max=100)

    slider_23 = models.IntegerField(
        label='Masukkan angka 93!',
        widget=widgets.Slider,
        default=0, min=-100, max=100)

    slider_24 = models.IntegerField(
        label='Masukkan angka -31!',
        widget=widgets.Slider,
        default=0, min=-100, max=100)

    slider_25 = models.IntegerField(
        label='Masukkan angka 50!',
        widget=widgets.Slider,
        default=0, min=-100, max=100)