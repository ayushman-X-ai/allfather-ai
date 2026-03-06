# telegram/commands.py

import json

from data.cache import load_cache

from core.performance import get_performance
from core.backtester import run_backtest
from core.monte_carlo import run_monte_carlo
from core.walk_forward import walk_forward

from core.market_briefing import market_briefing
from core.dashboard import generate_dashboard
from core.opportunity_ranker import find_best_opportunity


# ------------------------------------------------
# COMMAND ROUTER
# ------------------------------------------------

def handle_command(command):

    cache = load_cache()

    if command == "/dashboard":
        return dashboard()

    if command == "/market":
        return market_report()

    if command == "/status":
        return market_status(cache)

    if command == "/bias":
        return market_bias(cache)

    if command == "/why":
        return why_no_trade(cache)

    if command == "/performance":
        return performance_report()

    if command == "/journal":
        return journal_report()

    if command == "/backtest":
        return backtest_report()

    if command == "/portfolio":
        return portfolio()

    if command == "/news":
        return news()

    if command == "/risk":
        return risk()

    if command == "/scangold":
        return scan_gold()

    if command == "/scanforex":
        return scan_forex()

    if command == "/opportunity":
        return opportunity()

    if command == "/montecarlo":
        return montecarlo()

    if command == "/walkforward":
        return walkforward()

    if command == "/help":
        return help_message()

    return "Unknown command. Type /help to see available commands."


# ------------------------------------------------
# DASHBOARD
# ------------------------------------------------

def dashboard():

    data = generate_dashboard()

    message = "ALLFATHER Trading Dashboard\n\n"

    message += f"Session: {data['session']}\n"
    message += f"Volatility: {data['volatility']}\n\n"

    message += "Trend Overview\n"

    for t in data["trend"]:
        message += f"{t}\n"

    message += "\nBest Opportunity\n"

    if data["opportunity"]:

        o = data["opportunity"]

        message += (
            f"{o['symbol']} {o['direction']}\n"
            f"Confidence: {o['score']}\n"
        )

    else:
        message += "No strong setup\n"

    message += "\nStrategy Health\n"

    message += (
        f"Winrate: {data['winrate']}%\n"
        f"Expectancy: {data['expectancy']}R\n"
        f"Max Drawdown: {data['drawdown']}\n"
    )

    message += f"\nNews Risk: {data['news']}"

    return message


# ------------------------------------------------
# MARKET BRIEFING
# ------------------------------------------------

def market_report():

    report = market_briefing()

    message = "Market Briefing\n\n"

    message += f"Session: {report['session']}\n\n"

    message += "Trend Overview\n"

    for t in report["trend"]:
        message += f"{t}\n"

    message += f"\nVolatility: {report['volatility']}\n"

    message += "\nBest Setups\n"

    for s in report["setups"]:
        message += f"{s}\n"

    message += f"\nNews Risk: {report['news']}"

    return message


# ------------------------------------------------
# MARKET STATUS
# ------------------------------------------------

def market_status(cache):

    session = cache.get("session", "UNKNOWN")
    regime = cache.get("market_regime", "UNKNOWN")

    return (
        "Market Status\n\n"
        f"Session: {session}\n"
        f"Condition: {regime}"
    )


# ------------------------------------------------
# MARKET BIAS
# ------------------------------------------------

def market_bias(cache):

    bias = cache.get("htf_bias", "UNKNOWN")
    reason = cache.get("bias_reason", "")

    return (
        "Market Bias\n\n"
        f"Direction: {bias}\n"
        f"Reason: {reason}"
    )


# ------------------------------------------------
# WHY NO TRADE
# ------------------------------------------------

def why_no_trade(cache):

    regime = cache.get("market_regime", "UNKNOWN")

    return (
        "Why no trade\n\n"
        f"Market condition: {regime}\n\n"
        "If volatility is low or market is ranging, "
        "the system waits for stronger setups."
    )


# ------------------------------------------------
# STRATEGY PERFORMANCE
# ------------------------------------------------

def performance_report():

    stats = get_performance()

    return (
        "Strategy Performance\n\n"
        f"Trades: {stats['total']}\n"
        f"Wins: {stats['wins']}\n"
        f"Losses: {stats['losses']}\n"
        f"Win rate: {stats['winrate']}%"
    )


# ------------------------------------------------
# TRADE JOURNAL
# ------------------------------------------------

def journal_report():

    try:
        with open("data/trade_journal.json") as f:
            trades = json.load(f)
    except:
        return "No trades recorded yet."

    last = trades[-5:]

    message = "Recent Trades\n\n"

    for t in last:

        message += (
            f"{t['symbol']} {t['direction']}\n"
            f"Entry: {t['entry']}\n"
            f"Stop: {t['stop']}\n\n"
        )

    return message


# ------------------------------------------------
# BACKTEST
# ------------------------------------------------

def backtest_report():

    result = run_backtest()

    return (
        "Backtest Results\n\n"
        f"Trades: {result['total']}\n"
        f"Wins: {result['wins']}\n"
        f"Losses: {result['losses']}\n"
        f"Winrate: {result['winrate']}%"
    )


# ------------------------------------------------
# OPPORTUNITY
# ------------------------------------------------

def opportunity():

    trade = find_best_opportunity()

    if not trade:
        return "No strong opportunity found."

    return (
        "Best Opportunity\n\n"
        f"Asset: {trade['symbol']}\n"
        f"Direction: {trade['direction']}\n\n"
        f"Confidence Score: {trade['score']}\n\n"
        f"Entry: {round(trade['entry'],5)}\n"
        f"Stop: {round(trade['stop'],5)}"
    )


# ------------------------------------------------
# PORTFOLIO
# ------------------------------------------------

def portfolio():

    return (
        "Assets Monitored\n\n"
        "EURUSD\n"
        "XAUUSD (Gold)\n"
        "NAS100\n"
        "US30"
    )


# ------------------------------------------------
# NEWS
# ------------------------------------------------

def news():

    return (
        "Major Economic Events\n\n"
        "CPI\n"
        "NFP\n"
        "FOMC\n"
        "Interest Rate Decisions\n\n"
        "The bot avoids trading during these events."
    )


# ------------------------------------------------
# RISK
# ------------------------------------------------

def risk():

    return (
        "Recommended Risk Rules\n\n"
        "Risk per trade: 1%\n"
        "Max daily risk: 3%\n"
        "Max weekly risk: 6%"
    )


# ------------------------------------------------
# SCANS
# ------------------------------------------------

def scan_gold():
    return "Scanning Gold (XAUUSD) for setups..."


def scan_forex():
    return "Scanning major forex pairs..."


# ------------------------------------------------
# MONTE CARLO
# ------------------------------------------------

def montecarlo():

    r = run_monte_carlo()

    return (
        "Monte Carlo Test\n\n"
        f"Simulations: {r['simulations']}\n"
        f"Average result: {r['average_result']}"
    )


# ------------------------------------------------
# WALK FORWARD
# ------------------------------------------------

def walkforward():

    r = walk_forward()

    return (
        "Walk Forward Test\n\n"
        f"Segments: {r['segments']}\n"
        f"Average winrate: {r['average_winrate']}%"
    )


# ------------------------------------------------
# HELP
# ------------------------------------------------

def help_message():

    return (
        "ALLFATHER Commands\n\n"
        "/dashboard\n"
        "/market\n"
        "/status\n"
        "/bias\n"
        "/why\n"
        "/opportunity\n"
        "/performance\n"
        "/journal\n"
        "/backtest\n"
        "/montecarlo\n"
        "/walkforward\n"
        "/scangold\n"
        "/scanforex\n"
        "/news\n"
        "/risk\n"
        "/portfolio\n"
        "/help"
    )