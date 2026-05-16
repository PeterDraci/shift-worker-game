# Shift Worker - Game Design

**Concept**: Top-down tile-based factory delivery game. Player is a shift worker collecting items from storage and delivering them to the station while navigating the industrial layout.

**Core Loop**: Move → Collect item (C) → Deliver to station (D) → Trigger machine events (M) → Repeat.

**Objective**: Complete deliveries by collecting from storage zones and reaching the delivery point. Future phases add locked doors and triggers.

**Systems**:
- Tile map rendering
- WASD movement + collision
- Simple interaction zones for collect/deliver/trigger