'''price chart'''

from typing import List, Optional

import pandas as pd
import pygame

class PriceChart:
    'Draw a stock price and moving average chart.'

    def __init__( # Initialize values.
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        stock_data: Optional[pd.DataFrame] = None
    ) -> None:
        self.x = x
        self.y = y
        self.width = width # Set width/height of chart
        self.height = height
        self.stock_data = stock_data # Initialize stock data to display on chart
        self.ma_series: Optional[pd.Series] = None # If possible, display moving avg series.
        self.ticker = ''
        self.font = pygame.font.SysFont(None, 24) # Specify fonts for chart
        self.title_font = pygame.font.SysFont(None, 32)


    def _make_points( # Define how to draw the points on the chart.
        self,
        values: pd.Series,
        min_val: float,
        max_val: float
    ) -> list[tuple[int, int]]:
        if len(values) < 2: # If less than 2 values, return []
            return []

        points = [] # Initialize points list
        n = len(values)
        for i, val in enumerate(values): # Convert price values into screen points.
            px = self.x + int(i * (self.width / (n - 1))) # Create points to display on graph
            py = self.y + self.height - int(
                ((float(val) - min_val) / (max_val - min_val)) * self.height
            )
            points.append((px, py)) # Add points to list
        return points

    def update(self,
               stock_data: Optional[pd.DataFrame],
               ma_series: Optional[pd.Series],
               ticker: str
               ) -> None: # Update the data to match the graph.
            self.stock_data = stock_data
            self.ma_series = ma_series
            self.ticker = ticker

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect( # Draw chart box.
            screen,
            (245, 245, 245),
            (self.x, self.y, self.width, self.height)
        )
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (self.x, self.y, self.width, self.height),
            2
        )
        # Draw title
        title_text = self.title_font.render(f"{self.ticker} Price Chart", True, (0,0,0))
        screen.blit(title_text, (self.x + self.width // 2 - 90, self.y - 40))

        # Draw axis labels
        y_label = self.font.render("Price ($)", True, (0, 0, 0))
        screen.blit(y_label, (5, self.y + self.height // 2 - y_label.get_height() // 2))

        x_label = self.font.render("Time (Past Year)", True, (0, 0, 0))
        screen.blit(x_label, (self.x + self.width // 2 - 75, self.y + self.height + 10))

        if self.stock_data is None or self.stock_data.empty:
            return # Handle no data

        close_series = self.stock_data['Close'].dropna()
        if len(close_series) < 2:
            return # Handle close series being too short

        combined = close_series.copy()
        if self.ma_series is not None:
            combined = pd.concat([combined, self.ma_series.dropna()]) # Combine the close series w/ moving average

        if combined.empty:
            return

        min_val = float(combined.min())
        max_val = float(combined.max())
        if max_val == min_val:
            max_val += 1.0 # Handle equal crashing

        # Draw close price
        close_points = self._make_points(close_series, min_val, max_val)
        if len(close_points) > 1:
            pygame.draw.lines(screen, (0, 0, 255), False, close_points, 2)

        # Draw moving average (ma)
        if self.ma_series is not None:
            ma_points = self._make_points(self.ma_series.dropna(), min_val, max_val)
            if len(ma_points) > 1:
                pygame.draw.lines(screen, (255, 0, 0), False, ma_points, 2)

        # Draw legend
        legend_x = self.x + self.width - 150
        legend_y = self.y + 10

        # Draw close line
        pygame.draw.line(screen, (0, 0, 255), (legend_x, legend_y), (legend_x + 20, legend_y), 3)
        close_label = self.font.render("Close", True, (0, 0, 0))
        screen.blit(close_label, (legend_x + 30, legend_y - 10))

        # Draw MA line
        pygame.draw.line(screen, (255, 0, 0), (legend_x, legend_y + 25), (legend_x + 20, legend_y + 25), 3)
        ma_label = self.font.render("MA (50)", True, (0, 0, 0))
        screen.blit(ma_label, (legend_x + 30, legend_y + 15))
