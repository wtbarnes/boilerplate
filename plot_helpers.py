#Name: plot_helpers.py
#Author: Will Barnes
#Date created: 24 November 2015
#Description: Some functions to help in formatting plots

def tick_maker(old_ticks,n):
    """Set n-1 evenly spaced tick marks to make axes look prettier"""

    if n < 2:
        raise ValueError('n must be greater than 1')

    n = n-1
    delta = (old_ticks[-1] - old_ticks[0])/n
    new_ticks = []
    for i in range(n):
        new_ticks.append(old_ticks[0] + i*delta)

    new_ticks.append(old_ticks[0] + n*delta)
    return new_ticks

def my_formatter_2f(x,p):
    """Format tick marks to have 2 significant figures."""
    return "%.2f" % (x)

def my_formatter_1f(x,p):
    """Format tick marks to have 1 significant figure."""
    return "%.1f" % (x)
