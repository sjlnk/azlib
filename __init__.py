import re
import numpy as np


def sma(x, period):
    weigths = np.repeat(1.0, period) / period
    # TODO: figure out what np.convolve actually does (mathematical education)
    ma = np.convolve(x, weigths, 'valid')
    # append some nans to make the result match the length of x
    return np.hstack([np.repeat(np.nan, period - 1), ma])


def feq(a, b, e=1e-8):
    if abs(a-b) < e:
        return True
    else:
        return False


# more accurate than feq (but possibly slower)
def feqd(a, b, e=1e-14):
    return abs(1 - a / b) < e
    

def dump(obj):
    for attr in dir(obj):
        if not (len(attr) > 4 and attr[0:2] == '__' and attr[-2:] == '__') and hasattr( obj, attr ):
            print("{}: {}".format(attr, getattr(obj, attr)))


def globber(s, choices):
    candidates = []
    s_re = s.replace("*", ".*").replace("?", ".")
    s_re = "\\b" + s_re + "\\b"
    for x in choices:
        if re.search(s_re, x):
            candidates.append(x)
    return candidates


def sharpe_ratio(changes, rfrate_yearly, period=252):
    """
    Calculates Sharpe ratio.
    Periods:
        252 = daily
        12 = monthly
    """
    rfrate_per_day = rfrate_yearly ** (1/period) - 1
    excess_returns = changes - rfrate_per_day
    std_excess_return = np.std(excess_returns)
    avg_excess_return = np.mean(excess_returns)
    dailysharpe = avg_excess_return / std_excess_return
    annualized = dailysharpe * np.sqrt(period)
    return annualized


def sortino_ratio(changes, trate_yearly, period=252):
    """
    Calculates Sortino ratio.
    Periods:
        252 = daily
        12 = monthly
    """
    trate_per_day = trate_yearly ** (1/period) - 1
    excess_returns = changes - trate_per_day
    avg_excess_return = np.mean(excess_returns)
    minus_exc_returns_squared = excess_returns[excess_returns < 0] ** 2
    downside_risk = np.sqrt(np.sum(minus_exc_returns_squared) / len(excess_returns))
    dailysortino = avg_excess_return / downside_risk
    annualized = dailysortino * np.sqrt(period)
    return annualized