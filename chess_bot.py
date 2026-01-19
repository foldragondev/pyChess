import random

class ChessBot:
    def __init__(self, color):
        self.color = color
        self.piece_values = {
            'P': 1,
            'N': 3,
            'B': 3,
            'R': 5,
            'Q': 9,
            'K': 0  # King is invaluable
        }

    def evaluate_board(self, board):
        score = 0
        for r in range(8):
            for c in range(8):
                piece = board.grid[r][c]
                if piece:
                    val = self.piece_values.get(piece.name, 0)
                    if piece.color == self.color:
                        score += val
                    else:
                        score -= val
        return score

    def get_move(self, game):
        valid_moves = game.get_all_valid_moves(self.color)
        if not valid_moves:
            return None

        # Simple strategy: Try to capture pieces or pick a random move
        best_moves = []
        max_score = -float('inf')

        for move_str in valid_moves:
            # Simulate move
            start_col = ord(move_str[0]) - ord('a')
            start_row = 8 - int(move_str[1])
            end_col = ord(move_str[2]) - ord('a')
            end_row = 8 - int(move_str[3])
            
            original_piece = game.board.grid[end_row][end_col]
            moving_piece = game.board.grid[start_row][start_col]
            
            game.board.grid[end_row][end_col] = moving_piece
            game.board.grid[start_row][start_col] = None
            
            score = self.evaluate_board(game.board)
            
            # Undo move
            game.board.grid[start_row][start_col] = moving_piece
            game.board.grid[end_row][end_col] = original_piece
            
            if score > max_score:
                max_score = score
                best_moves = [move_str]
            elif score == max_score:
                best_moves.append(move_str)

        return random.choice(best_moves)
