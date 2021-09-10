import openmc
import pandas as pd

sp = openmc.StatePoint('statepoint.10.h5')

tally = sp.get_tally(name='tally_on_sphere_1')
df = tally.get_pandas_dataframe()

pd.options.display.float_format = '{:,.5f}'.format

print(df)
