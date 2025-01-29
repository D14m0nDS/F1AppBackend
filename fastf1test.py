import pdb

import fastf1 as ff1
import pandas as pd

session = ff1.get_session(year=2021, gp=2, identifier='FP1')

session.load()
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

print(session.results)