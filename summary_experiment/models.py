from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from otree.models import Session, Participant


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'summary_experiment'
    players_per_group = 1
    num_rounds = 1


class Subsession(BaseSubsession):

    def vars_for_admin_report(self):

        session1code = Player.session1code
        session1 = Session.objects.get(code=session1code)

        series = session1.vars['series_embz']

        return {
            'highcharts_series': series,
            'round_numbers': list(range(1, Constants.num_rounds + 1))
        }


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    session1code = models.StringField(
        label="Session 1 Code:"
    )
    session2code = models.StringField(
        label="Session 2 Code:"
    )
    session3code = models.StringField(
        label="Session 3 Code:"
    )
