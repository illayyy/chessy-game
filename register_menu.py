import pygame

import chessy
import constants


def form(username, password, mouse_pos):
    chessy.win.fill(constants.board_black)

    font = pygame.font.SysFont("cambria", 120)
    big_text = font.render("CHESSY", True, constants.black)
    outline = font.render("CHESSY", True, constants.white)

    text_rect = big_text.get_rect(center=(503, 200))
    chessy.win.blit(outline, text_rect)
    text_rect = big_text.get_rect(center=(497, 200))
    chessy.win.blit(outline, text_rect)
    text_rect = big_text.get_rect(center=(500, 203))
    chessy.win.blit(outline, text_rect)
    text_rect = big_text.get_rect(center=(500, 197))
    chessy.win.blit(outline, text_rect)

    text_rect = big_text.get_rect(center=(500, 200))
    chessy.win.blit(big_text, text_rect)

    username_rect = pygame.Rect(250, 350, 500, 40)
    pygame.draw.rect(chessy.win, constants.board_white, username_rect)
    password_rect = pygame.Rect(250, 450, 500, 40)
    pygame.draw.rect(chessy.win, constants.board_white, password_rect)

    font = pygame.font.SysFont("cambria", 30)

    text = font.render("USERNAME", True, constants.white)
    text_rect = text.get_rect(center=(330, 330))
    chessy.win.blit(text, text_rect)

    text = font.render("PASSWORD", True, constants.white)
    text_rect = text.get_rect(center=(329, 430))
    chessy.win.blit(text, text_rect)

    text = font.render(username, True, constants.black)
    text_rect = text.get_rect(center=(500, 368))
    chessy.win.blit(text, text_rect)

    text = font.render(password, True, constants.black)
    text_rect = text.get_rect(center=(500, 468))
    chessy.win.blit(text, text_rect)

    login_rect = pygame.Rect(325, 550, 150, 40)
    pygame.draw.rect(chessy.win, constants.board_white, login_rect)
    signup_rect = pygame.Rect(525, 550, 150, 40)
    pygame.draw.rect(chessy.win, constants.board_white, signup_rect)

    text = font.render("LOG IN", True, constants.black)
    text_rect = text.get_rect(center=(400, 570))
    chessy.win.blit(text, text_rect)

    text = font.render("SIGN UP", True, constants.black)
    text_rect = text.get_rect(center=(600, 570))
    chessy.win.blit(text, text_rect)

    if username_rect.collidepoint(mouse_pos):
        return 1
    elif password_rect.collidepoint(mouse_pos):
        return 2
    elif login_rect.collidepoint(mouse_pos):
        return 3
    elif signup_rect.collidepoint(mouse_pos):
        return 4
    return 0


def check_valid(string):
    valid_characters = "abcdefghijklmnopqrstuvwxyz" \
                       "ABCDEFGHIJKLMNOPQRSTUVWXYZ" \
                       "1234567890._"
    if len(string) in range(4, 13) and all(char in valid_characters for char in string):
        return True
    return False


def message(msg):
    font = pygame.font.SysFont("cambria", 30)
    if msg[1]:
        text = font.render(msg[0], True, constants.red)
    else:
        text = font.render(msg[0], True, constants.green)
    text_rect = text.get_rect(center=(500, 620))
    chessy.win.blit(text, text_rect)
