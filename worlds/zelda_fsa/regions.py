from typing import TYPE_CHECKING

from BaseClasses import CollectionState, Region, ItemClassification
from rule_builder.rules import And, Or, Has, CanReachRegion, True_
from .items import ZfsaItem, TICKET_ITEMS
from .locations import ZfsaLocation
from .static_logic import ALL_REGIONS, ZfsaRegion, Key, Chest, Pedestal, Jewel, Requirements, ItemType

if TYPE_CHECKING:
    from . import ZfsaWorld


ITEM_RULES = [
    (ItemType.pegasus_boots, Has("Progressive Pegasus Boots")),
    (ItemType.pegasus_bootsL2, Has("Progressive Pegasus Boots", count=2)),
    (ItemType.lamp, Has("Progressive Lamp")),
    (ItemType.lampL2, Has("Progressive Lamp", count=2)),
    (ItemType.boomerang, Has("Progressive Boomerang")),
    (ItemType.boomerangL2, Has("Progressive Boomerang", count=2)),
    (ItemType.bow, Has("Progressive Bow")),
    (ItemType.bowL2, Has("Progressive Bow", count=2)),
    (ItemType.magic_hammer, Has("Progressive Magic Hammer")),
    (ItemType.magic_hammerL2, Has("Progressive Magic Hammer", count=2)),
    (ItemType.fire_rod, Has("Progressive Fire Rod")),
    (ItemType.fire_rodL2, Has("Progressive Fire Rod", count=2)),
    (ItemType.rocs_feather, Has("Progressive Roc's Feather")),
    (ItemType.rocs_featherL2, Has("Progressive Roc's Feather", count=2)),
    (ItemType.bombs, Has("Progressive Bombs")),
    (ItemType.bombsL2, Has("Progressive Bombs", count=2)),
    (ItemType.shovel, Has("Progressive Shovel")),
    (ItemType.shovelL2, Has("Progressive Shovel", count=2)),
    (ItemType.slingshot, Has("Progressive Slingshot")),
    (ItemType.slingshotL2, Has("Progressive Slingshot", count=2)),
]


def item_mask_rule(mask: ItemType):
    """A rule satisfied by owning any item represented by this bitmask."""
    rules = [
        rule for item_flag, rule in ITEM_RULES
        if mask & item_flag
    ]

    if not rules:
        return None

    return Or(*rules)


def zfsa_requirements_rule(requirements: Requirements, world: "ZfsaWorld"):
    """Convert a ZFSA Requirements object into a rule-builder expression."""
    rules = []

    # Each inner set is an AND; the outer list is an OR.
    # An empty requirements.items list means no item requirement.
    if requirements.items:
        item_set_rules = []

        for item_set in requirements.items:
            required_rules = [
                item_mask_rule(item_mask)
                for item_mask in item_set
            ]

            # An unknown/empty item mask cannot satisfy its requirement.
            if any(rule is None for rule in required_rules):
                item_set_rules.append(None)
            else:
                item_set_rules.append(And(*required_rules))

        valid_item_sets = [
            rule for rule in item_set_rules if rule is not None
        ]

        if not valid_item_sets:
            # No valid alternative can satisfy the item requirement.
            from rule_builder.rules import False_
            rules.append(False_())
        else:
            rules.append(Or(*valid_item_sets))

    if requirements.power_bracelet:
        rules.append(Has("Power Bracelet"))

    if requirements.jewels:
        rules.append(And(
            Has("Blue Royal Jewel"),
            Has("Green Royal Jewel"),
            Has("Red Royal Jewel"),
            Has("Purple Royal Jewel"),
        ))

    for key in requirements.keys:
        rules.append(Has(key.name, count=key.amount))

    if requirements.special_the_mountain_path:
        rules.append(Or(
            Has("Power Bracelet"),
            Has("Progressive Lamp"),
            Has("Progressive Magic Hammer"),
            Has("Progressive Fire Rod"),
        ))

    if requirements.special_the_swamp:
        rules.append(Or(
            Has("The Swamp Moon Gate"),
            Has("Progressive Roc's Feather", count=2),
            Has("Progressive Pegasus Boots", count=2),
        ))

    if requirements.special_temple_of_darkness:
        rules.append(Or(
            Has("Temple of Darkness Progressive Key"),
            Has("Progressive Roc's Feather"),
        ))

    if requirements.special_palace_of_winds:
        rules.append(Or(
            Has("Palace of Winds Progressive 2F North Key", count=2),
            And(
                Or(
                    Has("Progressive Roc's Feather"),
                    Has("Progressive Pegasus Boots", count=2),
                ),
                Has("Progressive Bombs"),
            ),
        ))

    # Options are evaluated while building the rule.
    if world.options.lamp_for_dark and requirements.lamp_for_dark:
        rules.append(Or(
            Has("Progressive Lamp"),
            Has(world.glitches_item_name),
        ))

    if not world.options.minor_tricks:
        trick_rules = []

        if requirements.projectile_regroup:
            trick_rules.append(Or(
                Has("Progressive Bow"),
                Has("Progressive Fire Rod"),
                Has("Progressive Roc's Feather"),
                Has("Progressive Bombs"),
                Has("Progressive Slingshot"),
                Has("Progressive Pegasus Boots", count=2),
            ))

        if requirements.bomb_regroup:
            trick_rules.append(Has("Progressive Bombs"))

        if requirements.helmaroc_regroup:
            trick_rules.append(Or(
                Has("Progressive Magic Hammer"),
                Has("Progressive Bombs"),
            ))

        if requirements.bowless_gohma:
            trick_rules.append(Has("Progressive Bow"))

        if requirements.jump_pound:
            trick_rules.append(Or(
                Has("Progressive Roc's Feather"),
                Has("Progressive Bombs"),
            ))

        if requirements.jump_pound_side:
            trick_rules.append(Or(
                Has("Progressive Pegasus Boots"),
                Has("Progressive Roc's Feather"),
                Has("Progressive Bombs"),
            ))

        if requirements.desert_cactus:
            trick_rules.append(Or(
                Has("Progressive Roc's Feather"),
                Has("Progressive Pegasus Boots", count=2),
            ))

        if requirements.desert_death_clip:
            trick_rules.append(Or(
                Has("Progressive Pegasus Boots", count=2),
                Has("Progressive Roc's Feather", count=2),
            ))

        if requirements.gap_regroup:
            trick_rules.append(Or(
                Has("Progressive Roc's Feather"),
                Has("Progressive Pegasus Boots", count=2),
            ))

        if requirements.gap_big_regroup:
            trick_rules.append(Or(
                Has("Progressive Pegasus Boots", count=2),
                Has("Progressive Roc's Feather", count=2),
            ))

        if requirements.gap_bigest_regroup:
            trick_rules.append(Has("Progressive Pegasus Boots", count=2))

        if requirements.gap_big_bow_regroup:
            trick_rules.append(Or(
                Has("Progressive Bow"),
                Has("Progressive Pegasus Boots", count=2),
                Has("Progressive Roc's Feather", count=2),
            ))

        if trick_rules:
            rules.append(Or(
                And(*trick_rules),
                Has(world.glitches_item_name),
            ))

    return And(*rules) if rules else True_()


def zfsa_key_rule(key: Key, world: "ZfsaWorld"):
    return zfsa_requirements_rule(key.requirements, world)


def zfsa_chest_rule(chest: Chest, world: "ZfsaWorld"):
    return zfsa_requirements_rule(chest.requirements, world)


def zfsa_pedestal_rule(pedestal: Pedestal, world: "ZfsaWorld"):
    return zfsa_requirements_rule(pedestal.requirements, world)


def zfsa_jewel_rule(jewel: Jewel, world: "ZfsaWorld"):
    return zfsa_requirements_rule(jewel.requirements, world)


def zfsa_entrance_rule(region: ZfsaRegion, parent, ticket, world: "ZfsaWorld"):
    rules = []

    if region.requirements.jewels:
        rules.append(And(
            Has("Blue Royal Jewel"),
            Has("Green Royal Jewel"),
            Has("Red Royal Jewel"),
            Has("Purple Royal Jewel"),
            Has("Progressive Maiden", 6),
        ))
    if region.requirements.zelda:
        rules.append(Has("Progressive Maiden", 7))

    if world.options.level_access == 1:
        if ticket is not None:
            ticket_name, ticket_number = ticket
            rules.append(Has(ticket_name, count=ticket_number))
    elif parent is not None:
        rules.append(CanReachRegion(parent.name))
        rules.append(zfsa_requirements_rule(parent.requirements, world))

    return And(*rules) if rules else True_()


def create_region(region: ZfsaRegion, world: "ZfsaWorld"):
    new_region = Region(region.name, world.player, world.multiworld)
    #for key in region.keys:
    #    new_location = ZfsaLocation(world.player, f"{region.name} - {key.name}", key.id, new_region)
    #    world.set_rule(new_location, zfsa_key_rule(key, world))
    #    new_region.locations.append(new_location)
    for chest in region.chests:
        new_location = ZfsaLocation(world.player, f"{region.name} - {chest.name}", chest.id, new_region)
        world.set_rule(new_location, zfsa_chest_rule(chest, world))
        new_region.locations.append(new_location)
    if world.options.item_pedestals:
        for pedestal in region.pedestals:
            new_location = ZfsaLocation(world.player, f"{region.name} - {pedestal.name}", pedestal.id, new_region)
            world.set_rule(new_location, zfsa_pedestal_rule(pedestal, world))
            new_region.locations.append(new_location)
    if region.jewel is not None:
        new_location = ZfsaLocation(world.player, f"{region.name} - {region.jewel.name}", region.jewel.id, new_region)
        world.set_rule(new_location, zfsa_jewel_rule(region.jewel, world))
        new_region.locations.append(new_location)
    
    location_name = f"{region.name} - Stage Clear"
    location_id = region.id
    if region.name == "Palace of Winds":
        location_name = f"Palace of Winds - Ganon's Defeat!"
        location_id = None
    
    new_location = ZfsaLocation(world.player, location_name, location_id, new_region)
    world.set_rule(new_location, zfsa_requirements_rule(region.requirements, world))
    new_region.locations.append(new_location)
    
    if region.name == "Palace of Winds":
        event_item = ZfsaItem("Victory", ItemClassification.progression, None, world.player)
        new_location.place_locked_item(event_item)
        world.set_completion_rule(Has("Victory"))
    elif world.options.level_access != 1:
        ticket = (
            f"Progressive Level {(int(region.stageId/10))} Ticket"
            if region.stageId%10 < 3
            else None
        )
        if ticket is not None:
            ticket_id, _ = TICKET_ITEMS[ticket]
            new_location.place_locked_item(ZfsaItem(ticket, ItemClassification.progression, ticket_id, world.player))

    return new_region


def create_regions(world: "ZfsaWorld"):
    regions = {
        "Menu": Region("Menu", world.player, world.multiworld)
    }
    world.multiworld.regions.append(regions["Menu"])

    for region_name in ALL_REGIONS:
        region = ALL_REGIONS[region_name]
        regions[region.name] = create_region(region, world)
        ticket = (
            (
                f"Progressive Level {(int(region.stageId/10))} Ticket",
                2 if region.stageId%10 == 3 else 1
            )
            if region.stageId%10 > 0
            else None
        )
        parent = None if region.parentRegion is None else ALL_REGIONS[region.parentRegion]
        world.create_entrance(regions["Menu"], regions[region.name], zfsa_entrance_rule(region, parent, ticket, world))
        world.multiworld.regions.append(regions[region.name])
