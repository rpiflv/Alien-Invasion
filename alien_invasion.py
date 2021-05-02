import sys
import pygame
import sqlite3
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from time import sleep
from button import Button
from scoreboard import Scoreboard
# from highscores import HighScores


class AlienInvasion:
    """Overall class to manage the app"""

    def __init__(self):

        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        # full screen mode
        # self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)  # self-> ai_game
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self._provide_highscore()
        self.stats = GameStats(self)

        self.play_button = Button(self, "Play")
        self.scoreboard = Scoreboard(self)
        # self.highscores = HighScores(self)

    def _create_fleet(self):
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        ship_height = self.ship.rect.height
        available_space_x = self.settings.screen_width - (2 * alien_width)
        available_space_y = self.settings.screen_height - (3 * alien_height) - ship_height
        number_of_aliens_in_row = available_space_x // (2 * alien_width)

        number_of_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_of_rows):
            for alien_number in range(number_of_aliens_in_row):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien_height * row_number
        self.aliens.add(alien)

    def _check_keydown(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self._provide_highscore()
            self.scoreboard._prep_score()
            self.scoreboard._prep_high_score()
            pygame.mouse.set_visible(False)

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            self.scoreboard.show()

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)
        collision = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collision:
            self.stats.score += self.settings.alien_score
            # self.scoreboard.check_high_score()
            self.scoreboard._prep_score()
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            # self.settings.alien_speed += 0.1

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien._check_edges():
                self._change_fleet_direction()
                break

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
             self._ship_hit()
        self._check_alien_bottom()

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings._fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _fire_bullet(self):
        if len(self.bullets) <= self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def update_screen(self):
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.ship.blitme()
        self.scoreboard.show()
        if not self.stats.game_active:
            self.play_button._draw_button()
        pygame.display.flip()

    def _ship_hit(self):
        # To keep playing in case you still have ships, or new run.
        # In case of high score, store it.
        if self.stats.ships_left > 1:
            self.stats.ships_left -= 1
            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            sleep(1.5)
        else:
            self.add_high_score()
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _provide_highscore(self):

        db = sqlite3.connect("highscores.sqlite")
        cursor = db.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS highscores (name TEXT, score INTEGER)")
        # db.execute('INSERT INTO highscores VALUES ("FLA", 1000000)')
        # db.execute('INSERT INTO highscores VALUES ("ANG", 1500000)')
        # db.execute('INSERT INTO highscores VALUES ("KAL", 500000)')

        for name, score in cursor.execute("SELECT name, MAX(score)  FROM highscores").fetchall():
            return name, score

        cursor.close()
        db.commit()
        db.close()

    def add_high_score(self):
    # storing high score
        if self.stats.score > self.stats.high_score[1]:
            db = sqlite3.connect("highscores.sqlite")
            # self.name = input("Please enter your name: ")
            self.new_high = self.stats.score
            self.scoreboard._prep_high_score()
            # name_input = InputBox # todo need to fix this name value
            self.name = self.input_name()
            add_sql = 'INSERT INTO highscores VALUES (?, ?)'
            db.execute(add_sql, (self.name, self.new_high))
            db.commit()

            db.close()
            # return self.new_high

    def input_name(self):
        rect = pygame.Rect(200, 200, 300, 200)
        FONT = pygame.font.Font("images/ZenDots-Regular.ttf", 50)
        input_rect = pygame.Rect(rect.y + 10, rect.x + 10, rect.width - 20, rect.height - 140)
        text = ''
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        print(text)
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

            self.screen.fill((30, 30, 30))
            title_surface = FONT.render('Enter your name:', True, (195, 195, 195))
            text_surface = FONT.render(text, True, (255, 255, 255))
            title_surface_rect = title_surface.get_rect()
            title_surface_rect.y = rect.y - 100
            title_surface_rect.x = rect.x + 75
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 2)
            pygame.draw.rect(self.screen, (255, 0, 255), input_rect, 2)
            self.screen.blit(title_surface, title_surface_rect)
            self.screen.blit(text_surface, input_rect)
            pygame.display.flip()


    def _check_alien_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit() # same behaviour as ship hit
                break




    def run_game(self):
        """Start the MAIN LOOP"""
        while True:
            self.check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self.update_screen()


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()
