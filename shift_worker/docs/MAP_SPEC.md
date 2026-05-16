# Map Specification

The map uses a 2D grid representation (list of strings) as a conceptual reference to the industrial factory layout in assets/img/game_map.png.

**Tile Legend**:
- `#` : Wall (solid, blocks movement)
- `.` : Floor (walkable)
- `S` : Spawn point (player start)
- `C` : Storage/collectible zone
- `D` : Delivery station
- `M` : Machine trigger zone

The grid is 20x7 tiles. The image serves only as visual inspiration for corridors and rooms; the logical grid drives gameplay.