from chess_engine import Game
from chess_bot import ChessBot
import os

def clear_screen():
    os.system('clear')

def main():
    print("Welcome to Terminal Chess!")
    print("1. Player vs Player")
    print("2. Player vs Bot")
    
    choice = input("Select mode (1/2): ")
    mode = 'pvp' if choice == '1' else 'pvb'
    
    game = Game()
    bot = ChessBot('black') if mode == 'pvb' else None
    
    while not game.game_over:
        clear_screen()
        game.board.display()
        print(f"\n{game.turn.capitalize()}'s turn.")
        
        if game.is_in_check(game.turn):
            print("CHECK!")

        if mode == 'pvb' and game.turn == 'black':
            print("Bot is thinking...")
            move = bot.get_move(game)
            print(f"Bot moves: {move}")
            input("Press Enter to continue...")
        else:
            move = input("Enter move (e.g., e2e4) or 'quit': ").lower()
            if move == 'quit':
                break
        
        success, message = game.make_move(move)
        if not success:
            print(f"Error: {message}")
            input("Press Enter to try again...")
        elif message:
            print(message)
            input("Press Enter to continue...")

    clear_screen()
    game.board.display()
    print("\nGame Over!")
    if game.is_in_check('white'):
        print("Black wins by Checkmate!")
    elif game.is_in_check('black'):
        print("White wins by Checkmate!")
    else:
        print("Draw!")

if __name__ == "__main__":
    main()
