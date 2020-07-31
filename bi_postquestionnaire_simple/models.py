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
    name_in_url = 'bi_postquestionnaire_simple'
    players_per_group = None
    num_rounds = 1
    endo = 25
    with open('bi_postquestionnaire_simple/Ambiguity.csv') as csvFile:
        reader = csv.reader(csvFile)
        Ambiguous_list = [int(i) for i in next(reader)]

class Subsession(BaseSubsession):
    pass

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
    xG_final = models.FloatField()
    xB_final = models.FloatField()
    tG_final = models.FloatField()
    tB_final = models.FloatField()
    payoff_A = models.FloatField()
    payoff_B = models.FloatField()
    payoff_now = models.FloatField()

    # for demographics
    gender = models.StringField(widget=widgets.RadioSelect,
                                label="Pilih Gender Anda",
                                choices=["Pria","Wanita"])
    usia = models.IntegerField(label="Tentukan Usia Anda (Tahun)",
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
    expenditure = models.StringField(widget=widgets.RadioSelect,
                                     label="Rata-rata Pengeluaran Bulanan Anda:",
                                     choices=["Di bawah Rp 500.000",
                                               "Rp 500.001 - Rp 1.000.000",
                                               "Rp 1.000.001 - Rp 1.500.000",
                                               "Rp 1.500.001 - Rp 2.000.000",
                                               "Rp 2.000.001 - Rp 2.500.000",
                                               "Rp 2.500.001 - Rp 3.000.000",
                                               "Di atas Rp 3.000.000",])

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

    def payoff_dataframe(self):
        x = self.participant.vars["p_app_sequence"]
        x["decision_list"] = self.participant.vars['decision_list']
        self.participant.vars["player_dataframe"] = x[x["training"] == False].reset_index()

    def round_selector_code(self):
        self.participant.vars["round_selected"] = self.participant.vars["player_dataframe"].loc[self.round_selector - 1]
        self.participant.vars["x1G_selected"] = self.participant.vars["round_selected"]["x1G"]
        self.participant.vars["x2G_selected"] = self.participant.vars["round_selected"]["x2G"]
        self.participant.vars["x1B_selected"] = self.participant.vars["round_selected"]["x1B"]
        self.participant.vars["x2B_selected"] = self.participant.vars["round_selected"]["x2B"]
        self.participant.vars["t1G_selected"] = self.participant.vars["round_selected"]["t1G"]
        self.participant.vars["t2G_selected"] = self.participant.vars["round_selected"]["t2G"]
        self.participant.vars["t1B_selected"] = self.participant.vars["round_selected"]["t1B"]
        self.participant.vars["t2B_selected"] = self.participant.vars["round_selected"]["t2B"]

    def decision_selector_code(self):
        x = self.participant.vars["round_selected"]
        if x["game_type"] == "risky_setup_1":
            self.participant.vars["allocated_G"] = x["decision_list"][self.decision_selector - 1]
            self.participant.vars["threshold_G"] = list(range(0, 101, 10))[::-1][self.decision_selector - 1]
            self.participant.vars["allocated_B"] = 0
            self.participant.vars["threshold_B"] = 0
        elif x["game_type"] == "risky_setup_2":
            self.participant.vars["allocated_G"] = x["decision_list"][self.decision_selector - 1][0]
            self.participant.vars["threshold_G"] = list(range(0, 81, 10))[::-1][self.decision_selector - 1]
            self.participant.vars["allocated_B"] = x["decision_list"][self.decision_selector - 1][1]
            self.participant.vars["threshold_B"] = list(range(0, 81, 10))[::-1][self.decision_selector - 1]
        elif x["game_type"] == "risky_setup_3_ambi":
            self.participant.vars["allocated_G"] = x["decision_list"][self.decision_selector - 1]
            self.participant.vars["threshold_G"] = list(range(0, 101, 10))[::-1][
                                                       self.decision_selector - 1] + self.unct_selector_G
            self.participant.vars["allocated_B"] = 0
            self.participant.vars["threshold_B"] = 0
        elif x["game_type"] == "risky_setup_4_ambi":
            self.participant.vars["allocated_G"] = x["decision_list"][self.decision_selector - 1][0]
            self.participant.vars["threshold_G"] = list(range(0, 81, 10))[::-1][
                                                       self.decision_selector - 1] + self.unct_selector_G
            self.participant.vars["allocated_B"] = x["decision_list"][self.decision_selector - 1][1]
            self.participant.vars["threshold_B"] = list(range(0, 81, 10))[::-1][
                                                       self.decision_selector - 1] + self.unct_selector_B

    def payment_realization_code(self):
        x = self.participant.vars["round_selected"]
        alloc_G = self.participant.vars["allocated_G"]
        thres_G = self.participant.vars["threshold_G"]
        alloc_B = self.participant.vars["allocated_B"]
        thres_B = self.participant.vars["threshold_B"]
        if x["game_type"] == "risky_setup_1" or x["game_type"] == "risky_setup_3_ambi":
            if self.urn_G <= thres_G:
                self.participant.vars["xG_final"] = self.participant.vars["x1G_selected"]
                self.participant.vars['tG_final'] = self.participant.vars["t1G_selected"]
                self.participant.vars["payoff_1"] = alloc_G * self.participant.vars["x1G_selected"]
            elif self.urn_G > thres_G:
                self.participant.vars["xG_final"] = self.participant.vars["x2G_selected"]
                self.participant.vars['tG_final'] = self.participant.vars["t2G_selected"]
                self.participant.vars["payoff_1"] = alloc_G * self.participant.vars["x2G_selected"]
            self.participant.vars["xB_final"] = 0
            self.participant.vars['tB_final'] = 0
            self.participant.vars["payoff_2"] = 0
            self.participant.vars["payoff_leftover"] = Constants.endo - alloc_G
        elif x["game_type"] == "risky_setup_2" or x["game_type"] == "risky_setup_4_ambi":
            if self.urn_G <= thres_G:
                self.participant.vars["xG_final"] = self.participant.vars["x1G_selected"]
                self.participant.vars['tG_final'] = self.participant.vars["t1G_selected"]
                self.participant.vars["payoff_1"] = alloc_G * self.participant.vars["x1G_selected"]
            elif self.urn_G > thres_G:
                self.participant.vars["xG_final"] = self.participant.vars["x2G_selected"]
                self.participant.vars['tG_final'] = self.participant.vars["t2G_selected"]
                self.participant.vars["payoff_1"] = alloc_G * self.participant.vars["x2G_selected"]
            if self.urn_B <= thres_B:
                self.participant.vars["xB_final"] = self.participant.vars["x1B_selected"]
                self.participant.vars['tB_final'] = self.participant.vars["t1B_selected"]
                self.participant.vars["payoff_2"] = alloc_B * self.participant.vars["x1B_selected"]
            elif self.urn_B > thres_B:
                self.participant.vars["xB_final"] = self.participant.vars["x2B_selected"]
                self.participant.vars['tB_final'] = self.participant.vars["t2B_selected"]
                self.participant.vars["payoff_2"] = alloc_B * self.participant.vars["x2B_selected"]
            self.participant.vars["payoff_leftover"] = Constants.endo - alloc_G - alloc_B
        self.payoff = self.participant.vars["payoff_1"] + self.participant.vars["payoff_2"] + self.participant.vars[
            "payoff_leftover"]
        self.xG_final = self.participant.vars["xG_final"]
        self.xB_final = self.participant.vars["xB_final"]
        self.tG_final = self.participant.vars['tG_final']
        self.tB_final = self.participant.vars['tB_final']
        self.payoff_A = self.participant.vars["payoff_1"]
        self.payoff_B = self.participant.vars["payoff_2"]
        self.payoff_now = self.participant.vars["payoff_leftover"]





























