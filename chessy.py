import chess
import pygame
import math
import time
import socket

import constants
import main_menu
import chess_board
import evaluation_algorithms
import messages
import register_menu

win_width = 10 * constants.square_size
win_height = 8 * constants.square_size
win = pygame.display.set_mode([win_width, win_height])

pygame.display.set_caption("Chessy")
pygame.display.set_icon(constants.pawn_white)
board = chess.Board("8/8/8/8/8/8/8/8 w - - 0 1")

IP = "127.0.0.1"
PORT = 59920


def hovering_square(pos, color):
    x = math.floor((pos[0] - 30) / constants.square_size)
    y = 7 - math.floor(pos[1] / constants.square_size)
    if not color:
        y = math.floor(pos[1] / constants.square_size)
    return y * 8 + x


def find_sound(n_board, move):
    if n_board.is_capture(move):
        play_sound = constants.sound_capture
    elif n_board.is_castling(move):
        play_sound = constants.sound_castle
    else:
        play_sound = constants.sound_move

    return play_sound


def game(game_mode, color, username):
    # server variables
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.setblocking(False)
    my_socket.settimeout(60000)
    status = "disconnected"
    frame = 0

    # players names
    opponent_name = my_name = username.upper()
    if game_mode == 2:
        opponent_name = ""

    # game variables
    start_wait = not color  # bot opponents only - if the player plays black (last), wait a moment before making a move
    turn = True  # white goes first
    my_color = color
    selected_piece = -1  # no piece is selected
    hovering_button = 0
    resigned = None

    # sound variables
    stop_sound = False
    play_sound = constants.sound_silence
    if game_mode != 2:
        pygame.mixer.Sound.play(constants.sound_start)  # plays start sound

    # initialize board and pygame
    board.reset()
    running = True
    pygame.init()
    while running:
        # single player
        if game_mode == 1:
            for event in pygame.event.get():
                # player has quit the game
                if event.type == pygame.QUIT:
                    running = False
                # player has clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # if the game is over, return false for game() and return to main menu
                    if stop_sound:
                        return False
                    # if the player is hovering over the resign button, resign
                    elif hovering_button != 0:
                        resigned = turn

                    # player has clicked within the bounds of the chess board
                    if mouse_pos[0] < 830:
                        # the player currently has a piece selected
                        if selected_piece != -1:
                            move = chess.Move(selected_piece, hovering_square(mouse_pos, my_color))

                            # pawn promotion if reached eighth rank
                            if board.piece_type_at(selected_piece) == chess.PAWN \
                                    and (move.to_square in range(0, 8) or move.to_square in range(56, 64)):
                                move.promotion = chess.QUEEN

                            # if the move is legal, make it
                            if move in board.legal_moves:
                                board.push(move)

                                # play appropriate sound and switch turns with opponent
                                play_sound = find_sound(board, move)
                                turn = not turn

                            # regardless of whether the move has been made or not, deselect the piece
                            selected_piece = -1

                        # the player currently has no piece selected
                        elif board.color_at(hovering_square(mouse_pos, my_color)) == turn and selected_piece == -1:
                            # select the piece currently hovered over
                            selected_piece = hovering_square(mouse_pos, my_color)

        # online multiplayer
        elif game_mode == 2:
            # attempt connection to the server
            if status == "disconnected":
                try:
                    my_socket.connect((IP, PORT))
                except socket.error:
                    return False
                my_socket.send("connect".encode())
                status = my_socket.recv(1024).decode()

                if status == "name":
                    my_socket.send(my_name.encode())
                    status = my_socket.recv(1024).decode()

            # wait for game to begin
            elif status == "connected":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                my_socket.settimeout(0.001)
                try:
                    msg = my_socket.recv(1024).decode()
                    if msg == "white":
                        my_color = True
                    else:
                        my_color = False
                    my_socket.settimeout(60000)
                except socket.error:
                    pass
                else:
                    my_socket.send(my_name.encode())
                    opponent_name = my_socket.recv(1024).decode()
                    my_socket.send("ok".encode())
                    status = my_socket.recv(1024).decode()

                    pygame.mixer.Sound.play(constants.sound_start)

            # game has begun
            else:
                # opponent's turn, wait until move is received from server
                if status == "wait":
                    my_socket.settimeout(0.001)
                    try:
                        status = my_socket.recv(1024).decode()
                    except socket.error:
                        pass
                    my_socket.settimeout(60000)

                # my turn
                elif turn != my_color:
                    # if opponent resigned, end game
                    if status == "resign":
                        resigned = not my_color
                        turn = not turn
                    # make the opponent's move on the board
                    elif status != "play" and resigned != my_color:
                        if status[-4:] == "MATE":
                            status = status[:-4]
                        board.push(chess.Move.from_uci(status))
                    turn = not turn

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if stop_sound:
                            my_socket.shutdown(1)
                            my_socket.close()
                            return False
                        elif hovering_button != 0:
                            resigned = my_color
                            my_socket.send("resign".encode())

                        if mouse_pos[0] < 830:
                            if selected_piece != -1:
                                move = chess.Move(selected_piece, hovering_square(mouse_pos, my_color))
                                if board.piece_type_at(selected_piece) == chess.PAWN \
                                        and (move.to_square in range(0, 8) or move.to_square in range(56, 64)):
                                    move.promotion = chess.QUEEN

                                if move in board.legal_moves:
                                    play_sound = find_sound(board, move)
                                    board.push(move)
                                    turn = not turn

                                    msg = move.uci()
                                    if board.is_game_over():
                                        msg += "MATE"
                                    my_socket.send(msg.encode())

                                    status = my_socket.recv(1024).decode()
                                selected_piece = -1
                            elif turn == my_color and board.color_at(hovering_square(mouse_pos, my_color)) == my_color \
                                    and selected_piece == -1:
                                selected_piece = hovering_square(mouse_pos, my_color)
                        else:
                            pass

        # bot opponents
        elif game_mode == 3 or game_mode == 4 or game_mode == 5:
            if game_mode == 3:
                opponent_name = "RANDY"
            elif game_mode == 4:
                opponent_name = "MIMI"
            else:
                opponent_name = "OLLY"

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if stop_sound:
                        return False
                    elif hovering_button != 0:
                        resigned = my_color

                    if mouse_pos[0] < 830:
                        if selected_piece != -1:
                            move = chess.Move(selected_piece, hovering_square(mouse_pos, my_color))
                            if board.piece_type_at(selected_piece) == chess.PAWN \
                                    and (move.to_square in range(0, 8) or move.to_square in range(56, 64)):
                                move.promotion = chess.QUEEN

                            if move in board.legal_moves:
                                play_sound = find_sound(board, move)
                                board.push(move)
                                turn = not turn
                            selected_piece = -1
                        elif turn == my_color and board.color_at(hovering_square(mouse_pos, my_color)) == turn\
                                and selected_piece == -1:
                            selected_piece = hovering_square(mouse_pos, my_color)
                    else:
                        pass

            if start_wait:
                win.fill(constants.board_white)
                chess_board.draw_board(board, my_color, pygame.mouse.get_pos(), my_name, opponent_name)
                pygame.display.update()
                time.sleep(1)
                start_wait = not start_wait

            if play_sound != constants.sound_silence:
                pygame.mixer.Sound.play(play_sound)
                play_sound = constants.sound_silence

            if turn != my_color and not board.is_game_over():
                win.fill(constants.board_white)
                chess_board.draw_board(board, my_color, pygame.mouse.get_pos(), my_name, opponent_name)
                pygame.display.update()
                time.sleep(0.2)

                if game_mode == 4:
                    move = evaluation_algorithms.evaluate_immediate_moves(board, turn)
                elif game_mode == 5:
                    move = evaluation_algorithms.evaluate_immediate_moves(board, turn)
                else:
                    move = evaluation_algorithms.generate_random_move(board.legal_moves)
                play_sound = find_sound(board, move)
                board.push(move)
                turn = not turn

        # draw board and shows available moves if a piece is selected
        win.fill(constants.board_white)
        hovering_button = chess_board.draw_board(board, my_color, pygame.mouse.get_pos(), my_name, opponent_name)
        if selected_piece != -1:
            chess_board.show_legal_moves(selected_piece, my_color, board)

        if status == "connected":
            messages.looking_for_players_message(frame)
            frame += 1
            if frame > 210:
                frame = 0

        # game over effects
        if board.is_game_over() or resigned is not None:
            # play the checkmate sound if the game is over
            # stop_sound is used so that the checkmate sound is only played once
            if not stop_sound:
                pygame.mixer.Sound.play(constants.sound_checkmate)
                stop_sound = True

            # find the winner and display the correct winning message
            winner = not resigned
            if resigned is None:
                winner = board.outcome().winner
            messages.game_over_message(winner)

        # if a sound has been assigned to the play_sound variable, play it
        if play_sound != constants.sound_silence and not stop_sound:
            pygame.mixer.Sound.play(play_sound)
            play_sound = constants.sound_silence

        pygame.display.update()
    if game_mode == "2":
        my_socket.shutdown(1)
        my_socket.close()
    pygame.quit()
    return True


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((IP, PORT))
    my_socket.send("db".encode())
    my_socket.recv(1024)

    pygame.mixer.Sound.play(constants.sound_start)

    username = password = ""
    msg = ("", False)
    logged_in = False
    select = 0

    # offset initialized to zero, color initialized to white
    offset = 0
    color = True

    # initialize pygame
    running = True
    pygame.init()
    while running:
        if not logged_in:
            hovering = register_menu.form(username, password, pygame.mouse.get_pos())

            for event in pygame.event.get():
                # the player exits the program
                if event.type == pygame.QUIT:
                    running = False
                    my_socket.shutdown(1)
                    my_socket.close()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    select = hovering
                    if select == 3:
                        my_socket.send((username + "|" + password + "|login").encode())
                        server_msg = my_socket.recv(1024)
                        if int(server_msg):
                            logged_in = True
                            pygame.mixer.Sound.play(constants.sound_start)
                            my_socket.shutdown(1)
                            my_socket.close()
                        else:
                            msg = ("Username or password are incorrect", True)
                    elif select == 4:
                        if register_menu.check_valid(username) and register_menu.check_valid(password):
                            my_socket.send((username + "|" + password + "|signup").encode())
                            server_msg = my_socket.recv(1024)
                            if int(server_msg):
                                msg = ("Successfully signed up", False)
                            else:
                                msg = ("Username already exists", True)
                        else:
                            msg = ("Invalid username or password", True)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if select == 1:
                            username = username[:-1]
                        elif select == 2:
                            password = password[:-1]
                    else:
                        if select == 1:
                            username += event.unicode
                        elif select == 2:
                            password += event.unicode

            register_menu.message(msg)
            pygame.display.update()
        else:
            mouse_pos = pygame.mouse.get_pos()
            win.fill(constants.board_white)

            # the draw_main_menu creates the main menu for the program.
            # in addition, the draw_main_menu function returns certain values if the cursor in hovering over certain...
            # ...buttons in the menu
            hovering = main_menu.draw_main_menu(mouse_pos, offset, color, username)

            pygame.display.update()

            # offsets the background board to create the illusion of it scrolling
            offset += 0.3
            if offset >= 200:
                offset = 0

            for event in pygame.event.get():
                # the player exits the program
                if event.type == pygame.QUIT:
                    running = False
                # the player has clicked on a button (identified by "hovering" not being zero)
                if event.type == pygame.MOUSEBUTTONDOWN and hovering:
                    # hovering 6 is attributed to switching the selected color
                    if hovering == 6:
                        color = not color
                    # hovering 1 through 5 are attributed to their relative game mode (1-5)
                    else:
                        # "game" returns true when closed, which then also closes the main function
                        if game(hovering, color, username):
                            running = False
    pygame.quit()


if __name__ == "__main__":
    main()
