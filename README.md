# Connect Four Showdown: Test Your Wits and Face Off Against an AI Player

This project is a comprehensive Python implementation of the classic Connect Four (6×7) board game with a twist: Player X is controlled by a human, while Player O is powered by a Monte Carlo Tree Search (MCTS) AI agent. The MCTS algorithm runs numerous random simulations to evaluate potential moves, dynamically refining its strategy as it explores the game tree—creating a challenging and intelligent AI opponent.

The code includes all essential game features:
	•	Board Initialization (6×7)
	•	Interactive User Input for the human player’s moves
	•	Move Validation to ensure legal column placements
	•	Win/Draw Detection via thorough checks (horizontal, vertical, diagonal)
	•	MCTS-Based AI Decision for the opponent’s moves, customizable by tweaking the number of simulations
	•	Adaptive Display that detects whether you’re in a Jupyter notebook or terminal and clears the screen appropriately

With comprehensive docstrings and inline comments, this repository provides a transparent, well-documented codebase. It’s ideal for educational purposes or anyone looking to explore Monte Carlo Tree Search in a classic game scenario.
