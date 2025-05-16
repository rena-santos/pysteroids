import pygame

import os
import json

from events import *
from constants import * 
from utils import UIText
from gamestatemanager import GameManager, GAME_STATE


class Leaderboard:
    ''

    #{1: [name, score]}
    #{score: name}

    scores = {}

    def save_scores():
        j = json.dumps(Leaderboard.scores)
        with open('scores.json', 'w') as file:
            file.write(j)
        
    def load_scores():
        if not os.path.exists('scores.json'):
            return {}
        
        with open('scores.json', 'r') as file:
            Leaderboard.scores = json.load(file)
        
        return Leaderboard.scores
    
    def add_to_leaderboard(new_score):
        #Add and reorder scores
        x = len(Leaderboard.scores)
        for key in range(1, x+1):
            value = Leaderboard.scores.get(str(key))
            if int(new_score[1]) < int(value[1]):
                continue
            
            Leaderboard.scores[str(key)] = new_score
            new_score = value

        if x < LEADERBOARD_MAX_SIZE:
            x += 1
            Leaderboard.scores[str(x)] = new_score

        Leaderboard.save_scores()


    def draw(screen):
        match GameManager.GAME_STATE:
            case GAME_STATE.SCORE:
                if not hasattr(Leaderboard, "table") or not Leaderboard.table:
                    Leaderboard.load_scores()
                    Leaderboard.table = Leaderboard.create_score_table()
                table_rect = Leaderboard.table.get_rect()
                table_rect.center = [SCREEN_WIDTH/2, SCREEN_HEIGHT/2]
                screen.blit(Leaderboard.table, table_rect)

            case GAME_STATE.COLLECTING_SCORE:
                Leaderboard.collect_score()
                name = UIText(20, GameManager.GAME_SCORE_NAME, position=[SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - BUTTON_HEIGHT])
                name.draw(screen)
                score = UIText(20, str(GameManager.GAME_SCORE), position=[SCREEN_WIDTH/2, SCREEN_HEIGHT/2])
                score.draw(screen)


    def collect_score():
        if not Leaderboard.is_new_highscore():
            GameManager.GAME_STATE = GAME_STATE.OVER

        events = pygame.event.get(pygame.KEYDOWN)
        for event in events:
            if len(GameManager.GAME_SCORE_NAME) < LEADERBOARD_NAME_LIMIT and Leaderboard.is_alpha_key(event.key):
                GameManager.GAME_SCORE_NAME += event.unicode
                print(GameManager.GAME_SCORE_NAME)
            if event.key == pygame.K_BACKSPACE:
                GameManager.GAME_SCORE_NAME = GameManager.GAME_SCORE_NAME[:-1]
            if event.key == pygame.K_RETURN:
                Leaderboard.add_to_leaderboard([GameManager.GAME_SCORE_NAME, GameManager.GAME_SCORE])
                GameManager.GAME_STATE = GAME_STATE.OVER

    def is_new_highscore():
        for score in Leaderboard.scores.values():
            if GameManager.GAME_SCORE >= score[1]:
                return True
            
        return False

    def is_alpha_key(key):
        return (key >= pygame.K_a and key <= pygame.K_z) or (key >= pygame.K_0 and key <= pygame.K_9)

    def create_score_table():
        #Create surface - table
        table_width = SCREEN_WIDTH/2
        table_height = SCREEN_HEIGHT/2
        table = pygame.Surface((table_width, table_height), pygame.SRCALPHA)
        table_rect = table.get_rect()
        table_rect.center = [SCREEN_WIDTH/2, SCREEN_HEIGHT/2]
        font_size = 24
        font_bold = True
        #cell_alignment = 1 #-1.Left | 0.Center | 1.Right
        #last_cell_position = None
        placement_x_pos = 0
        placement_max_width = 0
        name_x_pos = 0
        for key, value in Leaderboard.scores.items():
            font_size, font_bold = Leaderboard.calculate_style(int(key))
            #Create surface - column placement
            placement = UIText(font_size, str(key), bold=font_bold)

            if int(key) == 1:
                placement_x_pos = placement.rendered_surface.get_width()+5
                placement_max_width = placement.rendered_surface.get_width()
                name_x_pos = 20+placement_max_width
            placement.rect.topright = [placement_x_pos, 5]

            #Create surface - column name
            name = UIText(font_size, value[0], bold=font_bold)
            name.rect.topleft = [name_x_pos, 5]
            #Create surface - column score
            score = UIText(font_size, str(value[1]), bold=font_bold)
            score.rect.topright = [SCREEN_WIDTH/2-10, 5]

            row = pygame.Surface((table_width, placement.rendered_surface.get_height()+10), pygame.SRCALPHA)
            row.blits(((placement.rendered_surface, placement.rect), (name.rendered_surface, name.rect), (score.rendered_surface, score.rect)))
            y = row.get_height() * int(key)
            row_rect = row.get_rect()
            row_rect.bottomleft = (0, y)

            table.blit(row, row_rect)

        return table


    def calculate_style(key):
        match key:
            case 1 | 2 | 3:
                bold = True
                if key == 1:
                    size = 24
                elif key == 2:
                    size = 22
                elif key == 3:
                    size = 20
            case _:
                bold = False
                size = 20

        return size, bold
    
    def calculate_cell_position(alignment, last_position):
        #All relative positions inside the Row

        pass

"""     def p_position(rect: pygame.Rect, alignment=1):
        rect.bottomright = [rect.get_width()+5, rect.height+5]
        return [x, y]

    def n_position(rect: pygame.Rect, p_position: pygame.Rect, alignment=1):
        rect.topleft = [5+p_position.rect.topright, 5]
        return [x, y]

    def s_position(alignment, n_position):
        rect.bottomright = [rect.get_width()+5, rect.height+5]
        return [x, y] """