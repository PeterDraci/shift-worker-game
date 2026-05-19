import pygame
from engine.tile_definitions import is_interactable, get_tile_name
from engine.quest_manager import QuestManager
from engine.inventory_system import Inventory

def get_nearby_interactable(player, game_map, radius=32):
    px, py = player.x, player.y
    for ty in range(max(0, (py - radius) // 8), min(game_map.height, (py + radius) // 8 + 1)):
        for tx in range(max(0, (px - radius) // 8), min(game_map.width, (px + radius) // 8 + 1)):
            tile = game_map.grid[ty][tx]
            if is_interactable(tile):
                dist = ((tx * 8 + 4 - px) ** 2 + (ty * 8 + 4 - py) ** 2) ** 0.5
                if dist < radius:
                    return tx, ty, tile
    return None

def handle_interaction(key, player, game_map, quest_mgr, inventory):
    if key != pygame.K_e:
        return ""
    nearby = get_nearby_interactable(player, game_map)
    if not nearby:
        return ""
    tx, ty, tile = nearby
    name = get_tile_name(tile)
    if tile == 2 and quest_mgr.is_active("activate_computer"):
        quest_mgr.advance("restore_power")
        return "Computer activated. First quest complete."
    elif tile == 3 and quest_mgr.is_active("restore_power"):
        quest_mgr.advance("collect_components")
        return "Generator activated. Power restored."
    elif tile == 4 and quest_mgr.is_active("collect_components"):
        if game_map.collect_component(tx, ty):
            inventory.add_component()
            return f"COMPONENT COLLECTED ({game_map.collected_count()}/{game_map.total_components()})"
        return ""
    elif tile == 5 and quest_mgr.is_active("collect_components"):
        if game_map.all_components_collected() and inventory.assemble_device(game_map):
            quest_mgr.advance("unlock_door")
            return "ALL COMPONENTS ACQUIRED - Device assembled!"
        return "MORE COMPONENTS REQUIRED"
    elif tile == 6 and quest_mgr.is_active("unlock_door") and inventory.device:
        game_map.grid[ty][tx] = 0  # unlock to floor
        quest_mgr.advance("reach_exit")
        return "DOOR UNLOCKED - ACCESS GRANTED"
    elif tile == 9 and quest_mgr.is_active("reach_exit"):
        quest_mgr.advance("completed")
        return "MISSION COMPLETE"
    return f"Interacted with {name}"