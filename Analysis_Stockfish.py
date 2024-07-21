import chess.pgn
import chess.engine
import csv
import numpy as np

engine = chess.engine.SimpleEngine.popen_uci("D:/programs/stockfish/stockfish-windows-x86-64-avx2.exe")
pgn_file = open("D:/mygames.pgn")


csv_file = open('analysis.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Game Number', 'Move Number', 'Move', 'Score', 'Depth', 'Best Move'])


game_number = 1

def lichess_white_expected_score(cp,p=-0.00368208):
    return 1.0/(1.0+np.exp(p*cp))


while True:
    game = chess.pgn.read_game(pgn_file)

    if game is None:
        break


    board = game.board()
    move_number = 1
    total_blunders = 0
    total_mistakes = 0
    total_inaccuracies = 0

    for move in game.mainline_moves():

        analysis = engine.analyse(board, chess.engine.Limit(time = 0.2))
        score = analysis['score']
        depth = analysis['depth']
        best_move = analysis['pv'][0] if 'pv' in analysis else None

        board.push(move)

    if score.is_mate():
        # If the score is a mate score, we use a large centipawn value
        score = 100000 if score.mate() > 0 else -100000
    else:
        score = score.white().score()



        # move quality

        if score is not None and isinstance(score, int):
            if score <= -300:
                total_blunders += 1
            elif score <= -100:
                total_mistakes += 1
            elif score <= -50:
                total_mistakes += 1

        csv_writer.writerow([

            game_number,
            move_number,
            str(move),
            lichess_white_expected_score(score),
            depth,
            str(best_move)
        ])
        
        move_number += 1



    csv_writer.writerow([])
    csv_writer.writerow(['Summary for Game', game_number])
    csv_writer.writerow(['Total Moves', move_number - 1])
    csv_writer.writerow(['Final Score', analysis['score'].relative.score() if 'score' in analysis else 'N/A'])
    csv_writer.writerow(['Total Inaccuracies', total_inaccuracies])
    csv_writer.writerow(['Total mistakes', total_mistakes])
    csv_writer.writerow(['Total blunders', total_blunders])
    csv_writer.writerow([])

    game_number += 1

engine.quit()
csv_file.close()
pgn_file.close()

