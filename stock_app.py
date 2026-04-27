'''
Interactive stock analysis app.
'''

import sys
from typing import List, Optional

import pygame

from app_button import AppButton
from watchlist_manager import WatchlistManager
from stock_analyzer import StockAnalyzer
from a_data_retriever import DataRetriever
from metric_label import MetricLabel
from rsi import RSI
from price_chart import PriceChart
from watchlist_panel import WatchlistPanel
from settings import Settings


class StockApp:
    '''Overall class to manage display and run the stock analysis.'''

    def __init__(self, initial_ticker: str = "") -> None:
        pygame.init()

        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Stock App")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 30)
        self.small_font = pygame.font.SysFont(None, 24)

        self.current_price = MetricLabel(20, 75, self.font, "Price", (0, 0, 255))
        self.moving_average = MetricLabel(20, 110, self.font, "MA(50)", (0, 150, 0))
        self.rsi = RSI(20, 145, self.font, "RSI")
        self.volatility = MetricLabel(20, 180, self.font, "Volatility", (120, 0, 120))

        self.watchlist = WatchlistPanel(1000, 20, self.font)
        self.price_chart = PriceChart(50, 240, 900, 330)

        self.retriever = DataRetriever()
        self.analyzer = StockAnalyzer(None)
        self.watchlist_manager = WatchlistManager()

        saved_watchlist = self.watchlist_manager.get_watchlist()
        starting_ticker = initial_ticker.strip().upper()
        self.ticker = starting_ticker if starting_ticker else saved_watchlist[0] if saved_watchlist else ""
        self.input_text = ""
        self.status_message = "Type a ticker and press Enter, Search, or click a watchlist item."

        self.volatility_threshold = 0.02
        self.filter_active = False
        self.filtered_watchlist: List[str] = []

        self.input_rect = pygame.Rect(180, 18, 190, 36)
        self.buttons = {
            "search": AppButton(pygame.Rect(385, 18, 85, 36), "Search", self.small_font),
            "add": AppButton(pygame.Rect(485, 18, 120, 36), "Add", self.small_font),
            "remove": AppButton(pygame.Rect(620, 18, 120, 36), "Remove", self.small_font),
            "filter": AppButton(pygame.Rect(755, 18, 125, 36), "Filter", self.small_font),
            "clear": AppButton(pygame.Rect(895, 18, 90, 36), "Clear", self.small_font),
        }

        if self.ticker:
            self.search_ticker(self.ticker, clear_input=True, add_to_watchlist=False)

    def refresh_stock_data(self) -> None:
        '''Pull stock data for the current ticker and connect it to the analyzer.'''
        if not self.ticker:
            self.status_message = "Type a ticker and press Enter."
            return

        if self.retriever.validate_ticker(self.ticker):
            self.analyzer.stock_data = self.retriever.stock_data
            self.status_message = f"Loaded {self.ticker}."
        else:
            self.status_message = f"Could not load ticker: {self.ticker}"

    def search_ticker(
        self,
        ticker: str,
        clear_input: bool = False,
        add_to_watchlist: bool = True,
    ) -> None:
        '''Validate and display a new ticker without restarting the app.'''
        candidate = ticker.strip().upper()
        if not candidate:
            self.status_message = "Please enter a ticker."
            return

        if self.retriever.validate_ticker(candidate):
            self.ticker = candidate
            self.retriever.ticker = self.ticker
            self.analyzer.stock_data = self.retriever.stock_data

            if add_to_watchlist:
                self.watchlist_manager.add_stock(candidate)

            if clear_input:
                self.input_text = ""

            self.status_message = f"Showing {candidate}."
        else:
            self.status_message = f"Ticker not found: {candidate}"

    def add_current_to_watchlist(self) -> None:
        if self.ticker:
            self.watchlist_manager.add_stock(self.ticker)
            self.status_message = f"Added {self.ticker} to watchlist."
        else:
            self.status_message = "Load a ticker before adding to the watchlist."

    def remove_current_from_watchlist(self) -> None:
        if self.ticker:
            self.watchlist_manager.remove_stock(self.ticker)
            self.status_message = f"Removed {self.ticker} from watchlist."
            if self.filter_active:
                self.apply_volatility_filter()
        else:
            self.status_message = "Load a ticker before removing from the watchlist."

    def apply_volatility_filter(self) -> None:
        self.filtered_watchlist = self.watchlist_manager.filter_by_volatility(
            self.retriever,
            self.analyzer,
            self.volatility_threshold,
        )
        self.filter_active = True
        self.refresh_stock_data()
        self.status_message = (
            f"Filter on: volatility > {self.volatility_threshold:.3f}. "
            f"{len(self.filtered_watchlist)} match."
        )

    def clear_filter(self) -> None:
        self.filter_active = False
        self.filtered_watchlist = []
        self.status_message = "Filter cleared."

    def update_display_data(self) -> None:
        '''Update UI elements using current stock data.'''
        if self.retriever.stock_data is None or self.retriever.stock_data.empty:
            self.watchlist.update(
                self.watchlist_manager.get_watchlist(),
                self.filtered_watchlist,
                self.filter_active,
            )
            return

        price = self.retriever.get_current_price()
        ma_series = self.analyzer.calculate_moving_average()
        rsi_series = self.analyzer.calculate_rsi()
        volatility_series = self.analyzer.calculate_volatility()

        self.price_chart.update(self.retriever.stock_data, ma_series, self.ticker)
        self.current_price.update(price)
        self.moving_average.update(self._latest_value(ma_series))
        self.rsi.update(self._latest_value(rsi_series))
        self.volatility.update(self._latest_value(volatility_series), ".4f")

        self.watchlist.update(
            self.watchlist_manager.get_watchlist(),
            self.filtered_watchlist,
            self.filter_active,
        )

    def _latest_value(self, series: Optional[object]) -> Optional[float]:
        if series is None:
            return None
        clean_series = series.dropna()
        if clean_series.empty:
            return None
        return float(clean_series.iloc[-1])

    def _handle_keydown(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_RETURN:
            self.search_ticker(self.input_text, clear_input=True)
        elif event.key == pygame.K_BACKSPACE:
            self.input_text = self.input_text[:-1]
        elif event.key == pygame.K_a:
            self.add_current_to_watchlist()
        elif event.key == pygame.K_d:
            self.remove_current_from_watchlist()
        elif event.key == pygame.K_f:
            self.apply_volatility_filter()
        elif event.key == pygame.K_c:
            self.clear_filter()
        elif event.key == pygame.K_UP:
            self.volatility_threshold += 0.005
            self.status_message = f"Volatility threshold: {self.volatility_threshold:.3f}"
        elif event.key == pygame.K_DOWN:
            self.volatility_threshold = max(0.0, self.volatility_threshold - 0.005)
            self.status_message = f"Volatility threshold: {self.volatility_threshold:.3f}"
        elif event.unicode.isalnum() or event.unicode in ".-":
            self.input_text += event.unicode.upper()

    def _handle_mouse_click(self, event: pygame.event.Event) -> None:
        if self.buttons["search"].is_clicked(event):
            self.search_ticker(self.input_text, clear_input=True)
        elif self.buttons["add"].is_clicked(event):
            self.add_current_to_watchlist()
        elif self.buttons["remove"].is_clicked(event):
            self.remove_current_from_watchlist()
        elif self.buttons["filter"].is_clicked(event):
            self.apply_volatility_filter()
        elif self.buttons["clear"].is_clicked(event):
            self.clear_filter()
        else:
            clicked_symbol = self._watchlist_symbol_at(event.pos)
            if clicked_symbol:
                self.search_ticker(clicked_symbol, clear_input=True, add_to_watchlist=False)

    def _watchlist_symbol_at(self, position: tuple[int, int]) -> Optional[str]:
        symbols = self.filtered_watchlist if self.filter_active else self.watchlist_manager.get_watchlist()
        x, y = position
        if x < self.watchlist.x or x > self.watchlist.x + 150:
            return None

        first_symbol_y = self.watchlist.y + 65
        for index, symbol in enumerate(symbols):
            row_rect = pygame.Rect(self.watchlist.x, first_symbol_y + index * 28, 150, 24)
            if row_rect.collidepoint(x, y):
                return symbol
        return None

    def _draw_input_box(self) -> None:
        label = self.font.render("Ticker:", True, (0, 0, 0))
        self.screen.blit(label, (50, 24))

        pygame.draw.rect(self.screen, (255, 255, 255), self.input_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), self.input_rect, 2)

        input_surface = self.font.render(self.input_text, True, (0, 0, 0))
        self.screen.blit(input_surface, (self.input_rect.x + 8, self.input_rect.y + 6))

        for button in self.buttons.values():
            button.draw(self.screen)

    def _draw_instructions(self) -> None:
        instructions = [
            "Enter/Search = load ticker | click watchlist ticker to switch stocks",
            "A/Add = add current ticker | D/Remove = remove current ticker",
            "F/Filter = apply volatility filter | C/Clear = show all watchlist",
            f"Up/Down = threshold ({self.volatility_threshold:.3f})",
        ]

        y = 610
        for line in instructions:
            text = self.small_font.render(line, True, (40, 40, 40))
            self.screen.blit(text, (50, y))
            y += 24

        status = self.small_font.render(self.status_message, True, (20, 20, 20))
        self.screen.blit(status, (50, 750))

    def run_game(self) -> None:
        '''Start the main loop for the app until the user quits.'''
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self._handle_keydown(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self._handle_mouse_click(event)

            self.update_display_data()

            self.screen.fill(self.settings.bg_color)
            self._draw_input_box()
            self.current_price.draw(self.screen)
            self.moving_average.draw(self.screen)
            self.rsi.draw(self.screen)
            self.volatility.draw(self.screen)
            self.watchlist.draw(self.screen)
            self.price_chart.draw(self.screen)
            self._draw_instructions()

            pygame.display.flip()
            self.clock.tick(60)
