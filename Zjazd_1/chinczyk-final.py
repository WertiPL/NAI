#!/usr/bin/python3

"""
Ludo Game, Rostkowski Wiktor, Szenborn Jan, 2023

Rules:
- map is 40 field line, where 1st player starts on n=1 and has finish at n=30, second on n=10 and finish on n=40
- each player can move his pawn by 1, 2 or 3 fields - pawn and amound are choosen by player
- each player can also spawn new pawn; total amount of player' pawns are four
- player cannot spawn new pawn if start field is occupied by his own pawn
- player cannot move pawn into his own pawn
- if player moves pawn onto enemy's pawn, enemy's pawn returns to start base
- if enemy pawn stays in player's spawn, spawning new pawn kills enemy's pawn
- goal is to park all pawns at finish line, then it disappears
- game is finished when one player finish all his pawns

How to run:
- run "pip install easyai"
- run "python3 chinczyk.py"
"""

import sys
from easyAI import TwoPlayerGame, Negamax, Human_Player, AI_Player

class Ludo(TwoPlayerGame):
    """Game rules explained in the comment on the beginning of the file."""

    def __init__(self, players=None):
        self.players = players
        self.board = [None] * 40 # map length of 40
        self.current_player = 1
        self.players_score = [0] * len(players)

    def get_player_boundaries(self, player):
        """
        Calculate start and end (base) for given player.
        Warning: not secured against out-of-bounds error.
        """

        return {
            "start": 0 if player == 1 else 10 * (player - 1) - 1,
            "end": 30 + 10 * (player - 1) - 1
        }

    def move_possible(self, move):
        """
        Get information if given pawn move is a valid move.
        Checks if:
        - pawn after move won't miss end field
        - pawn won't collide with player' pawn
        """

        boundaries = self.get_player_boundaries(self.current_player)
        after_index = boundaries['start'] if move['pawn_index'] == "spawn" else move['pawn_index'] + move['amount']

        if after_index > boundaries['end']:
            return False

        if self.board[after_index] == self.current_player:
            return False

        return True

    def possible_moves(self):
        """
        Calculate all possible moves for current player.
        Checks each spawned pawn possibilities and possibilities to spawn new pawns.
        """

        pawn_count = 0
        result = []

        for index, item in enumerate(self.board):
            # We are looking only for player' pawns
            if (item != self.current_player):
                continue

            # Player pawn found, increase count
            pawn_count += 1

            # Check all possible moves
            for amount in range(1, 3):
                move = {"pawn_index": index, "amount": amount}

                if self.move_possible(move):
                    result.append(move)

        # Calculate amount of pawns in the base
        pawns_finished = self.players_score[self.current_player - 1] / 25

        # Not all pawns already spawned, check if it's possible to spawn next one
        if pawn_count + pawns_finished < 4:
            move = {"pawn_index": "spawn", "amount": 0}

            if self.move_possible(move):
                result.append(move)

        return result

    def make_move(self, move):
        """Make pawn move."""

        boundaries = self.get_player_boundaries(self.current_player)
        current_index = boundaries['start'] if move['pawn_index'] == "spawn" else move['pawn_index']
        after_index = current_index + move['amount']

        # Do real move - set field to new value and clear previous field
        self.board[current_index] = None
        self.board[after_index] = self.current_player

        # If pawn hit last field, hide it to the base (remove) and increase score
        if after_index == boundaries['end']:
            self.board[after_index] = None
            self.players_score[self.current_player - 1] += 25

    def scoring(self):
        return 100 if self.win() else 0

    def win(self):
        """Tell if current player already won the game."""

        return self.players_score[self.current_player - 1] == 100 # All pawns finished

    def is_over(self):
        """Tell if game is ended."""

        return self.win()

    def show(self):
        """Print Ludo board in nice form. Dot is empty cell and number is player index."""

        print("Board: ", end='')

        for field in self.board:
            print('.' if field == None else field, end='')

        print('')

ai = Negamax(10) # The AI will think 10 moves in advance
game = Ludo( [ AI_Player(ai), Human_Player() ] )
history = game.play()
