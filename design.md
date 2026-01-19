# Chess Game Design

## Core Components
- **Board**: 8x8 grid representing the chess board.
- **Pieces**: Classes for each piece type (Pawn, Rook, Knight, Bishop, Queen, King) with their movement rules.
- **Game Engine**: Manages the game state, turn-taking, and move validation.
- **Move Parser**: Converts standard chess notation (e.g., 'e2e4' or 'e4') into board coordinates.
- **Bot AI**: Simple Minimax algorithm with basic evaluation for the bot mode.

## Move Notation
The game will support coordinate notation (e.g., 'e2e4') for simplicity, but I will aim to support basic algebraic notation if possible.

## Game Modes
1. **Player vs Player (PvP)**: Two humans taking turns.
2. **Player vs Bot (PvB)**: Human vs AI.
