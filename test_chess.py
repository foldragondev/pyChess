from chess_engine import Game

def test_pawn_move():
    game = Game()
    # White pawn e2 to e4
    success, msg = game.make_move("e2e4")
    assert success == True
    assert game.board.grid[4][4].name == 'P'
    assert game.board.grid[6][4] == None
    print("Pawn move test passed!")

def test_invalid_move():
    game = Game()
    # Try to move black piece on white's turn
    success, msg = game.make_move("e7e5")
    assert success == False
    print("Invalid turn test passed!")

def test_knight_move():
    game = Game()
    # White knight g1 to f3
    success, msg = game.make_move("g1f3")
    assert success == True
    assert game.board.grid[5][5].name == 'N'
    print("Knight move test passed!")

if __name__ == "__main__":
    try:
        test_pawn_move()
        test_invalid_move()
        test_knight_move()
        print("All tests passed!")
    except Exception as e:
        print(f"Test failed: {e}")
