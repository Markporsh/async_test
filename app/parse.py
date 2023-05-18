import argparse
from typing import Dict
CHOICES = ('0', '1', 'true', 'false', 'True', 'False', 'y', 'n', 'Y', 'N')
parser = argparse.ArgumentParser(description='Currency converter')
parser.add_argument('--rub', type=float, default=0.0)
parser.add_argument('--usd', type=float, default=0.0)
parser.add_argument('--eur', type=float, default=0.0)
parser.add_argument('--period', type=int, default=1)
parser.add_argument('--debug', type=str, choices=CHOICES, default='false')

args_pars = parser.parse_args()

currency_amounts: Dict[str, float] = {
    'usd': args_pars.usd,
    'eur': args_pars.eur,
    'rub': args_pars.rub,
}