import pygame
import sys

# return column and row on board based off x and y
def map_mouse_to_board(x, y):
    x -= margin
    y -= margin
    if x < 0:
        x = 0
    if y < 0:
        y = 0
    return min(8,x*9//gameSize), min(8, y*9//gameSize)

# maps x's and o's
def draw_board(board9x9, board3x3):
    myFont = pygame.font.SysFont('Tahoma', gameSize // 9)
    for y in range(9):
        for x in range(9):
            mark = board9x9[y][x]
            if mark == xMark:
                color = xColor
            else:
                color = oColor
            text_surface = myFont.render(mark, False, color)
            screen.blit(
                text_surface,
                (y*(gameSize//9) + margin + (gameSize//36),
                x*(gameSize//9) + margin - (gameSize//40))
            )
    myFont = pygame.font.SysFont('Tahoma', gameSize // 3)
    for y in range(3):
        for x in range(3):
            mark = board3x3[y][x]
            if mark == None:
                continue
            if xMark in mark:
                text_surface = myFont.render(xMark, False, xColor)
                screen.blit(
                    text_surface,
                    (y*(gameSize//3) + margin + (gameSize//12),
                    x*(gameSize//3) + margin - (gameSize//13))
                )
            if oMark in mark:
                text_surface = myFont.render(oMark, False, oColor)
                screen.blit(
                    text_surface,
                    (y*(gameSize//3) + margin + (gameSize//12),
                    x*(gameSize//3) + margin - (gameSize//13))
                )

# if there are any None's  
def is_full(board):
    for i in board:
        for j in i:
            if j != None:
                return False
    return True

# if the box is full
def is_full_box(board9x9, column, row):
    y = column%3
    x = row%3
    for i in range(3):
        for j in range(3):
            if board9x9[3*y+i][3*x+j] == None:
                return False
    return True

# TODO
# to check who won the 3x3 box
def get_winner_3x3(board, board3x3, column, row):
    if board3x3[column//3][row//3] != None:
        return None

    column = (column//3)*3
    row = (row//3)*3

    winners = ""
    # Diagonals
    if ((board[column+0][row+0] == board[column+1][row+1] and board[column+1][row+1] == board[column+2][row+2]) \
            or (board[column+0][row+2] == board[column+1][row+1] and board[column+1][row+1] == board[column+2][row+0])) and board[column+1][row+1] is not None:
        if board[column+1][row+1] not in winners:
            winners += board[column+1][row+1]
    for i in range(3):
        if board[column+i][row+0] == board[column+i][row+1] and board[column+i][row+1] == board[column+i][row+2] and board[column+i][row+0] is not None:  # Columns
            if board[column+i][row+0] not in winners:
                winners += board[column+i][row+0]
        if board[column+0][row+i] == board[column+1][row+i] and board[column+1][row+i] == board[column+2][row+i] and board[column+0][row+i] is not None:  # Rows
            if board[column+0][row+i] not in winners:
                winners += board[column+0][row+i]
    if winners == "":
        return None
    return winners

# to check who won the entire game
def get_winner_game(board):
    print(board)
    for mark in ['x', 'o']:
        if all(board[i][i] is not None and mark in board[i][i] for i in range(3)) or \
            all(board[i][2-i] is not None and mark in board[i][2-i] for i in range(3)) or \
            any(all([board[i][j] is not None and mark in board[i][j] for j in range(3)]) for i in range(3)) or \
            any(all([board[j][i] is not None and mark in board[j][i] for j in range(3)]) for i in range(3)):
            return mark
    return None

# draws frame
def draw_lines():
    for i in range(1, 9):
        if i % 3 == 0:
            continue
        else:
            # Vertical lines
            pygame.draw.line(
                screen, 
                lineColor, 
                (margin + (gameSize // 9) * i, margin),
                (margin + (gameSize // 9) * i, screenSize - margin), 
                lineSize)
            # Horizontal lines
            pygame.draw.line(
                screen, 
                lineColor, 
                (margin, margin + (gameSize // 9) * i), 
                (screenSize - margin, margin + (gameSize // 9) * i),
                lineSize)

    for i in range(1, 3):
        # Vertical lines
            pygame.draw.line(
                screen, 
                lineColor2, 
                (margin + (gameSize // 3) * i, margin),
                (margin + (gameSize // 3) * i, screenSize - margin), 
                lineSize2)
            # Horizontal lines
            pygame.draw.line(
                screen, 
                lineColor2, 
                (margin, margin + (gameSize // 3) * i), 
                (screenSize - margin, margin + (gameSize // 3) * i),
                lineSize2)

def is_move_legal(board9x9, column, row, nextBox):
    if board9x9[column][row] == None:
        # check if its in the box specified by the move before
        if nextBox == (None, None) or nextBox == (column//3, row//3):
            if not is_full_box(board9x9, column, row):
                return True
            print("Box is full")
    return False



screenSize = 1000
margin = 50
gameSize = screenSize - (2 * margin)
lineSize = 10
lineSize2 = 15
backgroundColor = (235, 235, 235)
lineColor = (74, 74, 74)
lineColor2 = (28, 28, 28)
xColor = (200, 0, 0)
oColor = (0, 0, 200)
xMark = 'x'
oMark = 'o'
board3x3 = [[None] * 3 for i in range(3)]
board9x9 = [[None] * 9 for i in range(9)]
currentMove = 'x'
pygame.init()
screen = pygame.display.set_mode((screenSize, screenSize))
pygame.display.set_caption("Tic Tac Froe by Maxim")
pygame.font.init()
screen.fill(backgroundColor)
canPlay = True
draw_lines()
nextBox = (None, None)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                board3x3 = [[None] * 3 for i in range(3)]
                board9x9 = [[None] * 9 for i in range(9)]
                screen.fill(backgroundColor)
                draw_lines()
                canPlay = True
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type is pygame.MOUSEBUTTONDOWN and canPlay:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            (column, row) = map_mouse_to_board(mouseX, mouseY)
            if is_move_legal(board9x9, column, row, nextBox):
                nextBox = (column%3, row%3)
                board9x9[column][row] = currentMove
                if currentMove == xMark:
                    currentMove = oMark
                else:
                    currentMove = xMark
                smallWinner = get_winner_3x3(board9x9, board3x3, column, row)
                board3x3[column//3][row//3] = smallWinner
                draw_board(board9x9, board3x3)
                if smallWinner is not None:
                    print(smallWinner, column//3, row//3)
                    winner = get_winner_game(board3x3)
                    if winner is not None:
                        myFont = pygame.font.SysFont('Tahoma', screenSize // 5)
                        text_surface = myFont.render(str(winner) + " has won!", False, lineColor)
                        screen.blit(text_surface, (margin, screenSize // 2 - screenSize // 10))
                        canPlay = False

                # check if there is a legal move next
                if is_full(board9x9):
                    myFont = pygame.font.SysFont('Tahoma', screenSize // 5)
                    text_surface = myFont.render("Draw!", False, lineColor)
                    screen.blit(text_surface, (screenSize // 10, screenSize // 2 - screenSize // 10))
    pygame.display.update()