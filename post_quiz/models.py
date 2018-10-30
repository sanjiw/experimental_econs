from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import numpy as np

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


