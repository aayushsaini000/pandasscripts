import pandas as pd
import time
csv_file_name = "daily_trade_report_formatter-%s.csv" % time.strftime("%Y%m%d-%H%M%S")
pd.set_option('display.max_columns', None)

df = pd.read_excel ('Daily_Trade_Report Formatter.xlsx')
total_rows = df['ACCOUNT'].shape[0]
blank_columns = ['Ticker', 'Exchange', 'Route Number', 'Route TIF', 'Route Type', 'Route Comm Amount', 'Route Comm Rate',
                'Execution Broker', 'GTD Date', 'Route Limit Price', 'Route Stop Price', 'Route Net Money', 'JP Comm Amount',
                'JP Tax Amount', 'JP Trade Amount', 'JP Trade Date', 'Settlement Amount', 'User Commission', 'FX_Rate']

odf = pd.DataFrame(columns = ['ROUTE', 'Order Number', 'Ticker', 'Exchange', 'Security Name', 'Route Number', 
                              'Side', 'Route Status', 'Route TIF', 'Route Type', 'Routed Amount', 'Route Filled Amount',
                             'Route Avg Price', 'Account', 'Route Comm Amount', 'Route Comm Rate', 'Route Date',
                              'Route Settlement Date', 'Broker', 'Execution Broker', 'GTD Date', 'Currency', 'CUSIP',
                             'ISIN', 'Route Limit Price', 'Route Stop Price', 'SEDOL', 'Route Net Money', 'JP Comm Amount',
                             'JP Tax Amount', 'JP Trade Amount', 'JP Trade Date', 'Settlement Amount', 'User Commission',
                             'Instructions', 'Net Amount', 'FX_Rate'], index=range(total_rows))

odf['ROUTE'] = 'ROUTE'
odf['Order Number'] = pd.Series([i for i in range(100, 100 + total_rows)])
odf['Security Name'] = df['ISSUE NAME']
odf['Side'] = df['TRAN'].apply(lambda x: 'BY' if x == 'B' else 'SL')
odf['Route Status'] = 'Filled'
odf[blank_columns] = ''
odf['Routed Amount'], odf['Route Filled Amount'] = df['TRN QTY'], df['TRN QTY']
odf['Route Avg Price'] = df['TRADE PRICE']
odf['Account'] = df['ACCOUNT'].apply(lambda x: "EPPW" if x == "9A54" else "WELL")
odf['Route Date'] = df['TRADE_DT']
odf['Route Settlement Date'] = df['SETTLE_DT']
odf['Broker'] = odf['Security Name'].apply(lambda x: "ZZZ" if isinstance(x, str) else "")
odf['Currency'] = df['ISO CURRENCY CD']
odf['CUSIP'] = df['CUSIP']
odf['ISIN'] = df['ISIN']
odf['SEDOL'] = df['SEDOL']
odf['Net Amount'] = df['NET AMT']

def getInstruction(tran, trn_qty, net_amt, trade_price):
    if tran == 'B':
        res = (net_amt-(trn_qty*trade_price))/trn_qty
    else:
        res = (trn_qty*trade_price-net_amt)/trn_qty
    return res
odf['Instructions'] = df.apply(lambda x: getInstruction(x['TRAN'], x['TRN QTY'], x['NET AMT'], x['TRADE PRICE']), axis=1)
odf.to_csv(csv_file_name, index=False)
