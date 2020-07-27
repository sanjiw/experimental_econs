from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

import pandas as pd
import numpy as np
import random

author = 'Your name here'

doc = """
Your app description
"""
import csv

class Constants(BaseConstants):
    name_in_url = 'bi_postquestionnaire'
    players_per_group = None
    num_rounds = 1
    endo = 25
    with open('bi_postquestionnaire/Ambiguity.csv') as csvFile:
        reader = csv.reader(csvFile)
        Ambiguous_list = [int(i) for i in next(reader)]

class Subsession(BaseSubsession):

    def payoff_dataframe(self):
        for p in self.get_players():
            p.participant.vars["player_dataframe"] = pd.DataFrame(list(zip(p.participant.vars['decision_list'],
                                                                           p.participant.vars['game_type'],
                                                                           p.participant.vars['x1G'],
                                                                           p.participant.vars['x2G'],
                                                                           p.participant.vars['unknown_prob_G'],
                                                                           p.participant.vars['x1B'],
                                                                           p.participant.vars['x2B'],
                                                                           p.participant.vars['unknown_prob_B'],
                                                                           p.participant.vars['t1G'],
                                                                           p.participant.vars['t2G'],
                                                                           p.participant.vars['t1B'],
                                                                           p.participant.vars['t2B'])),
                                                                  columns =['decision_list', 'game_type', 'x1G', 'x2G',
                                                                            'unknown_prob_G', 'x1B', 'x2B', 'unknown_prob_B',
                                                                            't1G', 't2G', 't1B', 't2B'])

    def round_selector(self):
        for p in self.get_players():
            p.participant.vars["round_selected"] = p.participant.vars["player_dataframe"].loc[p.round_selector-1]
            p.participant.vars["x1G_selected"] = p.participant.vars["round_selected"]["x1G"]
            p.participant.vars["x2G_selected"] = p.participant.vars["round_selected"]["x2G"]
            p.participant.vars["x1B_selected"] = p.participant.vars["round_selected"]["x1B"]
            p.participant.vars["x2B_selected"] = p.participant.vars["round_selected"]["x2B"]
            p.participant.vars["t1G_selected"] = p.participant.vars["round_selected"]["t1G"]
            p.participant.vars["t2G_selected"] = p.participant.vars["round_selected"]["t2G"]
            p.participant.vars["t1B_selected"] = p.participant.vars["round_selected"]["t1B"]
            p.participant.vars["t2B_selected"] = p.participant.vars["round_selected"]["t2B"]

    def decision_selector(self):
        for p in self.get_players():
            x = p.participant.vars["round_selected"]
            if x["game_type"] == "risky_setup_1":
                p.participant.vars["allocated_G"] = x["decision_list"][p.decision_selector-1]
                p.participant.vars["threshold_G"] = list(range(0, 101, 10))[::-1][p.decision_selector - 1]
                p.participant.vars["allocated_B"] = 0
                p.participant.vars["threshold_B"] = 0
            elif x["game_type"] == "risky_setup_2":
                p.participant.vars["allocated_G"] = x["decision_list"][p.decision_selector - 1][0]
                p.participant.vars["threshold_G"] = list(range(0, 81, 10))[::-1][p.decision_selector - 1]
                p.participant.vars["allocated_B"] = x["decision_list"][p.decision_selector - 1][1]
                p.participant.vars["threshold_B"] = list(range(0, 81, 10))[::-1][p.decision_selector - 1]
            elif x["game_type"] == "risky_setup_3_ambi":
                p.participant.vars["allocated_G"] = x["decision_list"][p.decision_selector - 1]
                p.participant.vars["threshold_G"] = list(range(0, 101, 10))[::-1][p.decision_selector - 1] + p.unct_selector_G
                p.participant.vars["allocated_B"] = 0
                p.participant.vars["threshold_B"] = 0
            elif x["game_type"] == "risky_setup_4_ambi":
                p.participant.vars["allocated_G"] = x["decision_list"][p.decision_selector - 1][0]
                p.participant.vars["threshold_G"] = list(range(0, 81, 10))[::-1][p.decision_selector - 1] + p.unct_selector_G
                p.participant.vars["allocated_B"] = x["decision_list"][p.decision_selector - 1][1]
                p.participant.vars["threshold_B"] = list(range(0, 81, 10))[::-1][p.decision_selector - 1] + p.unct_selector_B

    def payment_realization(self):
        for p in self.get_players():
            x = p.participant.vars["round_selected"]
            alloc_G = p.participant.vars["allocated_G"]
            thres_G = p.participant.vars["threshold_G"]
            alloc_B = p.participant.vars["allocated_B"]
            thres_B = p.participant.vars["threshold_B"]
            if x["game_type"] == "risky_setup_1" or x["game_type"] == "risky_setup_3_ambi":
                if p.urn_G <= thres_G:
                    p.participant.vars["xG_final"] = p.participant.vars["x1G_selected"]
                    p.participant.vars['tG_final'] = p.participant.vars["t1G_selected"]
                    p.participant.vars["payoff_1"] = alloc_G * p.participant.vars["x1G_selected"]
                elif p.urn_G > thres_G:
                    p.participant.vars["xG_final"] = p.participant.vars["x2G_selected"]
                    p.participant.vars['tG_final'] = p.participant.vars["t2G_selected"]
                    p.participant.vars["payoff_1"] = alloc_G * p.participant.vars["x2G_selected"]
                p.participant.vars["payoff_2"] = 0
                p.participant.vars["payoff_leftover"] = Constants.endo - alloc_G
            elif x["game_type"] == "risky_setup_2" or x["game_type"] == "risky_setup_4_ambi":
                if p.urn_G <= thres_G:
                    p.participant.vars["xG_final"] = p.participant.vars["x1G_selected"]
                    p.participant.vars['tG_final'] = p.participant.vars["t1G_selected"]
                    p.participant.vars["payoff_1"] = alloc_G * p.participant.vars["x1G_selected"]
                elif p.urn_G > thres_G:
                    p.participant.vars["xG_final"] = p.participant.vars["x2G_selected"]
                    p.participant.vars['tG_final'] = p.participant.vars["t2G_selected"]
                    p.participant.vars["payoff_1"] = alloc_G * p.participant.vars["x2G_selected"]
                if p.urn_B <= thres_B:
                    p.participant.vars["xB_final"] = p.participant.vars["x1B_selected"]
                    p.participant.vars['tB_final'] = p.participant.vars["t1B_selected"]
                    p.participant.vars["payoff_2"] = alloc_B * p.participant.vars["x1B_selected"]
                elif p.urn_B > thres_B:
                    p.participant.vars["xB_final"] = p.participant.vars["x2B_selected"]
                    p.participant.vars['tB_final'] = p.participant.vars["t2B_selected"]
                    p.participant.vars["payoff_2"] = alloc_B * p.participant.vars["x2B_selected"]
                p.participant.vars["payoff_leftover"] = Constants.endo - alloc_G - alloc_B
            p.payoff = p.participant.vars["payoff_1"] + p.participant.vars["payoff_2"] + p.participant.vars["payoff_leftover"]

class Group(BaseGroup):
    pass

def make_field(label):
    return models.IntegerField(
        choices=[1, 2, 3, 4, 5, 6],
        label=label,
        widget=widgets.RadioSelect,
    )

class Player(BasePlayer):

    # for payments
    round_selector = models.IntegerField()
    decision_selector = models.IntegerField()
    unct_selector_G = models.IntegerField(initial=0)
    unct_selector_B = models.IntegerField(initial=0)
    urn_G = models.IntegerField()
    urn_B = models.IntegerField()

    # for demographics
    gender = models.StringField(widget=widgets.RadioSelect,
                                label="Pilih Gender Anda",
                                choices=["Pria","Wanita"])
    usia = models.IntegerField(label="Tentukan Usia Anda",
                               min=14, max=60)
    bahasa = models.StringField(widget=widgets.RadioSelect,
                                label="Bahasa yang Anda gunakan sehari-hari selain Indonesia",
                                choices=["Jawa", "Sunda", "Melayu", "Bugis/Makassar", "Lainnya"])
    domisili = models.StringField(widget=widgets.RadioSelect,
                                  label="Domisili Anda (6 bulan terakhir yang paling lama ditinggali)",
                                  choices=["DIY", "Pulau Jawa non-DIY","Sumatera","Kalimantan","Sulawesi","Maluku","Papua","Bali-Nusra"])
    exp_experiment = models.IntegerField(label="Berapa kali Anda pernah mengikuti eksperimen sebelum eksperimen ini?",
                                         min=0, max=20)
    studi = models.StringField(widget=widgets.RadioSelect,
                               label="Bidang Studi paling utama Anda:",
                               choices=["Ilmu Alam",
                                        "Teknik",
                                        "Sosial-Budaya",
                                        "Politik-Hukum",
                                        "Ekonomi-Bisnis",
                                        "Psikologi",
                                        "Geografi",
                                        "Filsafat",
                                        "Medis",
                                        "Kehutanan-Pertanian-Perikanan",
                                        "Lainnya"])
    educ = models.StringField(widget=widgets.RadioSelect,
                              label="Jenjang pendidikan Anda sampai saat ini:",
                              choices=["SMA",
                                       "D3",
                                       "D4/S1",
                                       "S2",
                                       "S3",
                                       "Lainnya"])

    # for opinion
    q1_a = make_field("Saya mendukung penggunaan produk ramah lingkungan untuk kebutuhan kamar mandi dan mencuci piring saya; sebagai contoh tisu toilet daur ulang.")
    q1_b = make_field("Saya mendukung penurunan penggunaan energi berbasis fosil; sebagai contoh penggunaan biosolar.")
    q1_c = make_field("Saya mendukung penggunaan produk ramah lingkungan untuk kebutuhan pakaian saya; sebagai contoh membeli second-hand clothes.")
    q1_d = make_field("Saya mendukung penggunaan produk ramah lingkungan untuk industri pertanian; sebagai contoh pupuk organik.")
    q1_e = make_field("Saya mendukung penggunaan produk ramah lingkungan untuk mencuci baju; sebagai contoh deterjen ramah lingkungan.")

    q2_a = make_field("Saya mau menggunakan (dan membayar harganya) produk ramah lingkungan untuk kebutuhan kamar mandi dan mencuci piring saya; sebagai contoh membeli tisu toilet daur ulang.")
    q2_b = make_field("Saya mau (dan membayar harganya) untuk menurunkan konsumsi energi berbasis fosil dan menggantinya dengan energi terbarukan; sebagai contoh membeli biosolar dan menggunakan transportasi publik.")
    q2_c = make_field("Saya mau menggunakan (dan membayar harganya) produk-produk ramah lingkungan untuk kebutuhan fashion saya; sebagai contoh membeli produk tas daur ulang dan baju second-hand.")
    q2_d = make_field("Saya mau (dan membayar harganya) mengkonsumsi makanan organik secara berkala; sebagai contoh mengkonsumsi sehari-hari atau mingguan atau bulanan.")
    q2_e = make_field("Saya mau menggunakan (dan membayar harganya) deterjen dan pemutih ramah lingkungan untuk laundri saya.")

    q3_a = make_field("Penggunaan energi terbarukan (misal: panel surya dan biodiesel) dapat menurunkan risiko kesehatan masyarakat secara signfikan.")
    q3_b = make_field("Peningkatan penggunaan transportasi publik dapat mengurangi kerusakan lingkungan secara signifikan.")
    q3_c = make_field("Peluang untuk terjadinya kerusakan lingkungan dari penggunaan produk daur ulang lebih kecil daripada produk bukan daur ulang.")
    q3_d = make_field("Bahan kimia yang digunakan pada produk ramah lingkungan lebih tidak merusak lingkungan daripada produk bukan ramah lingkungan.")
    q3_e = make_field("Konsumsi makanan organik secara berkala dapat meningkatkan kesehatan dan imunitas saya secara signifikan.")

    q4_a = make_field("Saya pikir penyedia energi di Indonesia (PLN dan Pertamina) memiliki integritas bagus dalam pengelolaan suplai energi melalui sistem ramah lingkungan.")
    q4_b = make_field("Saya yakin bahwa perusahaan yang memproduksi produk ramah lingkungan (misal: kulkas, AC, dan mesin cuci) menggunakan material ramah lingkungan.")
    q4_c = make_field("Saya yakin bahwa kita semua (Anda dan masyarakat) akan menggunakan produk-produk yang lebih ramah lingkungan dalam waktu dekat untuk meningkatkan kesehatan individu.")
    q4_d = make_field("Saya percaya bahwa masyarakat akan melakukan hal-hal yang dibutuhkan untuk mengurangi level polusi di sekitar saya secara khusus dan di Indonesia secara umum.")
    q4_e = make_field("Saya percaya bahwa pemerintah (daerah dan pusat) mempromosikan produk-produk ramah lingkungan dalam waktu dekat untuk meningkatkan kesehatan masyarakat.")





























