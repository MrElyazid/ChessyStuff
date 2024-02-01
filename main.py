
chessboard = [[None for _ in range(8)] for _ in range(8)]

for row in range(8):
    for col in range(8):
        chessboard[row][col] = chr(97 + col) + str(8 - row)


def square_name_to_coordinates(square_name):

    col_letter = square_name[0]
    row_number = 5

    col = ord(col_letter) - ord('a')
    row = row_number - 1

    return row, col


def in_board(i,j):
    return (i >= 0 and i <= 7 and j >= 0 and j <= 7)


def possible_squares_for_knight(square):
    squares = []
    i, j = square_name_to_coordinates(square)

    knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
    for move in knight_moves:
        new_i, new_j = i + move[0], j + move[1]
        if in_board(new_i, new_j):
            squares.append(chessboard[new_i][new_j])
    return squares



starting_square = "b5"
# end_square = input("enter the desired arrival square for the knight : ")



graph = [[0 for _ in range(8)] for _ in range(8)]

seen_squares = set(starting_square)

current_square_in_loop = 0

counter = 1
for i in range(64):
    next_possible_squares = possible_squares_for_knight(list(seen_squares)[current_square_in_loop])

    for square in next_possible_squares:
        i,j = square_name_to_coordinates(square)
        graph[i][j] = counter

    seen_squares.update(next_possible_squares)
    current_square_in_loop += 1
    print(current_square_in_loop)
    counter += 1

for row in graph:
    print(row)