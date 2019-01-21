from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'SW'

doc = """
This is a multi-period public goods game with 5 players.
"""



class Constants(BaseConstants):
    name_in_url = 'pgg_sekar'
    players_per_group = 5
    num_rounds = 2
    endowment = 20
    multiplier = 2


class Subsession(BaseSubsession):
    def creating_session(self):
        pass


class Group(BaseGroup):

    total_token = models.IntegerField()

    def set_payoff(self):
        self.total_token = sum([p.token_contributed for p in self.get_players()])
        for p in self.get_players():
            p.payoff_thisround = ((float(self.total_token)*Constants.multiplier)/Constants.players_per_group) + \
                                 float(Constants.endowment - p.token_contributed)

    def set_final_payoff(self):
        for p in self.get_players():
            pass

class Player(BasePlayer):

    payoff_thisround = models.FloatField()

    token_contributed = models.IntegerField(
        widget=widgets.Slider, default=0,
        min=0, max=Constants.endowment,
        label="How many token(s) do you want to invest?"
    )

    guess_total_token = models.IntegerField(
        widget=widgets.Slider, default=0,
        min=0, max=100,
        label="How many total token(s) do you think were contributed by all members in your group?"
    )

    def payoff_vector_storage(self):
        if self.round_number == 1:
            self.participant.vars['payoff_vct'] = [self.payoff_thisround]
        else:
            self.participant.vars['payoff_vct'].append(self.payoff_thisround)

    def payoff_final(self):
        self.payoff = sum(self.participant.vars['payoff_vct'])