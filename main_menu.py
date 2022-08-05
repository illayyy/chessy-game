import pygame

import constants
import chessy


def draw_main_menu(mouse_pos, offset, picked_color, username):
    hovering = 0

    for file in range(0, 13):
        for rank in range(0, 8):
            x = file * constants.square_size - 270 + offset
            y = (7 - rank) * constants.square_size
            if (file + rank) % 2 == 1:
                pygame.draw.rect(chessy.win, constants.board_black,
                                 (x, y, constants.square_size, constants.square_size))

    big_font = pygame.font.SysFont("cambria", 95)
    big_text = big_font.render("  CHESSY", True, constants.black)
    outline = big_font.render("  CHESSY", True, constants.white)

    trans = pygame.Surface((1000, 800))
    trans.set_alpha(50)
    trans.fill(constants.darker_gray)
    chessy.win.blit(trans, (0, 0))

    text_rect = big_text.get_rect(center=(constants.square_size * 4 + 3 - 150, chessy.win_height / 2 - 50))
    chessy.win.blit(outline, text_rect)
    text_rect = big_text.get_rect(center=(constants.square_size * 4 - 3 - 150, chessy.win_height / 2 - 50))
    chessy.win.blit(outline, text_rect)
    text_rect = big_text.get_rect(center=(constants.square_size * 4 - 150, chessy.win_height / 2 - 50 + 3))
    chessy.win.blit(outline, text_rect)
    text_rect = big_text.get_rect(center=(constants.square_size * 4 - 150, chessy.win_height / 2 - 50 - 3))
    chessy.win.blit(outline, text_rect)
    text_rect = big_text.get_rect(center=(constants.square_size * 4 - 150, chessy.win_height / 2 - 50))
    chessy.win.blit(big_text, text_rect)

    font = pygame.font.SysFont("cambria", 48)
    pos = chessy.win_height / 2 + 40

    color = constants.black
    dummy_text = font.render("LOCAL", True, constants.black)
    text_rect = dummy_text.get_rect(center=(constants.square_size * 4 - 292, pos))
    if pygame.Rect.collidepoint(text_rect, mouse_pos):
        color = constants.white
        font.italic = True
        hovering = 1
    text = font.render("LOCAL", True, color)
    chessy.win.blit(text, text_rect)

    color = constants.black
    font.italic = False
    dummy_text = font.render("MULTIPLAYER", True, constants.black)
    text_rect = dummy_text.get_rect(center=(constants.square_size * 4 - 212, pos + 60))
    if pygame.Rect.collidepoint(text_rect, mouse_pos):
        color = constants.white
        font.italic = True
        hovering = 2
    text = font.render("MULTIPLAYER", True, color)
    chessy.win.blit(text, text_rect)

    color = constants.black
    font.italic = False
    dummy_text = font.render("RANDY BOT (EASY)", True, constants.black)
    text_rect = dummy_text.get_rect(center=(constants.square_size * 4 - 161, pos + 120))
    if pygame.Rect.collidepoint(text_rect, mouse_pos):
        color = constants.white
        font.italic = True
        hovering = 3
    text = font.render("RANDY BOT (EASY)", True, color)
    chessy.win.blit(text, text_rect)

    color = constants.black
    font.italic = False
    dummy_text = font.render("MIMI BOT (MEDIUM)", True, constants.black)
    text_rect = dummy_text.get_rect(center=(constants.square_size * 4 - 143, pos + 180))
    if pygame.Rect.collidepoint(text_rect, mouse_pos):
        color = constants.white
        font.italic = True
        hovering = 4
    text = font.render("MIMI BOT (MEDIUM)", True, color)
    chessy.win.blit(text, text_rect)

    color = constants.black
    font.italic = False
    dummy_text = font.render("OLLY BOT (DIFFICULT)", True, constants.black)
    text_rect = dummy_text.get_rect(center=(constants.square_size * 4 - 128, pos + 240))
    if pygame.Rect.collidepoint(text_rect, mouse_pos):
        color = constants.white
        font.italic = True
        hovering = 5
    text = font.render("OLLY BOT (DIFFICULT)", True, color)
    chessy.win.blit(text, text_rect)

    font = pygame.font.SysFont("cambria", 40)
    text = font.render("Welcome " + username + "!", True, constants.black)
    text_rect = text.get_rect(center=(500, 40))
    chessy.win.blit(text, text_rect)

    color_picker_rect = pygame.Rect(28, 315, 75, 75)
    if pygame.Rect.collidepoint(color_picker_rect, mouse_pos):
        hovering = 6

    if picked_color:
        icon_color = "P"
    else:
        icon_color = "p"
    chessy.win.blit(constants.piece_dict[icon_color], (22, 306))

    return hovering
