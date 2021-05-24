import pandas as pd
pd.set_option('display.max_columns', None)

df = pd.read_excel ('Book1.xlsx')

td_df = df.loc[df["Brkr"] == 'TD']

td_df.loc[((td_df['Cusip'].str.startswith("8911")) | ((td_df['SetDt'] == td_df['Issue Dt']) & (td_df['Side']=='B'))), ["Brkr"]] = 'TDSB'

td_df.loc[td_df['Brkr'] != 'TDSB', ['Brkr']] = "TDBB"

td_df.to_csv('book_filter.csv', index=False)
