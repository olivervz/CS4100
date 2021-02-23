import copy
# state = [
#           [" ", " ", " "],
#           [" ", " ", " "],
#           [" ", " ", " "]
#         ]
def utility(state):
  """Determines whether the game has terminated

  Args:
      state list(list()): Board State
  """
  pieces = {"X" : 1, "O": -1}
  for piece in pieces:
    # Top row
    if state[0][0] == piece and state[0][1] == piece and state[0][2] == piece:
      return pieces[piece] 
    # Mid row
    if state[1][0] == piece and state[1][1] == piece and state[1][2] == piece:
      return pieces[piece]
    # Bot row
    if state[2][0] == piece and state[2][1] == piece and state[2][2] == piece:
      return pieces[piece]

    # Left col
    if state[0][0] == piece and state[1][0] == piece and state[2][0] == piece:
      return pieces[piece] 

    # Mid col
    if state[0][1] == piece and state[1][1] == piece and state[2][1] == piece:
      return pieces[piece] 

    # Right col
    if state[0][2] == piece and state[1][2] == piece and state[2][2] == piece:
      return pieces[piece] 

    # Top Left Diag 
    if state[0][0] == piece and state[1][1] == piece and state[2][2] == piece:
      return pieces[piece] 

    # Right col
    if state[0][2] == piece and state[1][1] == piece and state[2][0] == piece:
      return pieces[piece] 
  for x in state:
    if " " in x:
      return None
  return 0

def minimax(state, player):
  """Minimax search function

  Args:
      state (list(list())): Board State
      player (String): index, "X" = X, "O" = O
  """
  # Terminal state
  if utility(state) in [0, -1, 1]:
    return utility(state)

  # X's turn
  if player == "X":
    max_value = float("-inf")
    for successor in generateSuccessors(state, player):
      max_value = max(max_value, minimax(successor, "O"))
    return max_value

  # O's turn
  if player == "O":
    min_value = float("inf")
    for successor in generateSuccessors(state, player):
      min_value = min(min_value, minimax(successor, "X"))
    return min_value

def generateSuccessors(state, player):
  """Return a list of all board states that are successors

  Args:
      state (list(list())): board state
      player (String): index, "X" = X, "O" = O
  """
  successors = []
  for i in range(len(state)):
    for j in range(len(state[i])):
      if state[i][j] == " ":
        tempState = copy.deepcopy(state)
        tempState[i][j] = player
        successors.append(tempState)
  return successors


if __name__ == '__main__':
  s0 = [
    [" ", " ", " "],
    [" ", " ", " "],
    [" ", " ", " "],
  ]
  s1 = [
    [" ", " ", " "],
    [" ", " ", " "],
    [" ", " ", "X"],
  ]
  s2 = [
    ["O", " ", " "],
    [" ", " ", " "],
    [" ", " ", "X"],
  ]
  # (1, 1), 
  s2optimal = [
    [" ", " ", " "],
    [" ", "O", " "],
    [" ", " ", "X"],
  ]
  s3 = [
    ["O", " ", " "],
    ["X", " ", " "],
    [" ", " ", "X"],
  ]
  # (0, 2), (2, 0)
  s3optimal = [
    ["O", " ", "X"],
    [" ", " ", " "],
    [" ", " ", "X"],
  ]
  s4 = [
    ["O", "O", " "],
    ["X", " ", " "],
    [" ", " ", "X"],
  ]
  # (0, 2), (1, 2), (1, 1) 
  s4optimal = [
    ["O", " ", " "],
    ["X", "O", " "],
    [" ", " ", "X"],
  ]
  s5 = [
    ["O", "O", "X"],
    ["X", " ", " "],
    [" ", " ", "X"],
  ]
  s6 = [
    ["O", "O", "X"],
    ["X", " ", "O"],
    [" ", " ", "X"],
  ]

  print("X Moves: Equal if optimal")
  print(minimax(s0, "X"), minimax(s1, "O"))
  print(minimax(s2, "X"), minimax(s3, "O"))
  print(minimax(s4, "X"), minimax(s5, "O"))

  print("O Moves: Equal if optimal")
  print(minimax(s1, "O"), minimax(s2, "X"))
  print(minimax(s3, "O"), minimax(s4, "X"))
  print(minimax(s5, "O"), minimax(s6, "X"))

  print("Alternate O moves")
  print(minimax(s1, "O"), minimax(s2optimal, "X"))
  print(minimax(s3, "O"), minimax(s4optimal, "X"))

  print("Alternate X moves")
  print(minimax(s2, "X"), minimax(s3optimal, "O"))

  """
  X Moves:
  minimax(s0) = 0, minimax(s1) = 0: Optimal
  minimax(s2) = 1, minimax(s3) = 0: Not Optimal
  minimax(s4) = 1, minimax(s5) = 1: Optimal

  O Moves:
  minimax(s1) = 0, minimax(s2) = 1: Not Optimal
  minimax(s3) = 0, minimax(s4) = 1: Not Optimal
  minimax(s5) = 1, minimax(s6) = 1: Optimal

  O made a sub-optimal move between s1 and s2
  optimal moves would have been:
  - O at (1, 1)

  X made a sub-optimal move between s2 and s3
  - X at (2, 0)
  - X at (0, 2)

  O made a sub-optimal move between s3 and s4
  - O at (0, 2)
  - O at (1, 2)
  - O at (1, 1)

  """