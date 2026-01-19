# Terminal Chess

A simple text-based chess game written in Python.

## Features
- **Two Modes**: Player vs Player and Player vs Bot.
- **Move Notation**: Uses coordinate notation (e.g., `e2e4`).
- **Full Rules**: Includes movement rules for all pieces, check detection, and checkmate/stalemate.
- **Bot AI**: A simple bot that evaluates material and makes moves.

## How to Play
1. Run the game:
   ```bash
   python3 main.py
   ```
2. Select the game mode (1 for PvP, 2 for PvB).
3. Enter moves using coordinate notation:
   - `e2e4` moves the piece at e2 to e4.
   - `g1f3` moves the knight at g1 to f3.
4. Type `quit` to exit the game.

## File Structure
- `main.py`: The entry point of the game.
- `chess_engine.py`: Contains the board logic, piece rules, and game state management.
- `chess_bot.py`: Contains the AI logic for the bot.
- `test_chess.py`: A script to verify the core engine logic.
