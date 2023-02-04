import time
import datetime
import pandas as pd

# Create a list of shares owned from a manually created CSV file with Share Ticker and Share Name

ticker_list = []
ticker_list_no_suffix = []

# Delisted shares shouldn't be used for Daily Price Calculations
blacklisted_shares = ['PDL', 'CL1', 'CASH']

owned_shares = pd.read_csv('./data/shares_in_portfolio.csv')
owned_tickers = owned_shares.loc[:, "Share Ticker"]
for ticker in owned_tickers:
    if ticker not in blacklisted_shares:
        ticker_list.append(f'{ticker}.AX')
        ticker_list_no_suffix.append(f'{ticker}')

# Find today's time
todays_date = int(time.mktime(datetime.datetime.now().timetuple())) - 1


# Find date of first investment (08/04/2021 in seconds)
first_investment_date = 1617840000


# Find last week's time by subtracting a week in seconds (604800s)
last_weeks_date = todays_date - 604800
# Choose the interval to retrieve weekly share information
interval = '1d'

# Share return dictionary
share_return_dict = {}
for ticker in owned_tickers:
    if ticker not in blacklisted_shares:
        share_return_dict[ticker] = None

weekly_data = []

# Retrieve weekly share information for each share
for ticker in owned_tickers:
    if ticker not in blacklisted_shares:
        query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}.AX?period1={last_weeks_date}&period2={todays_date}&interval={interval}&events=history&includeAdjustedClose=true'
        df = pd.read_csv(query_string)
        required_data = df.loc[:, ["Date", "Close"]]
        # Yahoo finance duplicates the last date, checks for duplication and removes the last row if it is duplicated
        if required_data.iloc[-1][0] == required_data.iloc[-2][0]:
            required_data = required_data.iloc[:-1,:]
        weekly_data.append(required_data)

        # From this data, calculate the daily return of each share that isn't blacklisted
        # and add it to the share_return_dict dictionary
        todays_value = required_data.iloc[-1][1]
        yesterdays_value = required_data.iloc[-2][1]
        total_return = (todays_value)/(yesterdays_value) - 1
        percentage_return = total_return * 100
        share_return_dict[ticker] = percentage_return