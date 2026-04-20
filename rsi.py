'''RSI'''

import pygame

from metric_label import MetricLabel

class RSI(MetricLabel):
    """
    Specialized MetricLabel for RSI that changes color based on value:
    - Red   → Overbought (> 70)
    - Green → Oversold (< 30)
    - Blue  → Neutral
    """
    def draw(self, screen: pygame.Surface) -> None:
        try: # Try converting displayed text to a numeric value
            numeric_value = float(self.value_text)
        except ValueError: # Handle exception
            numeric_value = None

        if numeric_value is None:
            color = (0, 0, 0) # Default color when no data
        elif numeric_value > 70:
            color = (255, 0, 0) # Red for overbought
        elif numeric_value < 30:
            color = (0, 160, 0) # Green for oversold
        else:
            color = (0, 0, 255) # Blue for neutral

        text = self.font.render(f"{self.label}: {self.value_text}", True, color) # Render text
        screen.blit(text, (self.x, self.y)) # Draw at specified position


