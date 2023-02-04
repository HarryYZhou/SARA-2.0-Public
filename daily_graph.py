from dailystocktracker import ticker_list_no_suffix, weekly_data, required_data
import datetime
import matplotlib.pyplot as plt


# standardize graph colours
COLORS = ["yellow", "orange", "red", "pink", "#Ce8972", "#521c0a"]

# standardized font sizes
SMALL, MED, LARGE, LW = 18, 24, 30, 3
plt.rc('axes', titlesize=MED)    # fontsize of the axes title
plt.rc('axes', labelsize=MED)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL) # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL) # fontsize of the tick labels
plt.rc('legend', fontsize=MED)   # legend fontsize
plt.rc('font', size=LARGE)       # controls default text sizes

# Get a list of the graph dates
graph_dates = list(required_data['Date'])
australian_graph_dates = []


# format
provided_format = '%Y-%m-%d'

# australian_format
australian_format = '%d-%m'

# Convert into Australian date format
for date in graph_dates:
    date_time = datetime.datetime.strptime(date, provided_format)
    string_correct_date = date_time.strftime(australian_format)
    australian_graph_dates.append(string_correct_date)

# Create a dictionary of all tickers and their share price closes over the last 7 days
ticker_dict = {}
for i in range(len(ticker_list_no_suffix)):
    ticker = ticker_list_no_suffix[i]
    ticker_weekly_data = weekly_data[i]
    ticker_weekly_close = list(ticker_weekly_data['Close'])
    # Convert share price closes to relative value of first day in the last week
    ticker_weekly_relative_close = []
    first_price = ticker_weekly_close[0]
    for price in ticker_weekly_close:
        relative_value = price/first_price
        ticker_weekly_relative_close.append(relative_value)
    ticker_dict[ticker] = ticker_weekly_relative_close


# Create x-axis data for graph
x = australian_graph_dates

fig, ax = plt.subplots()

# y-axis data is the prices of each share, plot graph using this data and label using ticker in ticker_dict
# use standardized colours and mix and match dashed/full lines to make it clearer to read
dashed = 0
for ticker, prices in ticker_dict.items():
    if dashed == 0:
        chosen_colour = COLORS[-1]
        style = "solid"
        dashed += 1
    elif dashed == 1:
        chosen_colour = COLORS.pop()
        style = "dashed"
        dashed -= 1
    ax.plot(x, prices, label=ticker, color=chosen_colour, linestyle=style, lw=3)

# Labels and Legend
ax.set_title('Weekly Single Stock Performance', fontsize = LARGE)
ax.set_xlabel("Dates")
ax.set_ylabel("Relative Value")
ax.legend(loc="upper left", bbox_to_anchor=(1, 1))

# Set Image Size
fig.set_size_inches((16, 9))

# Remove the top and right lines in the box
ax.spines[['right', 'top']].set_visible(False)

# Save figure to images folder, saved as jpeg due to iOS email issue
fig.savefig("images/weekly_graph.jpeg", bbox_inches="tight")
