'''pygame settings'''

class Settings:
    'A class to store the settings for the stock app.'

    def __init__(self) -> None:
        self.screen_width: int = 1200
        self.screen_height: int = 800
        self.bg_color: tuple[int, int, int] = (230, 230, 230)
