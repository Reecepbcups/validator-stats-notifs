import requests, os, time
import matplotlib.pyplot as plt

# def main():
#     os.makedirs('images', exist_ok=True)
#     for chain in CHAINS:
#         stats = get_stats(CHAINS[chain])
#         make_image(chain, stats, "votingPower", title="Voting Power", yAxis=chain, xAxis="Date")
#         make_image(chain, stats, "uniqueDelegates", title="Unique Delegators", yAxis="Delegators", xAxis="Date")

def get_stats(api_link: str):
    # get current epoch time in seconds based on system time
    response = requests.get(api_link.replace("{EPOCH}", str(int(round(time.time())))))    

    if 'stats' not in response.json().keys():
        return {}

    stats = response.json()['stats']
    # loop through stats & get statDate & votingPower
    data = {}
    for stat in stats:
        data[stat['statDate']] = {
            "votingPower": stat['votingPower'], 
            "uniqueDelegates": stat['uniqueDelegates']
        }
    return data


def convert_number_to_readable(num: int) -> str:
    SIG_FIGS = 3
    if num < 1000:
        return str(num)
    elif num < 1000000:
        return str(round(num / 1000, SIG_FIGS)) + 'K'
    elif num < 1000000000:
        return str(round(num / 1000000, SIG_FIGS)) + 'M'
    elif num < 1000000000000:
        return str(round(num / 1000000000, SIG_FIGS)) + 'B'    
    else:
        return str(round(num / 1000000000000, SIG_FIGS)) + 'T'


def make_image(chain_name, stats, value_key, title="", yAxis="y-axis", xAxis="Date", colors={}):
    # COLORS = {
    #     'LINE': LINE_COLOR,
    #     'CHART_BACKGROUND': CHART_BACKGROUND,
    #     'MAIN_BACKGROUND': MAIN_BACKGROUND
    # }
    os.makedirs('images', exist_ok=True)
    plt.style.use(colors['MAIN_BACKGROUND'])
    fig, ax = plt.subplots()
    L = 6
    ncolors = len(plt.rcParams['axes.prop_cycle'])
    # make the graph wider
    fig.set_size_inches(12, 6)
    ax.ticklabel_format(style='plain')

    y = [obj[value_key] for obj in stats.values()]        
    x = [date.replace("2022-", '') for date in stats.keys()]
        
    # set the plot range as the min and max of the y values
    ax.set_ylim(min(y), max(y)*1.01)

    # plot only every 3 X axis, but every Y
    ax.plot(x[::2], y[::2], '')

    ax.set_xlabel(xAxis)
    ax.set_ylabel(yAxis)
    ax.set_title(title)
    
    ax.title.set_weight('bold')
    ax.xaxis.label.set_weight('bold')
    ax.yaxis.label.set_weight('bold')
    
    ax.title.set_fontsize(20)
    ax.xaxis.label.set_fontsize(15)
    ax.yaxis.label.set_fontsize(15)
    
    ax.lines[0].set_color(colors['LINE'])
    # set background to a dark gray
    ax.set_facecolor(colors['CHART_BACKGROUND'])

    # Change Y axis scalking to be like 1.10M
    plt.gca().set_yticklabels([convert_number_to_readable(x) for x in plt.gca().get_yticks()])

    # save plt.show() as an image to disk, we need this so the bot can grab a link
    plt.savefig(f"images/{chain_name}_{value_key}.png")
    # plt.show()