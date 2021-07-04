"""
2048 Game
"""
from copy import deepcopy
import random

def createNull(a, b):
    return [[0 for i in range(b)] for j in range(a)]

def transpose(mat):
    ans = createNull(len(mat[0]), len(mat))
    for y in range(len(mat[0])):
        for x in range(len(mat)):
            ans[y][x] = mat[x][y]
    return ans

def maxMatVal(mat):
    maxi = -1000000000
    for row in mat:
        maxi = max(maxi, max(*row))
    return maxi

def printBoard(board):
    # The highest possible tile is 131072 in the game, hence each tile has a length of 6 digits
    rows, columns = 4, 4
    dashes_for_1_tile = 7
    for i in range(columns):
        print('-' * dashes_for_1_tile * rows + '-')
        for j in range(rows):
            print('|{:^6}'.format('' if board[i][j] == 0 else board[i][j]), end='')
        print('|')
    print('-' * dashes_for_1_tile * rows + '-')

def get_spawned_numbers(row):
    numbers = []
    for i in row:
        if i != 0:
            numbers.append(i)
    return numbers

def moveRowRight(row):
    numbers = get_spawned_numbers(row)
    idx = len(numbers) - 1
    while idx > 0:
        if numbers[idx] == numbers[idx-1]:
            numbers[idx] *= 2
            numbers[idx-1] = 0
            idx -= 2
        else:
            idx -= 1
    numbers = get_spawned_numbers(numbers)
    numbers = [0] * (4 - len(numbers)) + numbers
    return numbers

def moveRowLeft(row):
    row = row[::-1]
    row = moveRowRight(row)
    row = row[::-1]
    return row
    
def move(orgState, direction: str):
    state = deepcopy(orgState)
    if direction == 'l' or direction == 'r':
        for rowIdx in range(len(state)):
            if direction == 'l':
                state[rowIdx] = moveRowLeft(state[rowIdx])
            else:
                state[rowIdx] = moveRowRight(state[rowIdx])
    elif direction == 'u' or direction == 'd':
        state = transpose(state)
        for rowIdx in range(len(state)):
            if direction == 'u':
                state[rowIdx] = moveRowLeft(state[rowIdx])
            else:
                state[rowIdx] = moveRowRight(state[rowIdx])
        state = transpose(state)
    return state

def isBoardFull(board):
    for row in board:
        if 0 in row:
            return False
    return True

def place_random_tile(board, chances_2=80, chances_4=20):
    tile_to_place = random.choice((2,)*chances_2 + (4,)*chances_4)
    if not isBoardFull(board):
        while True:
            rowIdx, colIdx = random.randint(0, 3), random.randint(0, 3)
            if board[rowIdx][colIdx] == 0:
                board[rowIdx][colIdx] = tile_to_place
                break

def isGameOver(board):
    if not isBoardFull(board):
        return False
    # If all possible moves yield the same board, the board is stuck, hence game over.
    return move(board, 'l') == move(board, 'r') == move(board, 'u') == move(board, 'd')

def printInstructions():
    print("Welcome to 2048!")
    print("Rules:")
    print("Use [U]p, [D]own, [L]eft, [R]ight to move the tiles.")
    print("When two tiles with the same number touch, they merge into 1!")
    print("Your goal is to get the highest number possible without getting stuck. Good luck!")

def main():
    printInstructions()
    input("Press enter to start: ")
    board = createNull(4, 4)
    place_random_tile(board)
    place_random_tile(board)
    #board = [[2,0,0,2],[4,16,8,2],[2,64,32,4],[1024,1024,64,0]] # Uncomment to test
    playing = True
    while playing:
        print("Game had started.")
        print("The board now:")
        printBoard(board)
        while not isGameOver(board):
            valid = False
            while not valid:
                direction = input("Please enter your move ([U]p, [D]own, [L]eft, [R]ight, [Q]uit): ").strip().lower()
                if len(direction) < 1 or direction[0] not in "udlrq":
                    print("Invalid input, please try again.")
                else:
                    direction = direction[0]
                    if direction == 'q':
                        print("Thanks for playing! Your maximum tile is %d! Goodbye!" % maxMatVal(board))
                        return
                    valid = True
            board = move(board, direction)
            place_random_tile(board)
            print("The board now:")
            printBoard(board)
        print("Game over! Your maximum tile is %d! Good Job!" % maxMatVal(board))
        if input('Would you want to play again? (y/n) ').strip().lower().startswith('n'):
            playing = False
    print("Thanks for playing! Goodbye!")

def test():
    """Test function"""
    test_board = [[2,0,0,2],[4,16,8,2],[2,64,32,4],[1024,1024,64,0]]
    printBoard(test_board)
    printBoard(move(test_board, 'l'))
    printBoard(move(test_board, 'r'))
    printBoard(move(test_board, 'u'))
    printBoard(move(test_board, 'd'))
    
if __name__ == '__main__':
    main()
    #test() #Uncomment to test
    
    
