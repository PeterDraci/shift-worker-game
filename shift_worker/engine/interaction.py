def check_interaction(player, grid, inventory):
    tile = grid[player.y][player.x]
    msg = ""
    if tile == 'C':
        inventory['items'] += 1
        msg = "Item collected!"
    elif tile == 'D' and inventory['items'] > 0:
        inventory['delivered'] += 1
        inventory['items'] = 0
        msg = "Delivery complete!"
    elif tile == 'M':
        msg = "Machine triggered!"
    return msg