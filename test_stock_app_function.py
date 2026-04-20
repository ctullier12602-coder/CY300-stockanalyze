'''
Runs tests to ensure proper functionality
'''

from watchlist_manager import WatchlistManager
from stock_analyzer import StockAnalyzer
from a_data_retriever import DataRetriever
from metric_label import MetricLabel
from rsi import RSI
from price_chart import PriceChart
from watchlist_panel import WatchlistPanel
from settings import Settings
from main_full_project_stock_app import StockApp

'''Test if repeated stocks get properly added to the watchlist'''
def test_add_stock_same_lettercase_and_no_duplicates_in_watchlist(tmp_path): #(ChatGPT, 2026) lines 16-21
    wm = WatchlistManager(tmp_path / "watchlist.txt")
    wm.add_stock(" aapl ")
    wm.add_stock("AAPL")

    assert wm.get_watchlist() == ["AAPL"]

'''Test if watchlist stocks are saved and loaded'''
def test_watchlist_memory_saves_between_managers(tmp_path):
    filename = tmp_path / "watchlist.txt"
    wm = WatchlistManager(filename)
    wm.add_stock("AAPL")
    wm.add_stock("MSFT")

    loaded_wm = WatchlistManager(filename)

    assert loaded_wm.get_watchlist() == ["AAPL", "MSFT"]

'''Test if metric label properly formats label'''
def test_metric_label_formats_value(): #(ChatGPT, 2026) lines 24-28
    label = MetricLabel(0, 0, None, "Test")
    label.update(12.3456)

    assert label.value_text == "12.35"
