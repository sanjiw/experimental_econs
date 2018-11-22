from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import numpy as np
import json

author = 'Sanjiwacika Wibisana - UGM'

doc = """
Post Quiz
"""


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
    paygame = models.StringField()
    points_rand = models.IntegerField()
    points_A1 = models.IntegerField()
    points_B1 = models.IntegerField()
    result_matrix = models.StringField()
    rand_selector = models.StringField()

    def payoff_rand(self):
        ##### Tuple conversion for all data
        pay_tup_all_rd = list(zip(self.participant.vars['payoff_vct'],self.participant.vars['training'],
                                  self.participant.vars['round_all_vct'],self.participant.vars['game'],
                                  self.participant.vars['round_cut']))
        ##### Exclude all training rounds and oneshots
        pay_tup_rand = [i for i in pay_tup_all_rd if (i[3]=='B2' or i[3]=='A2')]
        ##### Only the oneshots
        oneshot = [i for i in pay_tup_all_rd if (i[3]=='B1' or i[3]=='A1')]
        self.result_matrix = json.dumps(pay_tup_all_rd)
        ##### Payoff round number selector
        self.points_rand = int([i[0] for i in pay_tup_rand if i[3][0]==self.rand_selector[0] and i[4]==int(self.rand_selector[-1])][0])
        self.points_A1 = int(oneshot[0][0])
        self.points_B1 = int(oneshot[1][0])
        ##### Payoff selector
        self.participant.payoff = 0.5*(self.points_rand) + 0.25*(oneshot[0][0]) + 0.25*(oneshot[1][0])


    fullname = models.StringField(
        label='Nama Lengkap:'
    )

    age = models.IntegerField(
        label='Berapakah usia Anda sekarang?',
        widget=widgets.Slider,
        min=13, max=40, default=20)

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
        label='Fakultas:',
        widget=widgets.Select
    )

    seasoned = models.StringField(
        choices=['Pernah','Tidak Pernah'],
        label='Pernahkah Anda menjadi peserta eksperimen ekonomi sebelumnya?'
    )

    dwellings = models.StringField(
        choices=['Sendirian (Kos/Kontrakan bersama)','Bersama Orang Tua','Bersama Saudara Lain','Lainnya'],
        label='Bagaimanakah status tinggal Anda?'
    )

    work_status = models.StringField(
        choices=['Tidak bekerja','Bekerja paruh waktu/Pekerja lepas','Bekerja penuh waktu'],
        label='Apakah status pekerjaan Anda?',
    )

    pocket_money = models.StringField(
        choices=['di bawah Rp 500.000', 'Rp 500.000 s/d Rp 1.500.000', 'Rp 1.500.001 s/d Rp 2.500.000', 'Rp 2.500.001 s/d Rp 3.500.000',
                 'Rp 3.500.001 s/d Rp 4.500.000', 'di atas Rp 4.500.000'],
        label='Berapakah uang saku Anda (di luar biaya kos/rumah) per bulannya?'
    )

    faith = models.IntegerField(
        min=0, max=100, default=0, widget=widgets.Slider,
        label ='Dari skala 0 (sangat tidak taat) hingga 100 (sangat taat), menurut Anda seberapa taatkah Anda dalam menjalankan ritual di agama/keyakinan Anda?'
    )

    moral = models.IntegerField(
        min=0, max=100, default=0, widget=widgets.Slider,
        label='Dari skala 0 (sangat tidak taat) hingga 100 (sangat taat), menurut Anda apakah Anda adalah orang yang menjalankan penuh etika di agama/keyakinan Anda?'
    )

    brothers_rank = models.IntegerField(
        label='Anda adalah anak nomor ke-:'
    )

    brothers_sum = models.IntegerField(
        label='Berapa bersaudarakah Anda? (termasuk Anda):'
    )

    perceived_wealth = models.IntegerField(
        widget=widgets.Slider, min=0, max=100,
        label='Anggap seluruh mahasiswa UGM diwakilkan dalam 100 orang, dari yang paling tidak mampu (0) hingga paling mampu (100).'
              'Jika Anda adalah salah satu dari mahasiswa tersebut, peringkat berapakah Anda?'
    )


