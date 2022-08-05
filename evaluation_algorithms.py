import time
import sys
import random
import pygame
import chess


def render_all_moves(depth, n_board):
    # exit condition, depth has reached 0
    if not depth:
        return 1

    # count the number of available moves per this iteration
    move_sum = 0
    for move in n_board.legal_moves:
        # make move
        n_board.push(move)
        # recursively check all available moves branching from this move
        move_sum += render_all_moves(depth - 1, n_board)
        # unmake move
        n_board.pop()

    return move_sum


def moves_per_iteration(depth):
    pygame.quit()
    n_board = chess.Board()
    for i in range(0, depth):
        start_time = time.time()
        num_moves = str(render_all_moves(i, n_board))
        elapsed_time = str(round(time.time() - start_time, 3))
        print(("Depth: " + str(i) + " ply\tResult: " + num_moves + " positions\tTime elapsed: " + elapsed_time)
              .expandtabs(15))


def evaluate_board(n_board, turn):
    evaluation = 0
    # values of each piece, king is worth infinitely many points
    value_dict = {"P": 1, "N": 3, "B": 3, "R": 5, "Q": 9, "K": sys.maxsize,
                  "p": -1, "n": -3, "b": -3, "r": -5, "q": -9, "k": -sys.maxsize}

    # for each square on the board, if there is a piece on it, add its value to the total evaluation
    for square in chess.SQUARES:
        if n_board.piece_at(square):
            evaluation += value_dict[n_board.piece_at(square).symbol()]

    # black's evaluation is the exact opposite of white's evaluation
    if turn:
        return evaluation
    return -evaluation


def evaluate_immediate_moves(n_board, turn):
    # lowest possible evaluation, base minimum value
    best_moves_eva = [(-sys.maxsize, generate_random_move(n_board.legal_moves))]

    for move in n_board.legal_moves:
        # make move
        n_board.push(move)

        # if the move that has been played is equal in evaluation to the other best moves, append it to the best...
        # ...moves list
        if evaluate_board(n_board, turn) == best_moves_eva[0][0]:
            best_moves_eva.append((evaluate_board(n_board, turn), move))

        # if the move that has been played is greater in evaluation to the other best moves, remove all best moves...
        # ...from the list and create a new one with just the recently played move
        elif evaluate_board(n_board, turn) > best_moves_eva[0][0]:
            best_moves_eva = [(evaluate_board(n_board, turn), move)]

        # unmake move
        n_board.pop()

    # pick a move at random from the found equally best moves
    best_moves = []
    for move in best_moves_eva:
        best_moves.append(move[1])
    return generate_random_move(best_moves)


def generate_random_move(moves):
    if type(moves) == list:
        move_num = random.randint(0, len(moves) - 1)
    else:
        move_num = random.randint(0, moves.count() - 1)
    count = 0
    for move in moves:
        if count == move_num:
            return move
        count += 1
