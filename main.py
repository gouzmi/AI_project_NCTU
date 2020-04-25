from board import Board


# ask for board size
board_size = input ("Board Size ? (4 or 6): ")
my_board = Board(int(board_size))
my_board.start()