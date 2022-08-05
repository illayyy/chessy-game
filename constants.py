import pygame
pygame.mixer.init()

square_size = 100

board_white = (240, 218, 181)
board_black = (181, 135, 99)
gray = (110, 110, 110)
dark_gray = (49, 46, 43)
darker_gray = (39, 37, 34)
yellow = (218, 195, 50)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

sound_start = pygame.mixer.Sound(r"sounds\sound_start.wav")
sound_move = pygame.mixer.Sound(r"sounds\sound_move.wav")
sound_castle = pygame.mixer.Sound(r"sounds\sound_castle.wav")
sound_capture = pygame.mixer.Sound(r"sounds\sound_capture.wav")
sound_check = pygame.mixer.Sound(r"sounds\sound_check.wav")
sound_checkmate = pygame.mixer.Sound(r"sounds\sound_checkmate.wav")
sound_silence = pygame.mixer.Sound(r"sounds\sound_silence.wav")

pawn_white = pygame.image.load(r"piece_icons\pawn_white.png")
pawn_black = pygame.image.load(r"piece_icons\pawn_black.png")
knight_white = pygame.image.load(r"piece_icons\knight_white.png")
knight_black = pygame.image.load(r"piece_icons\knight_black.png")
bishop_white = pygame.image.load(r"piece_icons\bishop_white.png")
bishop_black = pygame.image.load(r"piece_icons\bishop_black.png")
rook_white = pygame.image.load(r"piece_icons\rook_white.png")
rook_black = pygame.image.load(r"piece_icons\rook_black.png")
queen_white = pygame.image.load(r"piece_icons\queen_white.png")
queen_black = pygame.image.load(r"piece_icons\queen_black.png")
king_white = pygame.image.load(r"piece_icons\king_white.png")
king_black = pygame.image.load(r"piece_icons\king_black.png")
piece_dict = {"P": pawn_white, "N": knight_white, "B": bishop_white, "R": rook_white, "Q": queen_white, "K": king_white,
              "p": pawn_black, "n": knight_black, "b": bishop_black, "r": rook_black, "q": queen_black, "k": king_black}
