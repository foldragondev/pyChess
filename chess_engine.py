import copy

class Piece:
    def __init__(self, color, name):
        self.color = color
        self.name = name
        self.symbol = self._get_symbol()

    def _get_symbol(self):
        symbols = {
            'white': {'P': '♙', 'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔'},
            'black': {'P': '♟', 'R': '♜', 'N': '♞', 'B': '♝', 'Q': '♛', 'K': '♚'}
        }
        return symbols[self.color][self.name]

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.setup_board()

    def setup_board(self):
        # Setup Pawns
        for i in range(8):
            self.grid[1][i] = Piece('black', 'P')
            self.grid[6][i] = Piece('white', 'P')

        # Setup Rooks
        self.grid[0][0] = self.grid[0][7] = Piece('black', 'R')
        self.grid[7][0] = self.grid[7][7] = Piece('white', 'R')

        # Setup Knights
        self.grid[0][1] = self.grid[0][6] = Piece('black', 'N')
        self.grid[7][1] = self.grid[7][6] = Piece('white', 'N')

        # Setup Bishops
        self.grid[0][2] = self.grid[0][5] = Piece('black', 'B')
        self.grid[7][2] = self.grid[7][5] = Piece('white', 'B')

        # Setup Queens
        self.grid[0][3] = Piece('black', 'Q')
        self.grid[7][3] = Piece('white', 'Q')

        # Setup Kings
        self.grid[0][4] = Piece('black', 'K')
        self.grid[7][4] = Piece('white', 'K')

    def display(self):
        print("   a b c d e f g h")
        print("  -----------------")
        for r in range(8):
            row_str = f"{8-r} |"
            for c in range(8):
                piece = self.grid[r][c]
                row_str += (piece.symbol if piece else ".") + " "
            print(row_str + f"| {8-r}")
        print("  -----------------")
        print("   a b c d e f g h")

class Game:
    def __init__(self):
        self.board = Board()
        self.turn = 'white'
        self.game_over = False

    def parse_move(self, move_str):
        # Basic coordinate notation: e2e4
        try:
            if len(move_str) != 4:
                return None
            start_col = ord(move_str[0]) - ord('a')
            start_row = 8 - int(move_str[1])
            end_col = ord(move_str[2]) - ord('a')
            end_row = 8 - int(move_str[3])
            
            if all(0 <= x < 8 for x in [start_row, start_col, end_row, end_col]):
                return (start_row, start_col), (end_row, end_col)
        except:
            pass
        return None

    def is_valid_move(self, start, end):
        sr, sc = start
        er, ec = end
        piece = self.board.grid[sr][sc]

        if not piece or piece.color != self.turn:
            return False

        target = self.board.grid[er][ec]
        if target and target.color == self.turn:
            return False

        # Basic movement rules (simplified for now)
        dr = er - sr
        dc = ec - sc

        if piece.name == 'P':
            direction = -1 if piece.color == 'white' else 1
            if dc == 0: # Forward
                if dr == direction and not target:
                    return True
                if dr == 2 * direction and ((sr == 6 and piece.color == 'white') or (sr == 1 and piece.color == 'black')) and not target and not self.board.grid[sr+direction][sc]:
                    return True
            elif abs(dc) == 1 and dr == direction: # Capture
                if target and target.color != piece.color:
                    return True
            return False

        if piece.name == 'R':
            if dr != 0 and dc != 0: return False
            return self._is_path_clear(start, end)

        if piece.name == 'B':
            if abs(dr) != abs(dc): return False
            return self._is_path_clear(start, end)

        if piece.name == 'Q':
            if not (dr == 0 or dc == 0 or abs(dr) == abs(dc)): return False
            return self._is_path_clear(start, end)

        if piece.name == 'N':
            return (abs(dr), abs(dc)) in [(1, 2), (2, 1)]

        if piece.name == 'K':
            return abs(dr) <= 1 and abs(dc) <= 1

        return False

    def _is_path_clear(self, start, end):
        sr, sc = start
        er, ec = end
        dr = 1 if er > sr else -1 if er < sr else 0
        dc = 1 if ec > sc else -1 if ec < sc else 0
        
        curr_r, curr_c = sr + dr, sc + dc
        while (curr_r, curr_c) != (er, ec):
            if self.board.grid[curr_r][curr_c]:
                return False
            curr_r += dr
            curr_c += dc
        return True

    def find_king(self, color):
        for r in range(8):
            for c in range(8):
                piece = self.board.grid[r][c]
                if piece and piece.name == 'K' and piece.color == color:
                    return (r, c)
        return None

    def is_in_check(self, color):
        king_pos = self.find_king(color)
        opponent_color = 'black' if color == 'white' else 'white'
        
        # Temporarily switch turn to opponent to check if they can hit the king
        original_turn = self.turn
        self.turn = opponent_color
        for r in range(8):
            for c in range(8):
                piece = self.board.grid[r][c]
                if piece and piece.color == opponent_color:
                    if self.is_valid_move((r, c), king_pos):
                        self.turn = original_turn
                        return True
        self.turn = original_turn
        return False

    def get_all_valid_moves(self, color):
        moves = []
        for r in range(8):
            for c in range(8):
                piece = self.board.grid[r][c]
                if piece and piece.color == color:
                    for er in range(8):
                        for ec in range(8):
                            if self.is_valid_move((r, c), (er, ec)):
                                # Simulate move to see if it leaves king in check
                                original_piece = self.board.grid[er][ec]
                                self.board.grid[er][ec] = self.board.grid[r][c]
                                self.board.grid[r][c] = None
                                
                                if not self.is_in_check(color):
                                    start_str = chr(ord('a') + c) + str(8 - r)
                                    end_str = chr(ord('a') + ec) + str(8 - er)
                                    moves.append(start_str + end_str)
                                
                                # Undo move
                                self.board.grid[r][c] = self.board.grid[er][ec]
                                self.board.grid[er][ec] = original_piece
        return moves

    def make_move(self, move_str):
        coords = self.parse_move(move_str)
        if not coords:
            return False, "Invalid format. Use e2e4."
        
        start, end = coords
        if not self.is_valid_move(start, end):
            return False, "Invalid move for this piece."

        # Simulate move to check if it leaves king in check
        sr, sc = start
        er, ec = end
        original_piece = self.board.grid[er][ec]
        moving_piece = self.board.grid[sr][sc]
        
        self.board.grid[er][ec] = moving_piece
        self.board.grid[sr][sc] = None
        
        if self.is_in_check(self.turn):
            # Undo move
            self.board.grid[sr][sc] = moving_piece
            self.board.grid[er][ec] = original_piece
            return False, "Move leaves king in check."

        # Move is final
        self.turn = 'black' if self.turn == 'white' else 'white'
        
        # Check for checkmate
        if not self.get_all_valid_moves(self.turn):
            if self.is_in_check(self.turn):
                self.game_over = True
                return True, "Checkmate!"
            else:
                self.game_over = True
                return True, "Stalemate!"
                
        return True, ""

if __name__ == "__main__":
    game = Game()
    game.board.display()
