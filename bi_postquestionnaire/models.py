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


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'bi_postquestionnaire'
    players_per_group = None
    num_rounds = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

def make_field(label):
    return models.IntegerField(
        choices=[1,2,3,4,5,6],
        label=label,
        widget=widgets.RadioSelect,
    )

class Player(BasePlayer):
    q1_a = make_field("I support the use of eco-friendly products for toiletries and washing dishes; e.g., recycled toilet paper.")
    q1_b = make_field("I support to reduce the use of fossil energy; e.g., switch to renewable energy.")
    q1_c = make_field("I support using the eco-friendly products for fashion; e.g., reused clothes.")
    q1_d = make_field("I support using the eco-friendly products for agricultural industry (e.g., organic fertiliser).")
    q1_e = make_field("I support using the eco-friendly products for laundrette (e.g., detergent).")
    q2_a = make_field("I would be willing to use (pay the price) the green products for my toiletries and washing dishes; e.g., recycled toilet paper, eco-friendly dishwasher and eco-friendly dish soap.")
    q2_b = make_field("I would be willing to reduce fossil energy consumption and to switch to renewable energy; e.g., use more public transport and use solar panel.")
    q2_c = make_field("I would be willing to use (pay the price) any kinds of green product for my fashion; e.g., recycled and reused clothes.")
    q2_d = make_field("I would be willing to consume organic food in a regular basis; e.g., daily, or weekly or monthly shopping for organic food/groceries.")
    q2_e = make_field("I would be willing to use (pay the price) eco-friendly detergent and eco-friendly whitener for my laundrette.")
    q3_a = make_field("The use of renewable energy (e.g. solar panel or biodiesel) can significantly reduce the risk of public health.")
    q3_b = make_field("An increase use of public transport can significantly reduce the environmental damages.")
    q3_c = make_field("The environmental damages from using recycled and reused products is significantly less than using newly-branded clothes.")
    q3_d = make_field("Chemical products used in eco products are significantly less harmful to the environment than that of non-eco-friendly products.")
    q3_e = make_field("Consuming organic foods in a regular basis can significantly increase my health and immune.")
    q4_a = make_field("I think the energy providers in Indonesia (PLN and Pertamina) have good intentions in managing country’s energy supply with an eco-friendly system.")
    q4_b = make_field("I believe companies that produce eco-friendly products (e.g., refrigerator, AC and dishwasher) use environment-friendly materials.")
    q4_c = make_field("I believe we will all move on to use more green products in the near future for a better individual health.")
    q4_d = make_field("I trust public to do anything necessary to reduce the pollution level in my area and country.")
    q4_e = make_field("I trust the government (both central and local) to promote more green products in the near future for a better public health.")





























