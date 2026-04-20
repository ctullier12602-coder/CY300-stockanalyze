'''watchlist panel'''

from typing import List, Optional

import pygame

class WatchlistPanel:
    'A class to manage the watchlist.'

    def __init__(self, x: int, y: int, font: pygame.font.Font) -> None:
        self.x = x
        self.y = y
        self.font = font
        self.symbols: List[str] = []
        self.filtered_symbols: List[str] = [] # Initialize list of filtered symbols
        self.filter_active = False # Initialize bool for if filter is active

    def update(
            self,
            symbols: List[str],
            filtered_symbols: Optional[List[str]] = None,
            filter_active: bool = False
            ) -> None:
        self.symbols = symbols
        self.filtered_symbols = filtered_symbols or []
        self.filter_active = filter_active # Manage if filter is active or not

    def draw(self, screen: pygame.Surface) -> None:
        title = self.font.render("Watchlist", True, (0, 0, 0)) # Write the title as "Watchlist"
        screen.blit(title, (self.x, self.y)) # Draw title at pos (x,y)

        symbols_to_draw = self.filtered_symbols if self.filter_active else self.symbols # Specify the symbols to draw

        subtitle_text = "Filtered by volatility" if self.filter_active else "All tickers" # Write if filter is active or not
        subtitle = self.font.render(subtitle_text, True, (80, 80, 80))
        screen.blit(subtitle, (self.x, self.y + 28)) # Write the subtitle at pos (x,y)

        for i, symbol in enumerate(symbols_to_draw): # Write the text for each symbol
            text = self.font.render(symbol, True, (60, 60, 60))
            screen.blit(text, (self.x, self.y + 65 + i * 28))
