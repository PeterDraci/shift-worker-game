# Game Loop

**Pipeline**:
1. Input (WASD / arrows)
2. Movement + collision check
3. Interaction check (on current tile)
4. Render map + player

Runs at 60 FPS using pygame clock. State tracked in game_state.py (inventory, mission complete).