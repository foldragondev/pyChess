import copy
import random

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
        print("\n   a b c d e f g h")
        print("  -----------------")
        for r in range(8):
            row_str = f"{8-r} |"
            for c in range(8):
                piece = self.grid[r][c]
                row_str += (piece.symbol if piece else ".") + " "
            print(row_str + f"| {8-r}")
        print("  -----------------")
        print("   a b c d e f g h\n")

class Game:
    def __init__(self):
        self.board = Board()
        self.turn = 'white'
        self.game_over = False

    def parse_san(self, san_move):
        """
        Parses Standard Algebraic Notation (SAN) like e4, Nf3, Qxe6.
        """
        san_move = san_move.replace('+', '').replace('#', '')
        if san_move == "O-O" or san_move == "O-O-O":
            return None # Castling not implemented

        # Determine piece type
        piece_type = 'P'
        if san_move[0].isupper():
            piece_type = san_move[0]
            san_move = san_move[1:]
        
        # Remove 'x' for captures
        san_move = san_move.replace('x', '')

        # The last two characters are the destination
        if len(san_move) < 2:
            return None
        
        try:
            dest_col = ord(san_move[-2]) - ord('a')
            dest_row = 8 - int(san_move[-1])
        except:
            return None
        
        # Disambiguation (if any)
        disambig_col = None
        disambig_row = None
        if len(san_move) > 2:
            char = san_move[0]
            if 'a' <= char <= 'h':
                disambig_col = ord(char) - ord('a')
            elif '1' <= char <= '8':
                disambig_row = 8 - int(char)

        # Find all legal moves for this piece type to the destination
        possible_moves = []
        for r in range(8):
            for c in range(8):
                piece = self.board.grid[r][c]
                if piece and piece.color == self.turn and piece.name == piece_type:
                    if self.is_valid_move((r, c), (dest_row, dest_col)):
                        if disambig_col is not None and c != disambig_col:
                            continue
                        if disambig_row is not None and r != disambig_row:
                            continue
                        
                        # Simulate move to check for check
                        original_piece = self.board.grid[dest_row][dest_col]
                        self.board.grid[dest_row][dest_col] = self.board.grid[r][c]
                        self.board.grid[r][c] = None
                        in_check = self.is_in_check(self.turn)
                        # Undo
                        self.board.grid[r][c] = self.board.grid[dest_row][dest_col]
                        self.board.grid[dest_row][dest_col] = original_piece
                        
                        if not in_check:
                            possible_moves.append(((r, c), (dest_row, dest_col)))

        if len(possible_moves) == 1:
            return possible_moves[0]
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
                                original_piece = self.board.grid[er][ec]
                                self.board.grid[er][ec] = self.board.grid[r][c]
                                self.board.grid[r][c] = None
                                
                                if not self.is_in_check(color):
                                    start_str = chr(ord('a') + c) + str(8 - r)
                                    end_str = chr(ord('a') + ec) + str(8 - er)
                                    moves.append(start_str + end_str)
                                
                                self.board.grid[r][c] = self.board.grid[er][ec]
                                self.board.grid[er][ec] = original_piece
        return moves

    def make_move_san(self, san_move):
        coords = self.parse_san(san_move)
        if not coords:
            return False, f"Invalid or ambiguous move: {san_move}"
        
        start, end = coords
        sr, sc = start
        er, ec = end
        
        self.board.grid[er][ec] = self.board.grid[sr][sc]
        self.board.grid[sr][sc] = None
        self.turn = 'black' if self.turn == 'white' else 'white'
        
        if not self.get_all_valid_moves(self.turn):
            if self.is_in_check(self.turn):
                self.game_over = True
                return True, "Checkmate!"
            else:
                self.game_over = True
                return True, "Stalemate!"
        return True, ""

    def bot_move(self):
        moves = self.get_all_valid_moves(self.turn)
        if not moves:
            return None
        
        best_moves = []
        max_val = -1
        for move_str in moves:
            sc = ord(move_str[0]) - ord('a')
            sr = 8 - int(move_str[1])
            ec = ord(move_str[2]) - ord('a')
            er = 8 - int(move_str[3])
            
            target = self.board.grid[er][ec]
            val = 0
            if target:
                vals = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0}
                val = vals.get(target.name, 0)
            
            if val > max_val:
                max_val = val
                best_moves = [move_str]
            elif val == max_val:
                best_moves.append(move_str)
        
        move_str = random.choice(best_moves)
        sc = ord(move_str[0]) - ord('a')
        sr = 8 - int(move_str[1])
        ec = ord(move_str[2]) - ord('a')
        er = 8 - int(move_str[3])
        piece = self.board.grid[sr][sc]
        
        san = ""
        if piece.name != 'P': san += piece.name
        if self.board.grid[er][ec]: san += 'x'
        san += move_str[2:]
        
        self.board.grid[er][ec] = self.board.grid[sr][sc]
        self.board.grid[sr][sc] = None
        self.turn = 'black' if self.turn == 'white' else 'white'
        
        return san

if __name__ == "__main__":
    game = Game()
    print("Welcome to Python Chess!")
    print("Enter moves in SAN (e.g., e4, Nf3, Qxe6). Type 'quit' to exit.")
    
    while not game.game_over:
        game.board.display()
        if game.turn == 'white':
            move = input("Your move (White): ").strip()
            if move.lower() == 'quit':
                break
            success, msg = game.make_move_san(move)
            if not success:
                print(f"Error: {msg}")
            elif msg:
                print(msg)
        else:
            print("Bot is thinking...")
            bot_san = game.bot_move()
            if bot_san:
                print(f"Bot moved: {bot_san}")
            else:
                print("Game Over!")
                break
    
    game.board.display()
    print("Thanks for playing!")
