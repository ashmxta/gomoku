"""Gomoku starter code
You should complete every incomplete function,
and add more functions and variables as needed.

Note that incomplete functions have 'pass' as the first statement:
pass is a Python keyword; it is a statement that does nothing.
This is a placeholder that you should remove once you modify the function.
"""

def is_empty(board):
  for y in range(len(board[0])):
    for x in range(len(board[1])):
      if board[y][x] != " ":
        return False
  return True


def is_bounded(board, y_end, x_end, length, d_y, d_x):
  ends_open = 0
  if is_sq_in_board(board, y_end + d_y, x_end + d_x) == True:
    if board[y_end + d_y][x_end + d_x] == " ":
      ends_open += 1
  if is_sq_in_board(board, y_end - d_y * length, x_end - d_x * length) == True:
    if board[y_end - d_y * length][x_end - d_x * length] == " ":
      ends_open += 1

  if ends_open == 2:
    return "OPEN"
  elif ends_open == 1:
    return "SEMIOPEN"
  else:
    return "CLOSED"

# def seq_length(board, col, y_start, x_start, length, d_y, d_x):
#   for limit in range(len(board[0])):
#     x = x_start + d_x * limit
#     y = y_start + d_y * limit
#     if is_sq_in_board(board, y, x) == False:
#       break
#   return limit + 1

def detect_row_all(board, col, y_start, x_start, length, d_y, d_x):
  open_seq_count, semi_open_seq_count, closed_seq_count = 0, 0, 0
  if length >= len(board[0]):
    return open_seq_count, semi_open_seq_count, closed_seq_count
  y = y_start
  x = x_start
  while is_sq_in_board(board, y, x):
  #iterate through each possible "row" start point
    if board[y][x] == col:
      if y + d_y * length <= len(board[0]) and x + d_x * length <= len(board[0]):
        if is_sequence_complete(board, col, y, x, length, d_y, d_x) == True:
          y_end = y + d_y * (length - 1)
          x_end = x + d_x * (length - 1)
          if is_bounded(board, y_end, x_end, length, d_y, d_x) == "OPEN":
            open_seq_count += 1
          elif is_bounded(board, y_end, x_end, length, d_y, d_x) == "SEMIOPEN":
            semi_open_seq_count += 1
          elif is_bounded(board, y_end, x_end, length, d_y, d_x) == "CLOSED":
            closed_seq_count += 1
    y += d_y
    x += d_x

  return open_seq_count, semi_open_seq_count, closed_seq_count

def detect_row(board, col, y_start, x_start, length, d_y, d_x):
  open_seq_count = detect_row_all(board, col, y_start, x_start, length, d_y, d_x)[0]
  semi_open_seq_count = detect_row_all(board, col, y_start, x_start, length, d_y, d_x)[1]
  return open_seq_count, semi_open_seq_count


def detect_rows_all(board, col, length):
  open_seq_count, semi_open_seq_count, closed_seq_count = 0, 0, 0
  for y_start in range(len(board[0])): #horizontal rows
      x_start = 0
      d_y = 0
      d_x = 1
      res = detect_row_all(board, col, y_start, x_start, length, d_y, d_x)
      open_seq_count += res[0]
      semi_open_seq_count += res[1]
      closed_seq_count += res[2]

  for x_start in range(len(board[0])): #vertical rows
      y_start = 0
      d_y = 1
      d_x = 0
      res = detect_row_all(board, col, y_start, x_start, length, d_y, d_x)
      open_seq_count += res[0]
      semi_open_seq_count += res[1]
      closed_seq_count += res[2]

  for x_start in range(len(board[0])): #diagonal rows positive d_x
      y_start = 0
      d_y = 1
      d_x = 1
      res = detect_row_all(board, col, y_start, x_start, length, d_y, d_x)
      open_seq_count += res[0]
      semi_open_seq_count += res[1]
      closed_seq_count += res[2]

  for y_start in range(1, len(board[0])): #diagonal rows positive d_x
      x_start = 0
      d_y = 1
      d_x = 1
      res = detect_row_all(board, col, y_start, x_start, length, d_y, d_x)
      open_seq_count += res[0]
      semi_open_seq_count += res[1]
      closed_seq_count += res[2]


  for x_start in range(len(board[0]) - 1, 0, -1): #diagonal rows neg d_x
      y_start = 0
      d_y = 1
      d_x = -1
      res = detect_row_all(board, col, y_start, x_start, length, d_y, d_x)
      open_seq_count += res[0]
      semi_open_seq_count += res[1]
      closed_seq_count += res[2]

  for y_start in range(len(board[0]) - 1, 0, -1): #diagonal rows neg d_x
      x_start = len(board[0]) - 1
      d_y = 1
      d_x = -1
      res = detect_row_all(board, col, y_start, x_start, length, d_y, d_x)
      open_seq_count += res[0]
      semi_open_seq_count += res[1]
      closed_seq_count += res[2]
  return open_seq_count, semi_open_seq_count, closed_seq_count

def detect_rows(board, col, length):
  open_seq_count = detect_rows_all(board, col, length)[0]
  semi_open_seq_count = detect_rows_all(board, col, length)[1]
  return open_seq_count, semi_open_seq_count


def search_max(board):
  move_y = 0
  move_x = 0
  cur_max = -100000
  for y in range(len(board[0])):
      for x in range(len(board[0])):
          if board[y][x] == " ":
                board[y][x] = "b"
                if score(board) > cur_max:
                    cur_max = score(board)
                    move_y = y
                    move_x = x
                    board[y][x] = " "
                else:
                    board[y][x] = " "
  return move_y, move_x


def score(board):
  MAX_SCORE = 100000

  open_b = {}
  semi_open_b = {}
  open_w = {}
  semi_open_w = {}

  for i in range(2, 6):
    open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
    open_w[i], semi_open_w[i] = detect_rows(board, "w", i)

  if open_b[5] >= 1 or semi_open_b[5] >= 1:
    return MAX_SCORE

  elif open_w[5] >= 1 or semi_open_w[5] >= 1:
    return -MAX_SCORE

  return (-10000 * (open_w[4] + semi_open_w[4]) + 500 * open_b[4] +
          50 * semi_open_b[4] + -100 * open_w[3] + -30 * semi_open_w[3] +
          50 * open_b[3] + 10 * semi_open_b[3] + open_b[2] + semi_open_b[2] -
          open_w[2] - semi_open_w[2])



def is_full(board):
  for y in range(len(board[0])):
      for x in range(len(board[0])):
          if board[y][x] == " ":
            return False
  return True

def is_win(board):
  if detect_rows_all(board, "b", 5)[0] > 0 or detect_rows_all(board, "b", 5)[1] > 0 or detect_rows_all(board, "b", 5)[2] > 0:
    return "Black won"
  if detect_rows_all(board, "w", 5)[0] > 0 or detect_rows_all(board, "w", 5)[1] > 0 or detect_rows_all(board, "w", 5)[2] > 0:
    return "White won"
  elif is_full(board):
    return "Draw"
  else:
    return "Continue Playing"

def print_board(board):

  s = "*"
  for i in range(len(board[0]) - 1):
    s += str(i % 10) + "|"
  s += str((len(board[0]) - 1) % 10)
  s += "*\n"

  for i in range(len(board)):
    s += str(i % 10)
    for j in range(len(board[0]) - 1):
      s += str(board[i][j]) + "|"
    s += str(board[i][len(board[0]) - 1])

    s += "*\n"
  s += (len(board[0]) * 2 + 1) * "*"

  print(s)


def make_empty_board(sz):  #sz is size
  board = []
  for i in range(sz):
    board.append([" "] * sz)
  return board


def analysis(board):
  for c, full_name in [["b", "Black"], ["w", "White"]]:
    print("%s stones" % (full_name))
    for i in range(2, 6):
      open, semi_open = detect_rows(board, c, i)
      print("Open rows of length %d: %d" % (i, open))
      print("Semi-open rows of length %d: %d" % (i, semi_open))


def play_gomoku(board_size):
  board = make_empty_board(board_size)
  board_height = len(board)
  board_width = len(board[0])

  while True:
    print_board(board)
    if is_empty(board):
      move_y = board_height // 2
      move_x = board_width // 2
    else:
      move_y, move_x = search_max(board)

    print("Computer move: (%d, %d)" % (move_y, move_x))
    board[move_y][move_x] = "b"
    print_board(board)
    analysis(board)

    game_res = is_win(board)
    if game_res in ["White won", "Black won", "Draw"]:
      return game_res

    print("Your move:")
    move_y = int(input("y coord: "))
    move_x = int(input("x coord: "))
    board[move_y][move_x] = "w"
    print_board(board)
    analysis(board)

    game_res = is_win(board)
    if game_res in ["White won", "Black won", "Draw"]:
      return game_res


def put_seq_on_board(board, y, x, d_y, d_x, length, col):
  for i in range(length):
    board[y][x] = col
    y += d_y
    x += d_x


def test_is_empty():
  board = make_empty_board(8)
  if is_empty(board):
    print("TEST CASE for is_empty PASSED")
  else:
    print("TEST CASE for is_empty FAILED")


def test_is_bounded():
  board = make_empty_board(8)
  x = 5
  y = 1
  d_x = 0
  d_y = 1
  length = 3
  put_seq_on_board(board, y, x, d_y, d_x, length, "w")
  print_board(board)

  y_end = 3
  x_end = 5

  if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
    print("TEST CASE for is_bounded PASSED")
  else:
    print("TEST CASE for is_bounded FAILED")


def test_detect_row1():  # testing horizontal
  board = make_empty_board(8)
  x = 3
  y = 2
  d_x = 1
  d_y = 0
  length = 5
  put_seq_on_board(board, y, x, d_y, d_x, length, "w")
  print_board(board)
  if detect_row(board, "w", 2, 0, length, d_y, d_x) == (0, 1):
    print(detect_row(board, "w", 2, 0, length, d_y, d_x))
    print("TEST CASE for detect_row PASSED")
  else:
    print(detect_row(board, "w", 2, 0, length, d_y, d_x))
    print("TEST CASE for detect_row FAILED")

def test_detect_row2(): #testing diagonal
  board = make_empty_board(8)
  x = 1
  y = 1
  d_x = 1
  d_y = 1
  length = 5
  put_seq_on_board(board, y, x, d_y, d_x, length, "w")
  print_board(board)
  if detect_row(board, "w", 0, 0, length, d_y, d_x) == (1, 0):
    print(detect_row(board, "w", 0, 0, length, d_y, d_x))
    print("TEST CASE for detect_row PASSED")
  else:
    print(detect_row(board, "w", 0, 0, length, d_y, d_x))
    print("TEST CASE for detect_row FAILED")

def test_detect_row3(): #long diagonal
  board = make_empty_board(8)
  x = 7
  y = 0
  d_x = -1
  d_y = 1
  length = 8
  put_seq_on_board(board, y, x, d_y, d_x, length, "w")
  print_board(board)
  if detect_row(board, "w", 0, 7, length, d_y, d_x) == (0, 0):
    print(detect_row(board, "w", 0, 7, length, d_y, d_x))
    print("TEST CASE for detect_row PASSED")
  else:
    print(detect_row(board, "w", 0, 7, length, d_y, d_x))
    print("TEST CASE for detect_row FAILED")


def test_detect_row4(): #testing 2 seq in row
  board = make_empty_board(8)
  d_x = 0
  d_y = 1
  length = 2
  put_seq_on_board(board, 2, 0, d_y, d_x, length, "w")
  put_seq_on_board(board, 5, 0, d_y, d_x, length, "w")
  print_board(board)
  if detect_row(board, "w", 0, 0, length, d_y, d_x) == (2, 0):
    print(detect_row(board, "w", 0, 0, length, d_y, d_x))
    print("TEST CASE for detect_row PASSED")
  else:
    print(detect_row(board, "w", 0, 0, length, d_y, d_x))
    print("TEST CASE for detect_row FAILED")



def test_detect_row5(): #testing 2 seq in diag row
  board = make_empty_board(8)
  d_x = 1
  d_y = 1
  length = 2
  put_seq_on_board(board, 2, 0, d_y, d_x, length, "w")
  put_seq_on_board(board, 5, 3, d_y, d_x, length, "w")
  print_board(board)
  if detect_row(board, "w", 2, 0, length, d_y, d_x) == (1, 1):
    print(detect_row(board, "w", 2, 0, length, d_y, d_x))
    print("TEST CASE for detect_row PASSED")
  else:
    print(detect_row(board, "w", 2, 0, length, d_y, d_x))

    print("TEST CASE for detect_row FAILED")


def test_detect_row6(): #testing 2 seq in diag row
  board = make_empty_board(8)
  d_x = 1
  d_y = 1
  length = 2
  put_seq_on_board(board, 4, 0, d_y, d_x, length, "w")
  print_board(board)
  if detect_row(board, "w", 4, 0, length, d_y, d_x) == (0, 1):
    print(detect_row(board, "w", 4, 0, length, d_y, d_x))
    print("TEST CASE for detect_row PASSED")
  else:
    print(detect_row(board, "w", 4, 0, length, d_y, d_x))

    print("TEST CASE for detect_row FAILED")


def test_detect_row7(): #testing 2 seq in diag row
  board = make_empty_board(8)
  d_x = 1
  d_y = -1
  length = 2
  put_seq_on_board(board, 4, 0, d_y, d_x, length, "w")
  print_board(board)
  if detect_row(board, "w", 4, 0, length, d_y, d_x) == (0, 1):
    print(detect_row(board, "w", 4, 0, length, d_y, d_x))
    print("TEST CASE for detect_row PASSED")
  else:
    print(detect_row(board, "w", 4, 0, length, d_y, d_x))

    print("TEST CASE for detect_row FAILED")

def test_detect_row8(): #testing closed sequences
  board = make_empty_board(8)
  d_x = 1
  d_y = 1
  length = 2
  put_seq_on_board(board, 4, 0, 1, 1, length, "w")
  put_seq_on_board(board, 6, 2, d_y, d_x, length, "b")
  print_board(board)
  if detect_row_all(board, "w", 4, 0, length, d_y, d_x) == (0, 0, 1):
    print(detect_row_all(board, "w", 4, 0, length, d_y, d_x))
    print("TEST CASE for detect_row PASSED")
  else:
    print(detect_row_all(board, "w", 4, 0, length, d_y, d_x))

    print("TEST CASE for detect_row FAILED")


def test_detect_rows():
  board = make_empty_board(8)
  x = 4
  y = 2
  d_x = 1
  d_y = 0
  length = 4
  col = 'w'
  put_seq_on_board(board, 2, 0, d_y, d_x, 4, "b")
  put_seq_on_board(board, y, x, d_y, d_x, length, "w")
  put_seq_on_board(board, 3, 0, d_y, d_x, 4, "w")
  put_seq_on_board(board, 4, 0, 1, 1, length, "w")
  print_board(board)
  if detect_rows_all(board, 'w', length) == (0, 1, 2):
    print(detect_rows_all(board, 'w', length))
    print("TEST CASE for detect_rows PASSED")
  else:
    print(detect_rows_all(board, col, length))
    print("TEST CASE for detect_rows FAILED")


def test_search_max():
  board = make_empty_board(8)
  x = 5
  y = 0
  d_x = 0
  d_y = 1
  length = 4
  col = 'w'
  put_seq_on_board(board, y, x, d_y, d_x, length, col)
  x = 6
  y = 0
  d_x = 0
  d_y = 1
  length = 4
  col = 'b'
  put_seq_on_board(board, y, x, d_y, d_x, length, col)
  print_board(board)
  if search_max(board) == (4, 6):
    print("TEST CASE for search_max PASSED")
  else:
    print("TEST CASE for search_max FAILED")


def easy_testset_for_main_functions():
  test_is_empty()
  test_is_bounded()
  test_detect_rows()
  test_search_max()


def some_tests():
  board = make_empty_board(8)

  board[0][5] = "w"
  board[0][6] = "b"
  y = 5
  x = 2
  d_x = 0
  d_y = 1
  length = 3
  put_seq_on_board(board, y, x, d_y, d_x, length, "w")
  print_board(board)
  analysis(board)

  # Expected output:
  #       *0|1|2|3|4|5|6|7*
  #       0 | | | | |w|b| *
  #       1 | | | | | | | *
  #       2 | | | | | | | *
  #       3 | | | | | | | *
  #       4 | | | | | | | *
  #       5 | |w| | | | | *
  #       6 | |w| | | | | *
  #       7 | |w| | | | | *
  #       *****************
  #       Black stones:
  #       Open rows of length 2: 0
  #       Semi-open rows of length 2: 0
  #       Open rows of length 3: 0
  #       Semi-open rows of length 3: 0
  #       Open rows of length 4: 0
  #       Semi-open rows of length 4: 0
  #       Open rows of length 5: 0
  #       Semi-open rows of length 5: 0
  #       White stones:
  #       Open rows of length 2: 0
  #       Semi-open rows of length 2: 0
  #       Open rows of length 3: 0
  #       Semi-open rows of length 3: 1
  #       Open rows of length 4: 0
  #       Semi-open rows of length 4: 0
  #       Open rows of length 5: 0
  #       Semi-open rows of length 5: 0

  y = 3
  x = 5
  d_x = -1
  d_y = 1
  length = 2

  put_seq_on_board(board, y, x, d_y, d_x, length, "b")
  print_board(board)
  analysis(board)
  print(detect_row(board, "b", 1, 7, 2, 1, -1))

  # Expected output:
  #        *0|1|2|3|4|5|6|7*
  #        0 | | | | |w|b| *
  #        1 | | | | | | | *
  #        2 | | | | | | | *
  #        3 | | | | |b| | *
  #        4 | | | |b| | | *
  #        5 | |w| | | | | *
  #        6 | |w| | | | | *
  #        7 | |w| | | | | *
  #        *****************
  #
  #         Black stones:
  #         Open rows of length 2: 1
  #         Semi-open rows of length 2: 0
  #         Open rows of length 3: 0
  #         Semi-open rows of length 3: 0
  #         Open rows of length 4: 0
  #         Semi-open rows of length 4: 0
  #         Open rows of length 5: 0
  #         Semi-open rows of length 5: 0
  #         White stones:
  #         Open rows of length 2: 0
  #         Semi-open rows of length 2: 0
  #         Open rows of length 3: 0
  #         Semi-open rows of length 3: 1
  #         Open rows of length 4: 0
  #         Semi-open rows of length 4: 0
  #         Open rows of length 5: 0
  #         Semi-open rows of length 5: 0
  #

  y = 5
  x = 3
  d_x = -1
  d_y = 1
  length = 1
  put_seq_on_board(board, y, x, d_y, d_x, length, "b")
  print_board(board)
  analysis(board)

  #        Expected output:
  #           *0|1|2|3|4|5|6|7*
  #           0 | | | | |w|b| *
  #           1 | | | | | | | *
  #           2 | | | | | | | *
  #           3 | | | | |b| | *
  #           4 | | | |b| | | *
  #           5 | |w|b| | | | *
  #           6 | |w| | | | | *
  #           7 | |w| | | | | *
  #           *****************
  #
  #
  #        Black stones:
  #        Open rows of length 2: 0
  #        Semi-open rows of length 2: 0
  #        Open rows of length 3: 0
  #        Semi-open rows of length 3: 1
  #        Open rows of length 4: 0
  #        Semi-open rows of length 4: 0
  #        Open rows of length 5: 0
  #        Semi-open rows of length 5: 0
  #        White stones:
  #        Open rows of length 2: 0
  #        Semi-open rows of length 2: 0
  #        Open rows of length 3: 0
  #        Semi-open rows of length 3: 1
  #        Open rows of length 4: 0
  #        Semi-open rows of length 4: 0
  #        Open rows of length 5: 0
  #        Semi-open rows of length 5: 0


def is_sq_in_board(board, y, x):
  if y >= 0 and y < len(board[0]) and x >= 0 and x < len(board[0]):
    return True
  return False


def is_sequence_complete(board, col, y_start, x_start, length, d_y, d_x):
  for i in range(length):
    if is_sq_in_board(board, y_start + d_y * i, x_start + d_x * i) == False:
      return False
    elif board[y_start + d_y * i][x_start + d_x * i] != col:
      return False
  if is_sq_in_board(board, y_start - d_y, x_start - d_x) == True:
    if board[y_start - d_y][x_start - d_x] == col:
      return False
  if is_sq_in_board(board, y_start + d_y * length, x_start + d_x * length) == True:
    if board[y_start + d_y * length][x_start + d_x * length] == col:
      return False
  return True


if __name__ == '__main__':
  print(play_gomoku(8))
