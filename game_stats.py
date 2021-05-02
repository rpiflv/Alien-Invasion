# from alien_invasion import AlienInvasion

class GameStats:
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False

        # self.high_score = ai_game.highscores._provide_highscore()
        self.high_score = ai_game._provide_highscore()


    def reset_stats(self):
        self.score = 0
        self.ships_left = self.settings.ship_limit


