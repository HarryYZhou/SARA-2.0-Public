import datetime as dt
import pandas as pd
import yfinance as yf

blacklisted_shares = ['CL1', 'CASH']

# Need to find the daily portfolio value for portfolio
portfolios = ['SIIF', 'NDQ', 'A200']

today = dt.datetime.today()
start_stocks = dt.datetime(2021, 4, 22)

portfolio_mega_dict = {}
share_dict_list = []

for portfolio in portfolios:
    # Extract share data from CSV file
    transactions_df = pd.read_csv(f'./data/portfolios/{portfolio}.csv')

    # Convert date to datetime objects
    transactions_df["date"] = pd.to_datetime(transactions_df["date"], format="%d/%m/%Y")
    transactions_df["date"] = transactions_df["date"].dt.date

    # Ticker_list
    ticker_list = []

    # Code_list
    code_list = []

    # Find all share transactions as well as relevant dates and tickers from dataframe
    sell_share_transactions = transactions_df.loc[transactions_df['type'] == "Sell"]
    buy_share_transactions = transactions_df.loc[transactions_df['type'] == "Buy"]
    share_tickers_df = transactions_df.loc[:, "ticker"]
    for ticker in share_tickers_df:
        if ticker not in blacklisted_shares and ticker not in ticker_list:
            ticker_list.append(ticker)
    for ticker in ticker_list:
        code_list.append(f'{ticker}.AX')

    # Find daily stock price data
    data = yf.download(code_list, start=start_stocks, end=today, interval='1d')
    daily_stock_data = data["Close"]

    # Reset the index of the stock data so we don't get issues with duplicate dates
    new_daily_stock_data = daily_stock_data.reset_index()
    new_daily_stock_data["Date"] = new_daily_stock_data["Date"].dt.date

    # Remove NaN values and change them to Zero to avoid calculation errors
    new_daily_stock_data.fillna(0, inplace=True)

    # Store the dates that need to be used to find daily portfolio values
    start_date = new_daily_stock_data["Date"][0]
    list_date = [date for date in new_daily_stock_data["Date"]]

    portfolio_dict = {}

    for date in list_date:
        # We need to find the cumulative amounts of each unit held at the date, and the price of the unit on the portfolio valuation date
        end_date = date
        mask = (transactions_df["date"] >= start_date) & (transactions_df["date"] <= end_date)


        # Filter rows in transactions file by date
        transactions_filtered = transactions_df.loc[mask]

        # Find the cumulative holdings of each units at transaction date (excluding blacklisted shares)
        transactions_information = transactions_filtered.loc[:, ["date", "type", "ticker", "quantity"]]

        # Separate them into buy and sell
        mask = ["Buy", "Sell"]
        buy_sell_transactions = transactions_information.loc[transactions_df["type"].isin(mask)]

        # Make a dictionary to store cumulative units
        unit_dict = {}

        buy_sell_transactions.reset_index(drop=True, inplace=True)
        # Reset the index of buy_sell_transactions so we can iterate over it with a for loop
        for i in range(len(buy_sell_transactions)):
            if buy_sell_transactions.loc[i, "ticker"] not in blacklisted_shares:
                if buy_sell_transactions.loc[i, "ticker"] not in unit_dict:
                    unit_dict[buy_sell_transactions.loc[i, "ticker"]] = buy_sell_transactions.loc[i, "quantity"]
                else:
                    if buy_sell_transactions.loc[i, "type"] == "Buy":
                        unit_dict[buy_sell_transactions.loc[i, "ticker"]] += buy_sell_transactions.loc[i, "quantity"]
                    else:
                        unit_dict[buy_sell_transactions.loc[i, "ticker"]] -= buy_sell_transactions.loc[i, "quantity"]


        daily_stock_prices = new_daily_stock_data.loc[new_daily_stock_data["Date"] == end_date]

        daily_stock_prices_excluding_date = daily_stock_prices.drop(["Date"], axis="columns")
        # Rename portfolios with a single share (i.e. the comparison NDQ portfolio)
        for column in daily_stock_prices_excluding_date:
            if column == "Close":
                daily_stock_prices_excluding_date.rename(columns={'Close': f'{code_list[0]}'}, inplace=True)

        daily_price_dict = {}
        for column in daily_stock_prices_excluding_date:
            # Remove the AX to standardise the price and unit dictionaries
            daily_price_dict[column[:-3]] = daily_stock_prices_excluding_date[column].values[0]

        #After we have a dict of prices and cumulative units, we can finally find the daily portfolio value without cash flows
        daily_portfolio_share_value = 0

        if unit_dict == None:
            daily_portfolio_share_value = 0
        else:
            for key in unit_dict:
                share_value = unit_dict[key] * daily_price_dict[key]
                daily_portfolio_share_value += share_value

        cash_flow = 0
        # Now, I have to add the cumulative cash flows to the final date to find the total daily portfolio value including cash
        transactions_cash_flows = transactions_filtered.loc[:, ["date", "type", "cashflow"]]
        transactions_cash_flows.reset_index(drop=True, inplace=True)
        for i in range(len(transactions_cash_flows)):
            cash_flow += transactions_cash_flows.loc[i, "cashflow"]


        daily_portfolio_value = 0

        daily_portfolio_value += (cash_flow + daily_portfolio_share_value)

        portfolio_dict[end_date] = daily_portfolio_value

        # Add the share date, values and unit holdings for the share mega dict

        if portfolio == "SIIF":
            share_dict_list.append(daily_price_dict)

    portfolio_mega_dict[portfolio] = portfolio_dict

# Make a share price dataframe
share_df = pd.DataFrame(share_dict_list)



