'''pygame settings'''

class Settings:
    'A class to store the settings for the stock app.'

    def __init__(self) -> None:
        self.screen_width: int = 1000
        self.screen_height: int = 700
        self.bg_color: tuple[int, int, int] = (230, 230, 230)
