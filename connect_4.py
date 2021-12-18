import numpy as np
import pygame
import tkinter as tk
from tkinter import messagebox

ROW_COUNT = 6
COLUMN_COUNT = 7

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT -1][col] == 0


def get_next_open_row(board, col):
    for row in range(ROW_COUNT):
        if board[row][col] == 0:
            return row


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # check horizontal locations for win
    for col in range(COLUMN_COUNT -3):
        for row in range(ROW_COUNT):
            if board[row][col] == piece and board[row][col +1] == piece and board[row][col +2] == piece and board[row][col +3] == piece:
                return True

    # check vertical locations for win
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT -3):
            if board[row][col] == piece and board[row +1][col] == piece and board[row +2][col] == piece and board[row +3][col] == piece:
                return True

    # check for positively sloped diagonals
    for col in range(COLUMN_COUNT -3):
        for row in range(ROW_COUNT -3):
            if board[row][col] == piece and board[row +1][col +1] == piece and board[row +2][col +2] == piece and board[row +3][col +3] == piece:
                return True

    # check for negatively sloped diagonals
    for col in range(COLUMN_COUNT -3):
        for row in range(3, ROW_COUNT):
            if board[row][col] == piece and board[row -1][col +1] == piece and board[row -2][col +2] == piece and board[row -3][col +3] == piece:
                return True


def draw_board(screen, board):
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (col * SQUARE_SIZE, row * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, ((col * SQUARE_SIZE + SQUARE_SIZE // 2),(row * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE // 2)), RADIUS)


    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT):
            # player 1
            if board[row][col] == 1:
                pygame.draw.circle(screen, RED, ((col * SQUARE_SIZE + SQUARE_SIZE // 2), height - (row * SQUARE_SIZE + SQUARE_SIZE // 2)), RADIUS)

            # player 2
            elif board[row][col] == 2:
                pygame.draw.circle(screen, YELLOW, ((col * SQUARE_SIZE + SQUARE_SIZE // 2), height - (row * SQUARE_SIZE + SQUARE_SIZE // 2)), RADIUS)

    pygame.display.update()


# def message_box(subject, content):
#     root = tk.Tk()
#     root.attributes("-topmost", True)
#     root.withdraw()
#     messagebox.showinfo(subject, content)
#
#     try:
#         root.destroy()
#     except:
#         pass

board = create_board()
print_board(board)

game_over = False
turn = 0

pygame.init()

SQUARE_SIZE = 100

width = COLUMN_COUNT * SQUARE_SIZE
height = (ROW_COUNT + 1) * SQUARE_SIZE

size = (width, height)

RADIUS = int(SQUARE_SIZE / 2 - 5)

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Connect 4')
draw_board(screen, board)
pygame.display.update()

myfont = pygame.font.SysFont("comicsansms", 75)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            pos_x = event.pos[0]

            if turn == 0:
                pygame.draw.circle(screen, RED, (pos_x, SQUARE_SIZE // 2), RADIUS)

            elif turn == 1:
                pygame.draw.circle(screen, YELLOW, (pos_x, SQUARE_SIZE // 2), RADIUS)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # ask for player 1 input
            if turn == 0:
                pos_x = event.pos[0]
                col = pos_x // SQUARE_SIZE

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        # winner = "player 1"

                        pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
                        label = myfont.render("Player 1 wins!!", True, RED)
                        screen.blit(label, (115, 10))

                        print("Player 1 wins!!")
                        game_over = True

            # ask for player 2 input
            else:
                pos_x = event.pos[0]
                col = pos_x // SQUARE_SIZE

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if winning_move(board, 2):
                        # winner = "player 2"

                        pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
                        label = myfont.render("Player 2 wins!!", True, YELLOW)
                        screen.blit(label, (115, 10))

                        print("Player 2 wins!!")
                        game_over = True

            print_board(board)
            draw_board(screen, board)

            turn += 1
            turn = turn % 2

            if game_over:
                pygame.time.wait(3000)
                # message_box('Winner', winner + " Congratulations..!!")