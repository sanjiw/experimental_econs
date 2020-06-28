from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0.25,
    'participation_fee': 3.00,
    'doc': "",
}

SESSION_CONFIGS = [
    {
        'name': 'bi_experiment',
        'display_name': "BI - Experiment",
        'num_demo_participants': 1,
        'app_sequence': ['bi_introduction','bi_risky_setup_1','bi_postquestionnaire'],
        'use_browser_bots': False
    },
    {
        'name': 'bi_experiment_questionnaire',
        'display_name': "BI - Experiment (Questionnaire Only)",
        'num_demo_participants': 1,
        'app_sequence': ['bi_postquestionnaire'],
        'use_browser_bots': False
    },
    {
        'name': 'pgg_sekar',
        'display_name': "PG Games - Sekar Utami Setiastuti",
        'num_demo_participants': 5,
        'app_sequence': ['pgg_sekar'],
        'use_browser_bots': False
    },
    {
        'name': 'embezzlement_bribery',
        'display_name': "PG Games with Embezzlement and Bribery",
        'num_demo_participants': 3,
        'app_sequence': ['intro_screen', 'embezzlement', 'bribery', 'post_quiz'],
        'treatment': '0',
        'social_cost_multiplier': 1,
        'punishment_prob': 0.15,
        'soc_welf_multiplier': 1.5,
        'num_training_rounds': 3,
        'punish_fine': 25,
        'bribe_threshold': 5,
        'timeout_practice': 15,  ### Set to 'None' if you desire the game without any timeout.
        'timeout_real': 30,
        'endowment': 100,
    },
    {
        'name': 'slider_effort',
        'display_name': "Real Effort Task - Slider",
        'num_demo_participants': 1,
        'app_sequence': ['intro_screen', 'slider_effort'],
        'points_exact': 3,
        'points_near': 1,
    },
    {
        'name': 'embezzlement',
        'display_name': "PG Games with Embezzlement",
        'num_demo_participants': 3,
        'app_sequence': ['embezzlement'],
        'treatment': '2',
        'social_cost_multiplier': 1,
        'punishment_prob': 0.5,
        'soc_welf_multiplier': 1.5,
        'num_training_rounds': 1,
        'punish_fine': 5,
        'timeout_practice': None,  ### Set to 'None' if you desire the game without any timeout.
        'timeout_real': 30,
        'endowment': 40,
    },
    {
        'name': 'bribery',
        'display_name': "PG Games with Bribery",
        'num_demo_participants': 3,
        'app_sequence': ['bribery'],
        'treatment': '2',
        'social_cost_multiplier': 1,
        'punishment_prob': 0.5,
        'soc_welf_multiplier': 1.5,
        'num_training_rounds': 1,
        'punish_fine': 5,
        'bribe_threshold': 28,
        'timeout_practice': None,  ### Set to 'None' if you desire the game without any timeout.
        'timeout_real': 30,
        'endowment': 40,
    },
    {
        'name': 'post_quiz',
        'display_name': "Post Quiz",
        'num_demo_participants': 1,
        'app_sequence': ['post_quiz'],
    },
    {
        'name': 'prisoner',
        'display_name': "Prisoner's Dilemma",
        'num_demo_participants': 4,
        'app_sequence': ['prisoner', 'payment_info'],
    },
    {
        'name': 'utility_elicitation',
        'display_name': "Utility Elicitation",
        'num_demo_participants': 1,
        'app_sequence': ['utility_elicitation'],
        'PE_prospect_max': 100,
        'PE_prospect_min': 0,
        'PE_certainamount': [90, 50, 60, 40, 10, 80, 20, 30, 70],
        'CE_max': 100,
        'CE_min': 0,
        'CE_prob_P': [0.3, 0.9, 0.2, 0.6, 0.5, 0.8, 0.1, 0.7, 0.4],
        'CE_P_points': 100,
        'CE_cP_points': 0,
        'TO_P': 70,
        'TO_Rmin': 20,
        'TO_Rmax': 80,
        'TO_Base': 0,
    },
]
# see the end of this file for the inactive session configs


# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = [
    {
        'name': 'econ101',
        'display_name': 'Econ 101 class',
        'participant_label_file': '_rooms/econ101.txt',
    },
    {
        'name': 'live_demo',
        'display_name': 'Room for live demo (no participant labels)',
    },
    {
        'name': 'pilot_n12',
        'display_name': 'Pilot (n=12)',
        'participant_label_file': '_rooms/pilot_n12.txt'
    },
    {
        'name': 'econs_exp',
        'display_name': 'Experiment (n=42)',
        'participant_label_file': '_rooms/exp_n42.txt'
    }
]


# AUTH_LEVEL:
# this setting controls which parts of your site are freely accessible,
# and which are password protected:
# - If it's not set (the default), then the whole site is freely accessible.
# - If you are launching a study and want visitors to only be able to
#   play your app if you provided them with a start link, set it to STUDY.
# - If you would like to put your site online in public demo mode where
#   anybody can play a demo version of your game, but not access the rest
#   of the admin interface, set it to DEMO.

# for flexibility, you can set it in the environment variable OTREE_AUTH_LEVEL
AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')


# Consider '', None, and '0' to be empty/false
DEBUG = (environ.get('OTREE_PRODUCTION') in {None, '', '0'})

DEMO_PAGE_INTRO_HTML = """
Here are various games implemented with 
oTree. These games are open
source, and you can modify them as you wish.
"""

# don't share this with anybody.
SECRET_KEY = '1ae(_uzt1o$ao0p)(7i*!2(w_a*dopoa4sh!39r!kmbwj-w7-i'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

# inactive session configs
### {
###     'name': 'trust',
###     'display_name': "Trust Game",
###     'num_demo_participants': 2,
###     'app_sequence': ['trust', 'payment_info'],
### },
### {
###     'name': 'prisoner',
###     'display_name': "Prisoner's Dilemma",
###     'num_demo_participants': 2,
###     'app_sequence': ['prisoner', 'payment_info'],
### },
### {
###     'name': 'ultimatum',
###     'display_name': "Ultimatum (randomized: strategy vs. direct response)",
###     'num_demo_participants': 2,
###     'app_sequence': ['ultimatum', 'payment_info'],
### },
### {
###     'name': 'ultimatum_strategy',
###     'display_name': "Ultimatum (strategy method treatment)",
###     'num_demo_participants': 2,
###     'app_sequence': ['ultimatum', 'payment_info'],
###     'use_strategy_method': True,
### },
### {
###     'name': 'ultimatum_non_strategy',
###     'display_name': "Ultimatum (direct response treatment)",
###     'num_demo_participants': 2,
###     'app_sequence': ['ultimatum', 'payment_info'],
###     'use_strategy_method': False,
### },
### {
###     'name': 'vickrey_auction',
###     'display_name': "Vickrey Auction",
###     'num_demo_participants': 3,
###     'app_sequence': ['vickrey_auction', 'payment_info'],
### },
### {
###     'name': 'volunteer_dilemma',
###     'display_name': "Volunteer's Dilemma",
###     'num_demo_participants': 3,
###     'app_sequence': ['volunteer_dilemma', 'payment_info'],
### },
### {
###     'name': 'cournot',
###     'display_name': "Cournot Competition",
###     'num_demo_participants': 2,
###     'app_sequence': [
###         'cournot', 'payment_info'
###     ],
### },
### {
###     'name': 'principal_agent',
###     'display_name': "Principal Agent",
###     'num_demo_participants': 2,
###     'app_sequence': ['principal_agent', 'payment_info'],
### },
### {
###     'name': 'dictator',
###     'display_name': "Dictator Game",
###     'num_demo_participants': 2,
###     'app_sequence': ['dictator', 'payment_info'],
### },
### {
###     'name': 'matching_pennies',
###     'display_name': "Matching Pennies",
###     'num_demo_participants': 2,
###     'app_sequence': [
###         'matching_pennies',
###     ],
### },
### {
###     'name': 'traveler_dilemma',
###     'display_name': "Traveler's Dilemma",
###     'num_demo_participants': 2,
###     'app_sequence': ['traveler_dilemma', 'payment_info'],
### },
### {
###     'name': 'bargaining',
###     'display_name': "Bargaining Game",
###     'num_demo_participants': 2,
###     'app_sequence': ['bargaining', 'payment_info'],
### },
### {
###     'name': 'common_value_auction',
###     'display_name': "Common Value Auction",
###     'num_demo_participants': 3,
###     'app_sequence': ['common_value_auction', 'payment_info'],
### },
### {
###     'name': 'bertrand',
###     'display_name': "Bertrand Competition",
###     'num_demo_participants': 2,
###     'app_sequence': [
###         'bertrand', 'payment_info'
###     ],
### },
### {
###     'name': 'real_effort',
###     'display_name': "Real-effort transcription task",
###     'num_demo_participants': 1,
###     'app_sequence': [
###         'real_effort',
###     ],
### },
### {
###     'name': 'lemon_market',
###     'display_name': "Lemon Market Game",
###     'num_demo_participants': 3,
###     'app_sequence': [
###         'lemon_market', 'payment_info'
###     ],
### },
### {
###     'name': 'public_goods_simple',
###     'display_name': "Public Goods (simple version from tutorial)",
###     'num_demo_participants': 3,
###     'app_sequence': ['public_goods_simple', 'payment_info'],
### },
### {
###     'name': 'trust_simple',
###     'display_name': "Trust Game (simple version from tutorial)",
###     'num_demo_participants': 2,
###     'app_sequence': ['trust_simple'],
### },
