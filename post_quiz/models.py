from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import numpy as np


class Constants(BaseConstants):
    name_in_url = 'post_quiz'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    payround = models.IntegerField()

    def payoff_rand(self):
        ##### Tuple conversion for all data
        pay_tup_all_rd = list(zip(self.participant.vars['payoff_vct'],self.participant.vars['training'],self.participant.vars['round_all_vct']))
        ##### Exclude all training rounds
        pay_tup_only_paid = [i for i in pay_tup_all_rd if i[1]==False]
        ##### Randomizer local var
        sel = np.random.randint(1, len(pay_tup_only_paid)) - 1
        ##### Payoff round number selector
        self.payround = pay_tup_only_paid[sel][2]
        ##### Payoff selector
        self.participant.payoff = pay_tup_only_paid[sel][0]

    fullname = models.StringField(
        label='Nama Lengkap:'
    )

    age = models.IntegerField(
        label='Berapakah usia Anda sekarang?',
        widget=widgets.Slider,
        min=13, max=40)

    year_entry = models.IntegerField(
        min=2000, max=2018,
        label='Angkatan:'
    )

    gender = models.StringField(
        choices=['Pria', 'Wanita'],
        label='Jenis Kelamin',
        widget=widgets.RadioSelectHorizontal)

    faculty = models.StringField(
        choices=['Biologi','Ekonomika dan Bisnis','Farmasi','Filsafat','Geografi','Hukum',
                 'Ilmu Budaya','FISIPOL','Kedokteran Gigi','Kedokteran Hewan','FKKMK',
                 'Kehutanan','FMIPA','Pertanian','Peternakan','Psikologi','Teknik',
                 'Teknologi Pertanian','Sekolah Pascasarjana','Sekolah Vokasi'],
        label='Fakultas',
        widget=widgets.Select
    )

    seasoned = models.StringField(
        choices=['Pernah','Tidak Pernah'],
        label='Pernahkah anda menjadi peserta eksperimen ekonomi sebelumnya?'
    )

    perceived_wealth = models.IntegerField(
        widget=widgets.Slider, min=0, max=100,
        label='Anggap seluruh mahasiswa UGM diwakilkan dalam 100 orang, dari yang paling tidak mampu (0) hingga paling mampu (100).'
              'Jika Anda adalah salah satu dari mahasiswa tersebut, peringkat berapakah Anda?'
    )
    subjective_probability = models.IntegerField(
        widget=widgets.Slider, min=0, max=100,
        label='Menurut anda, berapa peluang (peluang) anda untuk ditangkap'
    )

