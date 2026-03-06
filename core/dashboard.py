from core.market_briefing import market_briefing
from core.opportunity_ranker import find_best_opportunity
from core.performance import get_performance
from core.strategy_validation import expectancy_analysis, drawdown_analysis
from core.news_filter import is_news_time

import json


def generate_dashboard():

    market = market_briefing()
    opportunity = find_best_opportunity()
    performance = get_performance()
    expectancy = expectancy_analysis()
    drawdown = drawdown_analysis()

    # recent trades
    try:
        with open("data/trade_journal.json") as f:
            trades = json.load(f)
            recent = trades[-2:]
    except:
        recent = []

    news = "HIGH" if is_news_time() else "LOW"

    dashboard = {}

    dashboard["session"] = market["session"]
    dashboard["trend"] = market["trend"]
    dashboard["volatility"] = market["volatility"]

    dashboard["opportunity"] = opportunity

    dashboard["winrate"] = performance["winrate"]
    dashboard["expectancy"] = expectancy["expectancy"]
    dashboard["drawdown"] = drawdown["max_drawdown"]

    dashboard["recent_trades"] = recent

    dashboard["news"] = news

    return dashboard