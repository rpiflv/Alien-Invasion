import pygame.font


class EnterNamePanel:
    def __init__(self, ai_game, cmd):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        self.width, self.height = 800, 600
        self.bg_color = (255, 255, 255)
        self.text_color = (0, 0, 0)
        self.font = pygame.font.Font("images/ZenDots-Regular.ttf", 32)

        self.panel_rect = pygame.Rect(0, 0, self.width, self.height)
        self.panel_rect.center = self.screen_rect.center

        self._prep_cmd_msg(cmd)

    def _prep_cmd_msg(self, cmd):
        self.msg_image = self.font.render(cmd, True, self.text_color, self.bg_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.panel_rect.center

    def _prep_input_box(self):
        self.input_box_rect = pygame.Rect(0, 0, 150, 40)
        self.input_box_rect.center = self.panel_rect.centerx
        self.input_box_rect.bottom = self.panel_rect.bottom - 30

    def draw(self):
        self.screen.fill(self.bg_color, self.panel_rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
        pygame.draw.rect(self.screen, self.text_color, self.input_box_rect, 3)


