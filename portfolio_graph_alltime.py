from portfolio_tracker import portfolio_mega_dict, portfolios
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter

# standardize graph colours
COLORS = ["brown", "yellow", "orange", "red"]

# Find latest portfolio value to send along in email
latest_portfolio_value_index = list((portfolio_mega_dict["SIIF"]))[-1]
week_ago_portfolio_value_index = list((portfolio_mega_dict)["SIIF"])[-6]
latest_portfolio_value = (portfolio_mega_dict["SIIF"])[latest_portfolio_value_index]
week_ago_portfolio_value = (portfolio_mega_dict["SIIF"])[week_ago_portfolio_value_index]

#Find the difference to send along in email
percentage_change = ((latest_portfolio_value/week_ago_portfolio_value)-1) * 100

if percentage_change > 0:
    percentage_change_orientation = "up"
else:
    percentage_change_orientation = "down"


# standardized font sizes
SMALL, MED, LARGE, LW = 18, 24, 30, 3
plt.rc('axes', titlesize=MED)    # fontsize of the axes title
plt.rc('axes', labelsize=MED)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL) # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL) # fontsize of the tick labels
plt.rc('legend', fontsize=MED)   # legend fontsize
plt.rc('font', size=LARGE)       # controls default text sizes

# Get a list of the graph dates
graph_dates = list(portfolio_mega_dict["SIIF"].keys())


# Create a dictionary of all portfolios and their relative portfolio close price since the beginning
portfolio_graph_dict = {}
for portfolio in portfolios:
    list_values = list(portfolio_mega_dict[portfolio].values())
    first_value = list_values[0]
    relative_list_values = []
    for price in list_values:
        relative_value = price/first_value
        relative_list_values.append(relative_value)
    portfolio_graph_dict[portfolio] = relative_list_values


# Create graph

fig, ax = plt.subplots()


# Add axes
x = graph_dates

# y-axis data is the relative prices of each portfolio, plot graph using this data and label using portfolio in portfolio_graph_dict
for key, value in portfolio_graph_dict.items():
    chosen_colour = COLORS.pop()
    ax.plot(x, value, label=key, color=chosen_colour, lw=3)

# plot a dashed horizontal axis line
y_line = []
for i in range(len(graph_dates)):
    y_line.append(1)
ax.plot(x, y_line, color = "black", linestyle="dashed", lw=1)

# Define the date form
date_form = DateFormatter('%b-%y')
ax.xaxis.set_major_formatter(date_form)
ax.set_xlim(left=graph_dates[0])

# Set ticks
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))

# Labels and Legend
ax.set_title('Portfolio Performance', fontsize = LARGE)
ax.set_xlabel("Dates")
ax.set_ylabel("Relative Value")
ax.legend(loc="upper left", bbox_to_anchor=(1, 1))

# Set Image Size
fig.set_size_inches((16, 9))

# Remove the top and right lines in the box
ax.spines[['right', 'top']].set_visible(False)

# Save figure to images folder, saved as jpeg due to iOS email issue
fig.savefig("images/portfolio_graph.jpeg", bbox_inches="tight")
