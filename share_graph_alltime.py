from portfolio_tracker import share_df, portfolio_mega_dict
from dailystocktracker import ticker_list_no_suffix
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter

# standardize graph colours
COLORS = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', '#ffe119', '#46f0f0', '#008080',
          '#9a6324', '#808000', '#000075', '#aaffc3', '#000000', '#808080']

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


# Create graph

fig, ax = plt.subplots()

x = graph_dates


# Create a dictionary of all portfolios and their relative portfolio close price since the beginning
share_graph_dict = {}
dashed = 0
for column in share_df:
    if column in ticker_list_no_suffix:
        y = list(share_df[column])
        first_y_value = y[0]
        relative_y_list = []
        for price in y:
            relative_value = price/first_y_value
            relative_y_list.append(relative_value)
        chosen_colour = COLORS.pop(0)
        ax.plot(x, relative_y_list, label=column, color=chosen_colour, lw=3)


# plot a dashed horizontal axis line
y_line = []
for i in range(len(graph_dates)):
    y_line.append(1)
ax.plot(x, y_line, color="black", linestyle="dashed", lw=1)

# Define the date form
date_form = DateFormatter('%b-%y')
ax.xaxis.set_major_formatter(date_form)
ax.set_xlim(left=graph_dates[0])

# Set ticks
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))

# Labels and Legend
ax.set_title('Owned Share Performance', fontsize = LARGE)
ax.set_xlabel("Dates")
ax.set_ylabel("Relative Value")
ax.legend(loc="upper left", bbox_to_anchor=(1, 1))

# Set Image Size
fig.set_size_inches((16, 9))

# Remove the top and right lines in the box
ax.spines[['right', 'top']].set_visible(False)

# Save figure to images folder, saved as jpeg due to iOS email issue
fig.savefig("images/share_graph.jpeg", bbox_inches="tight")
