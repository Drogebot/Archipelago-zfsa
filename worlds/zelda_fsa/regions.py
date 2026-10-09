from typing import TYPE_CHECKING

from BaseClasses import CollectionState, Region, ItemClassification
from .items import ZfsaItem
from .locations import ZfsaLocation
from .static_logic import ALL_REGIONS, ZfsaRegion, Key, Chest, Requirements, ItemType

if TYPE_CHECKING:
    from . import ZfsaWorld


def zfsa_requirements_satisfied(state: CollectionState, requirements: Requirements, world: "ZfsaWorld"):
    my_items: ItemType = ItemType.none
    if state.has("Progressive Pegasus Boots", world.player):
        my_items |= ItemType.pegasus_boots
    if state.has("Progressive Pegasus Boots", world.player, 2):
        my_items |= ItemType.pegasus_bootsL2
    if state.has("Progressive Lamp", world.player):
        my_items |= ItemType.lamp
    if state.has("Progressive Lamp", world.player, 2):
        my_items |= ItemType.lampL2
    if state.has("Progressive Boomerang", world.player):
        my_items |= ItemType.boomerang
    if state.has("Progressive Boomerang", world.player, 2):
        my_items |= ItemType.boomerangL2
    if state.has("Progressive Bow", world.player):
        my_items |= ItemType.bow
    if state.has("Progressive Bow", world.player, 2):
        my_items |= ItemType.bowL2
    if state.has("Progressive Magic Hammer", world.player):
        my_items |= ItemType.magic_hammer
    if state.has("Progressive Magic Hammer", world.player, 2):
        my_items |= ItemType.magic_hammerL2
    if state.has("Progressive Fire Rod", world.player):
        my_items |= ItemType.fire_rod
    if state.has("Progressive Fire Rod", world.player, 2):
        my_items |= ItemType.fire_rodL2
    if state.has("Progressive Roc's Feather", world.player):
        my_items |= ItemType.rocs_feather
    if state.has("Progressive Roc's Feather", world.player, 2):
        my_items |= ItemType.rocs_featherL2
    if state.has("Progressive Bombs", world.player):
        my_items |= ItemType.bombs
    if state.has("Progressive Bombs", world.player, 2):
        my_items |= ItemType.bombsL2
    if state.has("Progressive Shovel", world.player):
        my_items |= ItemType.shovel
    if state.has("Progressive Shovel", world.player, 2):
        my_items |= ItemType.shovelL2
    if state.has("Progressive Slingshot", world.player):
        my_items |= ItemType.slingshot
    if state.has("Progressive Slingshot", world.player, 2):
        my_items |= ItemType.slingshotL2

    has_items: bool = len(requirements.items) == 0
    for reqs in requirements.items:
        has_set_items: bool = True
        for req in reqs:
            if my_items & req == ItemType(0):
                has_set_items = False
        if has_set_items:
            has_items = True
    if not has_items:
        return False

    if requirements.power_bracelet and not state.has("Power Bracelet", world.player):
        return False

    if requirements.jewels and not (state.has("Blue Royal Jewel", world.player) and state.has("Green Royal Jewel", world.player) and state.has("Red Royal Jewel", world.player) and state.has("Purple Royal Jewel", world.player)):
        return False

    for key in requirements.keys:
        if not state.has(key.name, world.player, key.amount):
            return False
    
    if requirements.special_the_swamp and not (state.has("The Swamp Moon Gate", world.player) or state.has("Progressive Roc's Feather", world.player, 2) or state.has("Progressive Pegasus Boots", world.player, 2)):
        return False
    
    if requirements.special_temple_of_darkness and not (state.has("Temple of Darkness Progressive Key", world.player) or state.has("Progressive Roc's Feather", world.player)):
        return False
    
    if requirements.special_palace_of_winds and not (state.has("Palace of Winds Progressive 2F North Key", world.player, 2) or (state.has("Progressive Roc's Feather", world.player) or state.has("Progressive Pegasus Boots", world.player, 2)) and state.has("Progressive Bombs", world.player)):
        return False
    
    #options
    if world.options.lamp_for_dark and requirements.lamp_for_dark and my_items & (ItemType.lamp) == ItemType(0):
        return False
    
    if not world.options.minor_tricks:
        if requirements.projectile_regroup and my_items & (ItemType.bow | ItemType.fire_rod | ItemType.rocs_feather | ItemType.bombs | ItemType.slingshot | ItemType.pegasus_bootsL2) == ItemType(0):
            return False
        if requirements.bomb_regroup and my_items & (ItemType.bombs)  == ItemType(0):
            return False
        if requirements.helmaroc_regroup and my_items & (ItemType.magic_hammer | ItemType.bombs) == ItemType(0):
            return False
        if requirements.bowless_gohma and my_items & (ItemType.bow) == ItemType(0):
            return False
    
    return True


def zfsa_can_get_key(state: CollectionState, key: Key, world: "ZfsaWorld"):
    return zfsa_requirements_satisfied(state, key.requirements, world)


def zfsa_can_get_chest(state: CollectionState, chest: Chest, world: "ZfsaWorld"):
    return zfsa_requirements_satisfied(state, chest.requirements, world)


def zfsa_can_use_entrance(state: CollectionState, region: ZfsaRegion, parent, ticket, world: "ZfsaWorld"):
    if region.requirements.jewels and not (state.has("Blue Royal Jewel", world.player) and state.has("Green Royal Jewel", world.player) and state.has("Red Royal Jewel", world.player) and state.has("Purple Royal Jewel", world.player)):
        return False
    #return True
    if world.options.level_access == 1:
        if ticket is None:
            return True
        else:
            (ticket_name, ticket_number) = ticket
            return state.has(ticket_name, world.player, ticket_number)
    else:
        if region.parentRegion is None:
            return True
        else:
            return state.can_reach_region(parent.name, world.player) and zfsa_requirements_satisfied(state, parent.requirements, world)


def make_key_lambda(key: Key, world: "ZfsaWorld"):
    return lambda state: zfsa_can_get_key(state, key, world)


def make_chest_lambda(chest: Chest, world: "ZfsaWorld"):
    return lambda state: zfsa_can_get_chest(state, chest, world)


def make_entrance_lambda(region: ZfsaRegion, parent, ticket, world: "ZfsaWorld"):
    return lambda state: zfsa_can_use_entrance(state, region, parent, ticket, world)


def create_region(region: ZfsaRegion, world: "ZfsaWorld"):
    new_region = Region(region.name, world.player, world.multiworld)
    #for key in region.keys:
    #    new_location = ZfsaLocation(world.player, f"{region.name} - {key.name}", key.id, new_region)
    #    new_location.access_rule = make_key_lambda(key, world)
    #    new_region.locations.append(new_location)
    for chest in region.chests:
        new_location = ZfsaLocation(world.player, f"{region.name} - {chest.name}", chest.id, new_region)
        new_location.access_rule = make_chest_lambda(chest, world)
        new_region.locations.append(new_location)
    
    location_name = f"{region.name} - Stage Clear"
    location_id = region.id
    if region.name == "Palace of Winds":
        location_name = f"Palace of Winds - Ganon's Defeat!"
        location_id = None
    
    new_location = ZfsaLocation(world.player, location_name, location_id, new_region)
    new_location.access_rule = lambda state: zfsa_requirements_satisfied(state, region.requirements, world)
    new_region.locations.append(new_location)
    
    if region.name == "Palace of Winds":
        event_item = ZfsaItem("Victory", ItemClassification.progression, None, world.player)
        new_location.place_locked_item(event_item)
        world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)

    return new_region


def create_regions(world: "ZfsaWorld"):
    regions = {
        "Menu": Region("Menu", world.player, world.multiworld)
    }

    for region_name in ALL_REGIONS:
        region = ALL_REGIONS[region_name]
        regions[region.name] = create_region(region, world)
        parent = None if region.parentRegion is None else ALL_REGIONS[region.parentRegion]
        ticket = (f"Progressive Level {(int(region.stageId/10))} Ticket", 2 if region.stageId%10 == 3 else 1) if region.stageId%10 > 0 else None
        regions["Menu"].connect(regions[region.name], None, make_entrance_lambda(region, parent, ticket, world))

    world.multiworld.regions += regions.values()
