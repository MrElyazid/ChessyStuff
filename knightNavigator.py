

# initializing a chess board, the ascii code for a is 97, the square a8 coordinates are (0,0) and not (1,8) !

chessboard = [[None for _ in range(8)] for _ in range(8)]
for row in range(8):
    for col in range(8):
        chessboard[row][col] = chr(97 + col) + str(8 - row)

# testing
def square_name_to_coordinates(square_name):
    col_letter = square_name[0]
    row_number = int(square_name[1])  

    col = ord(col_letter) - ord('a')
    row = 8 - row_number  # see the comment at the start of the code :) 

    return row, col

def in_board(i,j):
    return (i >= 0 and i <= 7 and j >= 0 and j <= 7)



# classical breadth first search algorithm, see https://en.wikipedia.org/wiki/Breadth-first_search ,
# we explore the graph of possible kinght movements from the start square, layers in the graph are the possible knight
# movements at each time, each square holds the minimum number of moves necessary to reach it from the beginning square

def bfs(start):
    
    graph = [[float('inf') for _ in range(8)] for _ in range(8)]
    i_start, j_start = square_name_to_coordinates(start)
    graph[i_start][j_start] = 0  
    queue = [(i_start, j_start)]  
    
    while queue:
        i, j = queue.pop(0)
        current_moves = graph[i][j]
        
        for move in possible_squares_for_knight(chessboard[i][j]):
            next_i, next_j = square_name_to_coordinates(move)
            
            if graph[next_i][next_j] > current_moves + 1:
                graph[next_i][next_j] = current_moves + 1 # + 1 because we update the square with the number of moves done AT THE MOMENT
                queue.append((next_i, next_j))
    
    return graph


def possible_squares_for_knight(square):
    squares = []
    i, j = square_name_to_coordinates(square)
    
    knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
    for dx, dy in knight_moves:
        new_i, new_j = i + dx, j + dy
        if in_board(new_i, new_j):
            squares.append(chessboard[new_i][new_j])
    return squares


starting_square = input("enter the starting square for the knight : ")
end_square = input("enter the desired end square : ")

print(f'the following is the minimum number of moves needed to reach each square from {starting_square} on the chess board : \n')
graph = bfs(starting_square)

for row in graph:
    print(row)


# a recursive function to construct the path from two squares ( start and end ) based on the graph, idea is : 
# go to end square, see if start square is reachable within 1 move, if not then go to the nearest square ( in knight movement )
# which is reachable from the start in minimum number of moves possible. see implementation :


def construct_path(square):

    possible_moves = possible_squares_for_knight(square)



    if starting_square in possible_moves:
        return [square, starting_square]
    else:
        arr = [graph[i][j] for i,j in [square_name_to_coordinates(sqr) for sqr in possible_moves]]
        return [square] + construct_path(possible_moves[arr.index(min(arr))])


path = construct_path(end_square)
path.reverse()       
print("the path from start to end is : ")
print(path)
