import pygame

import chessy
import constants


def display_message(msg, inv):
    font = pygame.font.SysFont("cambria", 80)
    text = font.render(msg, True, constants.black)
    outline = font.render(msg, True, constants.white)
    if inv:
        text, outline = outline, text

    text_rect = text.get_rect(center=(constants.square_size * 4 + 2 + 30, chessy.win_height / 2 - 10))
    chessy.win.blit(outline, text_rect)
    text_rect = text.get_rect(center=(constants.square_size * 4 - 2 + 30, chessy.win_height / 2 - 10))
    chessy.win.blit(outline, text_rect)
    text_rect = text.get_rect(center=(constants.square_size * 4 + 30, chessy.win_height / 2 - 10 + 2))
    chessy.win.blit(outline, text_rect)
    text_rect = text.get_rect(center=(constants.square_size * 4 + 30, chessy.win_height / 2 - 10 - 2))
    chessy.win.blit(outline, text_rect)
    text_rect = text.get_rect(center=(constants.square_size * 4 + 30, chessy.win_height / 2 - 10))
    chessy.win.blit(text, text_rect)


def game_over_message(winner):
    trans = pygame.Surface((800, 800))
    trans.set_alpha(100)
    trans.fill(constants.gray)
    chessy.win.blit(trans, (30, 0))
    if winner:
        display_message("WHITE WON", True)
    elif winner is None:
        display_message("DRAW", False)
    else:
        display_message("BLACK WON", False)


def looking_for_players_message(frame):
    trans = pygame.Surface((800, 800))
    trans.set_alpha(100)
    trans.fill(constants.gray)
    chessy.win.blit(trans, (30, 0))
    txt = "Looking for game."
    if frame > 70:
        txt = "Looking for game.."
    if frame > 140:
        txt = "Looking for game..."
    display_message(txt, True)


def server_error_message():
    trans = pygame.Surface((800, 800))
    trans.set_alpha(100)
    trans.fill(constants.gray)
    chessy.win.blit(trans, (30, 0))
    display_message("SERVER UNAVAILABLE", True)
