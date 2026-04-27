'''Reusable pygame button for stock app controls.'''

import pygame


class AppButton:
    '''Draw and detect clicks for a rectangular UI button.'''

    def __init__(
        self,
        rect: pygame.Rect,
        text: str,
        font: pygame.font.Font,
        bg_color: tuple[int, int, int] = (255, 255, 255),
        text_color: tuple[int, int, int] = (0, 0, 0),
    ) -> None:
        self.rect = rect
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color

    def is_clicked(self, event: pygame.event.Event) -> bool:
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, self.bg_color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)

        label = self.font.render(self.text, True, self.text_color)
        label_rect = label.get_rect(center=self.rect.center)
        screen.blit(label, label_rect)
