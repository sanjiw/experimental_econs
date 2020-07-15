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
import random
import csv
import json
import pandas as pd
from otree.models_concrete import ParticipantToPlayerLookup, RoomToSession

from otree.common import get_models_module
from otree import common



def get_new_sequence_of_apps(app_sequence):
    the_rest = ['bi_risky_setup_1',
                'bi_risky_setup_2',
                'bi_risky_setup_3_ambi',
                'bi_risky_setup_4_ambi']
    random.shuffle(the_rest)
    app_sequence = [app_sequence[0]] + the_rest + [app_sequence[-1]]
    return app_sequence

def build_participant_to_player_lookups(participant, subsession_app_names, session):
    participant_to_player_lookups = []
    page_index = 0

    for app_name in subsession_app_names:

        views_module = common.get_pages_module(app_name)
        models_module = get_models_module(app_name)
        Constants = models_module.Constants
        Player = models_module.Player

        players_flat = Player.objects.filter(session=session, participant=participant).values(
            'id', 'participant__code', 'participant__id', 'subsession__id',
            'round_number'
        )

        #
        players_by_round = [[] for _ in range(Constants.num_rounds)]
        for p in players_flat:
            players_by_round[p['round_number'] - 1].append(p)
        for round_number, round_players in enumerate(players_by_round, start=1):
            for View in views_module.page_sequence:
                page_index += 1
                for p in round_players:
                    participant_code = p['participant__code']
                    url = View.get_url(
                        participant_code=participant_code,
                        name_in_url=Constants.name_in_url,
                        page_index=page_index
                    )

                    participant_to_player_lookups.append(
                        ParticipantToPlayerLookup(
                            participant_id=p['participant__id'],
                            participant_code=participant_code,
                            page_index=page_index,
                            app_name=app_name,
                            player_pk=p['id'],
                            subsession_pk=p['subsession__id'],
                            session_pk=session.pk,
                            url=url))

    ParticipantToPlayerLookup.objects.bulk_create(
        participant_to_player_lookups
    )

author = 'Putu Sanjiwacika Wibisana'

doc = """
Risky Setup - Green Only
"""


class Constants(BaseConstants):
    name_in_url = 'bi_introduction'
    players_per_group = None
    num_rounds = 1
    with open('bi_introduction/Params.csv') as file:
        params = pd.read_csv(file)


class Subsession(BaseSubsession):

    def creating_session(self):
        for p in self.get_players():
            print('OLD APP SEQ', self.session.config['app_sequence'])
            if not p.sequence_of_apps:
                ParticipantToPlayerLookup.objects.filter(participant=p.participant).delete()
                p.sequence_of_apps = json.dumps(get_new_sequence_of_apps(self.session.config['app_sequence']))
                print(f'SETTING A NEW RANDOM SEQUENCE...:::{p.sequence_of_apps}')
                build_participant_to_player_lookups(p.participant, json.loads(p.sequence_of_apps),
                                                    self.session)

    def cross_app_vars(self):
        self.session.vars['params'] = Constants.params
        for p in self.get_players():
            p.participant.vars['decision_list'] = []
            p.participant.vars['game_type'] = []
            p.participant.vars['x1G'] = []
            p.participant.vars['x2G'] = []
            p.participant.vars['unknown_prob_G'] = []
            p.participant.vars['x1B'] = []
            p.participant.vars['x2B'] = []
            p.participant.vars['unknown_prob_B'] = []
            p.participant.vars['t1G'] = []
            p.participant.vars['t2G'] = []
            p.participant.vars['t1B'] = []
            p.participant.vars['t2B'] = []


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    sequence_of_apps = models.LongStringField()
