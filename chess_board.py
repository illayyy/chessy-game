import pygame
import chess

import constants
import chessy
import evaluation_algorithms


def draw_board(n_board, color, mouse_pos, my_name, opponent_name):
    # for each square on the board, draw it with the appropriate color
    # !! in practice only paints the dark squares, light squares are simply made as the background
    for square in chess.SQUARES:
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        x = 30 + file * constants.square_size
        y = (7 - rank) * constants.square_size

        # if the player color is black, flip the y values (flip board across its horizontal axis)
        if not color:
            y = rank * constants.square_size

        # file number + rank number is odd, meaning the square should be colored dark
        if (file + rank) % 2 == 1:
            pygame.draw.rect(chessy.win, constants.board_black, (x, y, constants.square_size, constants.square_size))

        # if there is a piece at the currently selected square, draw it
        if n_board.piece_at(square):
            chessy.win.blit(constants.piece_dict[n_board.piece_at(square).symbol()], (x + 5, y + 5))

    # draw side bar outline
    pygame.draw.rect(chessy.win, constants.darker_gray,
                     (8 * constants.square_size + 30, 0, 10, 800 * constants.square_size))
    pygame.draw.rect(chessy.win, constants.dark_gray,
                     (8 * constants.square_size + 40, 0, 2 * constants.square_size, 8 * constants.square_size))

    draw_eval_bar(n_board)

    # draws side bar and returns the currently hovered over button
    return draw_side_bar(mouse_pos, color, my_name, opponent_name)


def draw_side_bar(mouse_pos, color, my_name, opponent_name):
    font = pygame.font.SysFont("cambria", 22)

    text = font.render(my_name, True, constants.white)
    text_rect = text.get_rect(center=(8 * constants.square_size + 120, chessy.win_height - 28))
    chessy.win.blit(text, text_rect)

    text = font.render(opponent_name, True, constants.white)
    text_rect = text.get_rect(center=(8 * constants.square_size + 120, 28))
    chessy.win.blit(text, text_rect)

    font = pygame.font.SysFont("cambria", 30)

    resign_button_rect = pygame.Rect(8 * constants.square_size + 55, chessy.win_height / 2 - 25, 130, 50)
    pygame.draw.rect(chessy.win, constants.darker_gray, resign_button_rect)

    text = font.render("RESIGN", True, constants.white)
    text_rect = text.get_rect(center=(8 * constants.square_size + 120, chessy.win_height / 2))
    chessy.win.blit(text, text_rect)

    if pygame.Rect.collidepoint(resign_button_rect, mouse_pos):
        return 1
    return 0


def draw_eval_bar(n_board):
    percentage = round(100 * evaluation_algorithms.evaluate_board(n_board, False) / 39 + 50)
    pygame.draw.rect(chessy.win, constants.white, (0, 0, 30, 800))
    pygame.draw.rect(chessy.win, constants.black, (0, 0, 30, percentage * 8))
    pygame.draw.rect(chessy.win, constants.darker_gray, (20, 0, 10, 800 * constants.square_size))


def show_legal_moves(original_square, color, n_board):
    for move in n_board.legal_moves:
        if original_square == move.from_square:
            x = (0.5 + chess.square_file(move.to_square)) * constants.square_size + 30
            y = (7.5 - chess.square_rank(move.to_square)) * constants.square_size
            if not color:
                y = (chess.square_rank(move.to_square) + 0.5) * constants.square_size
            if n_board.piece_at(move.to_square):
                pygame.draw.circle(chessy.win, constants.gray, (x, y), 48, 10)
            else:
                pygame.draw.circle(chessy.win, constants.gray, (x, y), 18)
