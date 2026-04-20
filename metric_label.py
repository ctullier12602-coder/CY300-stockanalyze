'''metric label'''

from typing import List, Optional

import pandas as pd
import pygame

class MetricLabel:
    "Simple text label for a numeric stock metric"

    def __init__(
        self,
        x: int,
        y: int,
        font: pygame.font.Font,
        label: str,
        color: tuple[int, int, int] = (0, 0, 0),
    ) -> None:
        self.x = x # X/Y coordinates for where the label will be on the screen
        self.y = y
        self.font = font
        self.label = label # Label name ('RSI', 'Price', etc.)
        self.color = color
        self.value_text = "--" # Placeholder for None data

    def update(self, value: Optional[float], fmt: str = ".2f") -> None:
        """
        Update the displayed value:
        - If value is None or NaN → show "--"
        - Otherwise format the number as a string
        """
        if value is None or pd.isna(value):
            self.value_text = "--"
        else:
            self.value_text = format(float(value), fmt) # Format numeric value using given format

    def draw(self, screen: pygame.Surface) -> None:
        """
        Render and draw the label + value onto the screen
        """
        text = self.font.render( # Create text surface w/ label and current vals
            f"{self.label}: {self.value_text}", True, self.color
        )
        screen.blit(text, (self.x, self.y)) # Draw text at specified (x,y) position
