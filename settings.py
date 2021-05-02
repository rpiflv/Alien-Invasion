class Settings:
    """A class with all the functionalities of AI"""
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        self.ship_limit = 1

        # bullet
        self.bullet_height = 15
        self.bullet_width = 3
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 7


        self.speedup_scale = 1.1
        self._fleet_drop_speed = 20
        self.dynamic_settings()




    def dynamic_settings(self):
        self.ship_speed = 1.2
        self.bullet_speed = 1.0
        self.alien_speed = 0.3
        self.alien_score = 50
        # fleet direction -> 1: right, -1: left
        self.fleet_direction = 1

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_score *= self.speedup_scale
