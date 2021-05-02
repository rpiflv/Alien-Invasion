import pygame.font

class Scoreboard:
    def __init__(self, ai_game):
        self.ai_game = None
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        self.text_color = (30, 30, 30)
        self.font = pygame.font.Font("images/ZenDots-Regular.ttf", 22)

        self._prep_score()
        self._prep_high_score()

    def _prep_score(self):
        rounded_score = round(self.stats.score,   - 1)
        score_str = str('{:,}'.format(rounded_score))
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 12

    def show(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_img, self.high_score_rect)
        self.screen.blit(self.high_scorer_img, self.high_scorer_rect)

    def _prep_high_score(self):
        high_score = round(self.stats.high_score[1], -1)
        # high_score = round(self.stats.scoreboard.highest_score)
        high_score_str = str("{:,}".format(high_score))
        high_scorer = self.stats.high_score[0]

        self.high_score_img = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)
        self.high_scorer_img = self.font.render(high_scorer, True, self.text_color, self.settings.bg_color)

        self.high_score_rect = self.high_score_img.get_rect()
        self.high_scorer_rect = self.high_scorer_img.get_rect()

        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

        self.high_scorer_rect.right = self.high_score_rect.left - 15
        self.high_scorer_rect.top = self.high_score_rect.top

