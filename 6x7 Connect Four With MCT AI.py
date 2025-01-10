import os
import time
import copy
import math
import random

# Attempt to import items used in Jupyter. If they don't exist, code will still work in terminal.
try:
    from IPython.display import clear_output
except ImportError:
    # If IPython is not available, we just won't use clear_output
    clear_output = None

###############################################################################
#                       ENVIRONMENT-DETECTION & CLEARING                      #
###############################################################################

def environment_is_jupyter():
    """
    Returns True if the code is running in a Jupyter notebook environment,
    and False if in a standard Python environment (e.g., terminal or IDE).
    """
    try:
        from IPython import get_ipython
        if get_ipython() and 'IPKernelApp' in get_ipython().config:
            return True
        else:
            return False
    except:
        return False

def clear_screen():
    """
    Clears the screen using:
      - IPython's clear_output(wait=True) if in a Jupyter notebook
      - The 'cls' command if on Windows in a terminal
      - The 'clear' command on non-Windows in a terminal
    """
    if environment_is_jupyter() and clear_output is not None:
        # We're in a Jupyter environment
        clear_output(wait=True)
    else:
        # We're in a standard Python environment
        os.system('cls' if os.name == 'nt' else 'clear')

###############################################################################
#                               BOARD SETUP                                   #
###############################################################################

# Initialize the board (6 rows x 7 columns)
board_game = [[" " for _ in range(7)] for _ in range(6)]
players = ["X", "O"]

def display_board(game):
    """
    Displays the current state of the game board.
    Handles both Jupyter notebook (with clear_output) and terminal environments.
    
    :param game: A 2D list (6x7) representing the Connect Four board
    """
    # Pause briefly to let the user see the previous board state
    time.sleep(2)
    # Clear the screen (works for both Jupyter notebook and terminal)
    clear_screen()

    # Print the column header (0 through 6)
    column_numbers = '  ' + '   '.join(map(str, range(len(game[0]))))
    print(column_numbers)
    print('+' + '---+' * len(game[0]))
    
    # Print each row with separators
    for row in game:
        row_display = '| ' + ' | '.join(row) + ' |'
        print(row_display)
        print('+' + '---+' * len(game[0]))

def board_filled(board):
    """
    Checks whether the board is completely filled up or not.
    
    :param board: 2D list representing the board
    :return: True if the board is fully filled; False otherwise
    """
    board_length = len(board)
    column_length = len(board[0])
    
    for row_index in range(board_length):
        for column_index in range(column_length):
            if board[row_index][column_index] == " ":
                return False
    return True

###############################################################################
#                           WIN / DRAW DETECTION                              #
###############################################################################

def left_horizontal_check(board):
    """
    Checks each row from left to right for a horizontal 4-in-a-row.
    
    :param board: 2D list representing the board
    :return: (True, 'X' or 'O') if there's a winning line, otherwise (False, None)
    """
    window_size = 4
    for row in board:
        # Create tuples of length 4 sliding across the row
        array = zip(*[row[i:] for i in range(window_size)])
        for window in array:
            if all(disc == window[0] and disc != " " for disc in window):
                return True, window[0]
    return False, None

def right_horizontal_check(board):
    """
    Checks each row from right to left for a horizontal 4-in-a-row.
    
    :param board: 2D list representing the board
    :return: (True, 'X' or 'O') if there's a winning line, otherwise (False, None)
    """
    # Slide from indices 6 down to 3
    for row in board:
        array = zip(*[row[i::-1] for i in range(6, 2, -1)])
        for window in array:
            if all(disc == window[0] and disc != " " for disc in window):
                return True, window[0]
    return False, None

def top_vertical_check(board):
    """
    Checks for a vertical 4-in-a-row from top to bottom.
    
    :param board: 2D list representing the board
    :return: (True, 'X' or 'O') if there's a winning line, otherwise (False, None)
    """
    # Transpose the board so columns become rows
    board_transposed = [list(combo) for combo in zip(*board)]
    column_length = len(board_transposed)
    window_size = 4
    for column_index in range(column_length):
        array = zip(*[board_transposed[column_index][i:] for i in range(window_size)])
        for window in array:
            if all(window[0] == item and window[0] != " " for item in window):
                return True, window[0]
    return False, None

def bottom_vertical_check(board):
    """
    Checks for a vertical 4-in-a-row from bottom to top.
    
    :param board: 2D list representing the board
    :return: (True, 'X' or 'O') if there's a winning line, otherwise (False, None)
    """
    board_transposed = [list(combo) for combo in zip(*board)]
    column_length = len(board_transposed)
    # Slide from the bottom (row 5) up to row 2
    for column_index in range(column_length):
        array = zip(*[board_transposed[column_index][i::-1] for i in range(5, 1, -1)])
        for window in array:
            if all(window[0] == item and window[0] != " " for item in window):
                return True, window[0]
    return False, None

def right_downwards_diagonal_check(board):
    """
    Checks for a diagonal 4-in-a-row going from top-left to bottom-right.
    
    :param board: 2D list representing the board
    :return: (True, 'X' or 'O') if a diagonal 4-in-a-row is found, otherwise (False, None)
    """
    for row_index in range(3):
        for column_index in range(4):
            disc = board[row_index][column_index]
            if disc != " ":
                diag = [disc]
                trigger = 0
                next_row = row_index + 1
                next_column = column_index + 1
                while trigger <= 2:
                    diag.append(board[next_row][next_column])
                    trigger += 1
                    next_row += 1
                    next_column += 1
                if all(i == disc for i in diag):
                    return True, disc
    return False, None

def right_upwards_diagonal_check(board):
    """
    Checks for a diagonal 4-in-a-row going from bottom-left to top-right.
    
    :param board: 2D list representing the board
    :return: (True, 'X' or 'O') if a diagonal 4-in-a-row is found, otherwise (False, None)
    """
    for row_index in range(5, 2, -1):
        for column_index in range(4):
            disc = board[row_index][column_index]
            if disc != " ":
                diag = [disc]
                trigger = 0
                next_row = row_index - 1
                next_column = column_index + 1
                while trigger <= 2:
                    diag.append(board[next_row][next_column])
                    trigger += 1
                    next_row -= 1
                    next_column += 1
                if all(i == disc for i in diag):
                    return True, disc
    return False, None

def left_downwards_diagonal_check(board):
    """
    Checks for a diagonal 4-in-a-row going from top-right to bottom-left.
    
    :param board: 2D list representing the board
    :return: (True, 'X' or 'O') if a diagonal 4-in-a-row is found, otherwise (False, None)
    """
    for row_index in range(3):
        for column_index in range(6, 2, -1):
            disc = board[row_index][column_index]
            if disc != " ":
                diag = [disc]
                trigger = 0
                next_row = row_index + 1
                next_column = column_index - 1
                while trigger <= 2:
                    diag.append(board[next_row][next_column])
                    trigger += 1
                    next_row += 1
                    next_column -= 1
                if all(i == disc for i in diag):
                    return True, disc
    return False, None

def left_upwards_diagonal_check(board):
    """
    Checks for a diagonal 4-in-a-row going from bottom-right to top-left.
    
    :param board: 2D list representing the board
    :return: (True, 'X' or 'O') if a diagonal 4-in-a-row is found, otherwise (False, None)
    """
    for row_index in range(5, 2, -1):
        for column_index in range(6, 2, -1):
            disc = board[row_index][column_index]
            if disc != " ":
                diag = [disc]
                trigger = 0
                next_row = row_index - 1
                next_column = column_index - 1
                while trigger <= 2:
                    diag.append(board[next_row][next_column])
                    trigger += 1
                    next_row -= 1
                    next_column -= 1
                if all(i == disc for i in diag):
                    return True, disc
    return False, None

def full_winning_check(board):
    """
    Aggregates all winning checks (horizontal, vertical, diagonal).
    
    :param board: 2D list representing the board
    :return: (True, 'X' or 'O') if there's a winner, otherwise (False, None)
    """
    function_list = [
        left_horizontal_check,
        right_horizontal_check,
        right_downwards_diagonal_check,
        left_downwards_diagonal_check,
        right_upwards_diagonal_check,
        left_upwards_diagonal_check,
        top_vertical_check,
        bottom_vertical_check
    ]
    
    for function in function_list:
        outcome, winner = function(board)
        if winner:
            return outcome, winner
    # If none of the checks found a winner
    return False, None

def draw_check(board):
    """
    Checks if the game has reached a draw state (board filled + no winner).
    
    :param board: 2D list representing the board
    :return: True if it's a draw, False otherwise
    """
    if board_filled(board) and not full_winning_check(board)[1]:
        return True
    else:
        return False

###############################################################################
#                       HUMAN MOVE (Player X) FUNCTION                        #
###############################################################################

def disc_drop(board, player):
    """
    Prompts the human player for a column choice, then returns (lowest_row, drop_column).

    :param board: 2D list representing the current board
    :param player: The player's symbol ("X" or "O") - here it's always "X" for human
    :return: (lowest_row, drop_column) where the disc will be placed
    """
    board_length = len(board)
    column_length = len(board[0])
    while True:
        try:
            drop_column = int(input(f"Hi player {player}, which column do you want to place your disc? "))
            # Ensure column is valid
            if drop_column < 0 or drop_column > (column_length - 1):
                print(f"Sorry, choose a number between 0 and {column_length - 1}")
                continue
            # Ensure the top cell is empty
            if board[0][drop_column] != " ":
                print(f"Sorry, that column is filled. Please choose a different column.")
                continue
        except ValueError:
            print("Sorry, only integers allowed.")
            time.sleep(2)
            continue
        else:
            # Find the lowest empty row in that column
            lowest_row = 0
            for row_index in range(board_length):
                if board[row_index][drop_column] == " ":
                    lowest_row = row_index
                else:
                    break
            print(f"Thanks, you have placed your disc at (Row {lowest_row}, Column {drop_column})")
            break

    return lowest_row, drop_column

###############################################################################
#                               MCTS CLASSES & FUNCS                          #
###############################################################################

class MCTSNode:
    """
    A node in the Monte Carlo Tree Search (MCTS) tree.

    Attributes:
        board (list): A deep copy of the board state at this node.
        player_to_move (str): Indicates whether 'X' or 'O' is to move.
        parent (MCTSNode): Pointer to the parent node in the MCTS tree (None for root).
        children (dict): A dictionary { move: child_node }, where move is the column chosen.
        visits (int): Number of times this node was visited during MCTS.
        wins (int): Number of wins from 'O's perspective (or whichever perspective is chosen).
    """
    def __init__(self, board, player_to_move, parent=None):
        self.board = board
        self.player_to_move = player_to_move  # 'X' or 'O'
        self.parent = parent
        self.children = {}  # key: column move, value: child node
        self.visits = 0
        self.wins = 0      # Tracking wins from O's perspective
    
    def is_fully_expanded(self):
        """
        Returns True if every valid move from this board state has a child node.
        If the number of children equals the number of valid moves, it's fully expanded.
        """
        possible_moves = get_valid_moves(self.board)
        return len(possible_moves) == len(self.children)
    
    def best_child(self, c_param=1.4142):
        """
        Returns the child node with the highest UCB1 score.
        
        UCB1 = (child.wins / child.visits) + c_param * sqrt(ln(self.visits) / child.visits)
        
        :param c_param: Exploration parameter (commonly sqrt(2) ~ 1.4142)
        :return: The MCTSNode child with the best UCB1 value
        """
        best_score = float("-inf")
        best_child_node = None
        
        for move, child in self.children.items():
            # If a child has 0 visits, return it immediately to explore
            if child.visits == 0:
                return child
            
            exploit = child.wins / child.visits
            explore = math.sqrt(math.log(self.visits) / child.visits)
            ucb1 = exploit + c_param * explore
            
            if ucb1 > best_score:
                best_score = ucb1
                best_child_node = child
        
        return best_child_node

def get_valid_moves(board):
    """
    Returns a list of valid columns where a disc can be played.
    A move is valid if the top cell of that column (row=0) is empty.
    
    :param board: 2D list representing the board
    :return: List of valid columns (integers)
    """
    valid_moves = []
    for col in range(len(board[0])):
        if board[0][col] == " ":
            valid_moves.append(col)
    return valid_moves

def make_move(board, col, player):
    """
    Returns a *deep copy* of the board with the move (player disc) placed in the specified column.
    
    :param board: 2D list representing the board
    :param col: Column to drop a disc in
    :param player: 'X' or 'O'
    :return: A new 2D list (copy) with the updated move
    """
    new_board = copy.deepcopy(board)
    for row_index in range(len(new_board)):
        if new_board[row_index][col] == " ":
            lowest_row = row_index
        else:
            break
    new_board[lowest_row][col] = player
    return new_board

def switch_player(player):
    """
    Switches from 'X' to 'O' or from 'O' to 'X'.
    
    :param player: Current player's symbol ('X' or 'O')
    :return: The symbol of the next player
    """
    return "O" if player == "X" else "X"

def expand_node(node):
    """
    Expands the given MCTSNode by creating one new child for a valid move
    that hasn’t been tried (has no child node yet).
    
    :param node: The current MCTSNode to expand
    :return: The newly created child node, or None if fully expanded
    """
    moves = get_valid_moves(node.board)
    for move in moves:
        # If this move hasn't been expanded yet, create a child for it
        if move not in node.children:
            new_board = make_move(node.board, move, node.player_to_move)
            new_player_to_move = switch_player(node.player_to_move)
            child_node = MCTSNode(new_board, new_player_to_move, parent=node)
            node.children[move] = child_node
            return child_node
    # No untried moves remain
    return None

def rollout_policy_random(board, player_to_move):
    """
    Simulates a random play-out (rollout) from the current board state until it ends.
    Returns the winner if there is one, otherwise None (for draw).
    
    :param board: A 2D list representing the current board state
    :param player_to_move: 'X' or 'O' indicating who moves next
    :return: 'X', 'O', or None (if draw)
    """
    current_player = player_to_move
    working_board = copy.deepcopy(board)
    
    # Keep playing random moves until game ends
    while True:
        outcome, winner = full_winning_check(working_board)
        if winner:
            return winner
        if draw_check(working_board):
            return None  # Means a draw occurred
        
        valid_cols = get_valid_moves(working_board)
        col = random.choice(valid_cols)
        working_board = make_move(working_board, col, current_player)
        current_player = switch_player(current_player)

def backpropagate(node, winner):
    """
    Backpropagates the result of a rollout simulation up the tree.
    Increments the visit count of each node along the path,
    and increments the win count if the winner is 'O'.
    
    :param node: The MCTSNode from which we start backpropagating (the leaf node)
    :param winner: 'X', 'O', or None (if draw)
    """
    current_node = node
    while current_node is not None:
        current_node.visits += 1
        # If 'O' won, increment wins. This means we're tracking from O’s perspective.
        if winner == "O":
            current_node.wins += 1
        current_node = current_node.parent

def mcts_search(root, iterations=1000):
    """
    Performs the core MCTS loop (selection, expansion, simulation, backpropagation).
    After 'iterations' number of simulations, returns the move with the highest visit count.
    
    :param root: The root MCTSNode
    :param iterations: Number of MCTS iterations to run
    :return: The best move (column) according to visit counts
    """
    for _ in range(iterations):
        # 1. Selection
        node = root
        # Traverse until we get to a node that is not fully expanded or has no children
        while node.is_fully_expanded() and node.children:
            node = node.best_child()
        
        # 2. Expansion (only if game is not already in a terminal state)
        if not full_winning_check(node.board)[1] and not draw_check(node.board):
            child = expand_node(node)
            if child is not None:
                node = child
        
        # 3. Simulation (rollout)
        winner = rollout_policy_random(node.board, node.player_to_move)
        
        # 4. Backpropagation
        backpropagate(node, winner)
    
    # After all simulations, pick the child with the highest visit count
    # root.children is a dict of {move: child}
    best_move, best_child_node = max(root.children.items(), key=lambda item: item[1].visits)
    return best_move

def get_ai_move(board):
    """
    Builds a root MCTSNode for the AI (Player 'O') and runs MCTS to decide the best column.
    
    :param board: The current 2D list representing the board
    :return: The best column (int) as determined by MCTS
    """
    # Create a root node from O's perspective
    root = MCTSNode(copy.deepcopy(board), "O", parent=None)
    
    # Number of simulations to run; increase for more thinking time/stronger AI
    NUM_SIMULATIONS = 500
    best_column = mcts_search(root, iterations=NUM_SIMULATIONS)
    
    return best_column

###############################################################################
#                               GAMEPLAY LOOP                                 #
###############################################################################

turn = 0  # 0 means it's X's turn (human), 1 means it's O's turn (AI)

def game_play(board):
    """
    Main gameplay loop for Connect Four. Manages turns for:
      - Human Player X
      - MCTS AI Player O
    
    :param board: A 2D list representing the game board (6x7)
    :return: String denoting the end-game status: "Game Over, It is a Draw" or "Player X has won" or "Player O has won"
    """
    display_board(board)
    while True:
        # Check for draw
        if draw_check(board):
            return "Game Over, It is a Draw"
        
        # Check for winner
        outcome, winner = full_winning_check(board)
        if winner:
            return f"Player {winner} has won the game"
        
        # Human player X
        if turn == 0:
            print("It is Player X (Human)'s turn.")
            chosen_row, chosen_column = disc_drop(board, "X")
            board[chosen_row][chosen_column] = "X"
            
            display_board(board)
            
            # Switch to AI
            update_turn()
        
        # AI player O
        else:
            print("It is Player O (MCTS AI)'s turn.")
            col = get_ai_move(board)
            # Place the disc for O
            for row_index in range(len(board)):
                if board[row_index][col] == " ":
                    lowest_row = row_index
                else:
                    break
            board[lowest_row][col] = "O"
            print(f"AI chooses column {col}.")
            
            display_board(board)
            
            # Switch back to human
            update_turn()

def update_turn():
    """
    Alternates the global 'turn' variable between 0 and 1:
      - 0 = Human (X)
      - 1 = AI (O)
    """
    global turn
    if turn == 0:
        turn = 1
    else:
        turn = 0

# Run the game if this file is executed as a script.
if __name__ == "__main__":
    result = game_play(board_game)
    print(result)