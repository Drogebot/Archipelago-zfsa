from BaseClasses import Item
from typing import NamedTuple


class ZfsaItem(Item):
    game: str = "The Legend of Zelda: Four Swords Adventures"
    
BASE_ITEM_OFFSET = 379000

KEY_ITEMS: dict[str, tuple[int, int]] = { # 2 of each
    "Progressive Pegasus Boots": (BASE_ITEM_OFFSET+0, 2),
    "Progressive Lamp": (BASE_ITEM_OFFSET+1, 2),
    "Progressive Boomerang": (BASE_ITEM_OFFSET+2, 2),
    "Progressive Bow": (BASE_ITEM_OFFSET+3, 2),
    "Progressive Magic Hammer": (BASE_ITEM_OFFSET+4, 2),
    "Progressive Fire Rod": (BASE_ITEM_OFFSET+5, 2),
    "Progressive Roc's Feather": (BASE_ITEM_OFFSET+6, 2),
    "Progressive Bombs": (BASE_ITEM_OFFSET+7, 2),
    "Progressive Shovel": (BASE_ITEM_OFFSET+8, 2),
    "Progressive Slingshot": (BASE_ITEM_OFFSET+9, 2),
}

IMPORTANT_ITEMS: dict[str, tuple[int, int]] = {
    "Blue Bracelet": (BASE_ITEM_OFFSET+10, 1), # there is about 19 of these, what do?
    "Power Bracelet": (BASE_ITEM_OFFSET+11, 1), # there is about 4 of these, what do?
    "Heart Piece": (BASE_ITEM_OFFSET+12, 1), # there are about 73(less) heart containers, but only 8 max hearts, 73 1/8ths is 9 hearts. Maybe require 2 pieces per quarter? Maybe start on max quarter heart?
}

TICKET_ITEMS: dict[str, tuple[int, int]] = { # 2 of each
    "Progressive Level 1 Ticket": (BASE_ITEM_OFFSET+13, 2),
    "Progressive Level 2 Ticket": (BASE_ITEM_OFFSET+14, 2),
    "Progressive Level 3 Ticket": (BASE_ITEM_OFFSET+15, 2),
    "Progressive Level 4 Ticket": (BASE_ITEM_OFFSET+16, 2),
    "Progressive Level 5 Ticket": (BASE_ITEM_OFFSET+17, 2),
    "Progressive Level 6 Ticket": (BASE_ITEM_OFFSET+18, 2),
    "Progressive Level 7 Ticket": (BASE_ITEM_OFFSET+19, 2),
    "Progressive Level 8 Ticket": (BASE_ITEM_OFFSET+20, 2),
}

JEWEL_ITEMS: dict[str, tuple[int, int]] = {
    "Blue Royal Jewel": (BASE_ITEM_OFFSET+21, 1),
    "Green Royal Jewel": (BASE_ITEM_OFFSET+22, 1),
    "Red Royal Jewel": (BASE_ITEM_OFFSET+23, 1),
    "Purple Royal Jewel": (BASE_ITEM_OFFSET+24, 1),
}

SAGE_ITEMS: dict[str, tuple[int, int]] = {
    "Progressive Maiden": (BASE_ITEM_OFFSET+25, 7),
}

FORMATION_ITEMS: dict[str, tuple[int, int]] = {
    "Box Formation": (BASE_ITEM_OFFSET+26, 1),
    "Wide Formation": (BASE_ITEM_OFFSET+27, 1),
    "Long Formation": (BASE_ITEM_OFFSET+28, 1),
    "Cross Formation": (BASE_ITEM_OFFSET+29, 1),
    "Split Formation": (BASE_ITEM_OFFSET+30, 1),
}

FORCE_GEM_ITEMS: dict[str, tuple[int, int]] = {
    "Small Green Force Gem": (BASE_ITEM_OFFSET+31, 1),
    "Small Blue Force Gem": (BASE_ITEM_OFFSET+32, 1),
    "Small Red Force Gem": (BASE_ITEM_OFFSET+33, 1),
    "Small Purple Force Gem": (BASE_ITEM_OFFSET+34, 1),
    "Green Force Gem": (BASE_ITEM_OFFSET+35, 1),
    "Blue Force Gem": (BASE_ITEM_OFFSET+36, 1),
    "Red Force Gem": (BASE_ITEM_OFFSET+37, 1),
    "Purple Force Gem": (BASE_ITEM_OFFSET+38, 1),
    "Big Green Force Gem": (BASE_ITEM_OFFSET+39, 1),
    "Big Blue Force Gem": (BASE_ITEM_OFFSET+40, 1),
    "Big Red Force Gem": (BASE_ITEM_OFFSET+41, 1),
    "Big Purple Force Gem": (BASE_ITEM_OFFSET+42, 1),
}

JUNK_ITEMS: dict[str, tuple[int, int]] = {
    **FORCE_GEM_ITEMS,
    #"Bombos Medallion": (BASE_ITEM_OFFSET+43, 1),
    #"Quake Medallion": (BASE_ITEM_OFFSET+44, 1),
    "Nothing": (BASE_ITEM_OFFSET+45, 1), # There are 5 of these
    "Heart": (BASE_ITEM_OFFSET+46, 1),
    "Force Fairy": (BASE_ITEM_OFFSET+47, 1),
}

TRAP_ITEMS: dict[str, tuple[int, int]] = {
    "Tingle Trap": (BASE_ITEM_OFFSET+48, 1),
    "Fire Trap": (BASE_ITEM_OFFSET+49, 1),
    #"Nova Bomb Trap": (BASE_ITEM_OFFSET+50, 1),
}

LEVEL_PROGRESSION_ITEMS: dict[str, tuple[int, int]] = {
    "Lake Hylia House Key": (BASE_ITEM_OFFSET+51, 1), # junk
    "Cave of No Return Progressive Key": (BASE_ITEM_OFFSET+52, 3), # need 3
    "Hyrule Castle Inner Wall Key": (BASE_ITEM_OFFSET+53, 1),
    "Village of the Blue Maiden Village Entrance Moon Gate": (BASE_ITEM_OFFSET+54, 1),
    "Village of the Blue Maiden Village East Moon Gate": (BASE_ITEM_OFFSET+55, 1),
    "Village of the Blue Maiden Village North Moon Gate": (BASE_ITEM_OFFSET+56, 1),
    "Village of the Blue Maiden Village West Moon Gate": (BASE_ITEM_OFFSET+57, 1),
    "Village of the Blue Maiden Book": (BASE_ITEM_OFFSET+58, 1),
    "Village of the Blue Maiden Letter": (BASE_ITEM_OFFSET+59, 1), # junk
    "Eastern Temple Entrance Key": (BASE_ITEM_OFFSET+60, 1),
    "Eastern Temple North East Moon Gate": (BASE_ITEM_OFFSET+61, 1), # junk
    "Eastern Temple South East Key": (BASE_ITEM_OFFSET+62, 1),
    "Eastern Temple South West Key": (BASE_ITEM_OFFSET+63, 1),
    "Eastern Temple South West Moon Gate": (BASE_ITEM_OFFSET+64, 1), # junk, skip damage boost
    #"Eastern Temple Big Key": (BASE_ITEM_OFFSET+65, 1),
    "The Mountain Path Water Storage Key": (BASE_ITEM_OFFSET+66, 1),
    "Tower of Flames 4F Key": (BASE_ITEM_OFFSET+67, 1),
    "The Field Storeroom Key": (BASE_ITEM_OFFSET+68, 1), # junk
    "The Field Stange Cave Key": (BASE_ITEM_OFFSET+69, 1), # junk
    "The Swamp Moon Gate": (BASE_ITEM_OFFSET+70, 1),
    "The Swamp Progressive Graveyard East Key": (BASE_ITEM_OFFSET+71, 2), # need 2
    "Infiltration of Hyrule Castle Lower Jail Key": (BASE_ITEM_OFFSET+72, 1), # junk, shortcut
    "Infiltration of Hyrule Castle Basement Stairs Moon Gate": (BASE_ITEM_OFFSET+73, 1),
    "Infiltration of Hyrule Castle Progressive Basement Key": (BASE_ITEM_OFFSET+74, 3), # need 3, 3rd is junk
    "Lost Woods East Woods Moon Gate": (BASE_ITEM_OFFSET+75, 1),
    "Lost Woods North Woods Storage Key": (BASE_ITEM_OFFSET+76, 1), # junk
    "Lost Woods South Woods Storage Key": (BASE_ITEM_OFFSET+77, 1), # junk
    "Kakariko Village South East House Key": (BASE_ITEM_OFFSET+78, 1),
    "Temple of Darkness Progressive Key": (BASE_ITEM_OFFSET+79, 5), # need 5
    "Temple of Darkness Secret Room Moon Gate": (BASE_ITEM_OFFSET+80, 1), # junk
    "Desert of Doubt Gerudo Town North East Moon Gate": (BASE_ITEM_OFFSET+81, 1),
    "Desert Temple Progressive Key": (BASE_ITEM_OFFSET+82, 3), # need 3
    "Desert Temple Laser Room Moon Gate": (BASE_ITEM_OFFSET+83, 1),
    "Pyramid South Corridor Key": (BASE_ITEM_OFFSET+84, 1),
    "Pyramid South East Key": (BASE_ITEM_OFFSET+85, 1),
    "Pyramid South East Moon Gate": (BASE_ITEM_OFFSET+86, 1), # junk
    "Pyramid Center Moon Gate": (BASE_ITEM_OFFSET+87, 1),
    #"Pyramid Big Key": (BASE_ITEM_OFFSET+88, 1),
    "Frozen Hyrule House Key": (BASE_ITEM_OFFSET+89, 1),
    "Frozen Hyrule House West Moon Gate": (BASE_ITEM_OFFSET+90, 1),
    "The Ice Temple Progressive Key": (BASE_ITEM_OFFSET+91, 4), # need 4
    "Tower of Winds Progressive Key": (BASE_ITEM_OFFSET+92, 2), # need 2
    "Realm of the Heavens South West Side Moon Gate": (BASE_ITEM_OFFSET+93, 1), # junk
    "Realm of the Heavens East Side Key": (BASE_ITEM_OFFSET+94, 1),
    "The Dark Cloud 3D Moon Gate": (BASE_ITEM_OFFSET+95, 1), # junk
    #"The Dark Cloud Big Key": (BASE_ITEM_OFFSET+96, 1),
    "The Dark Cloud Merge Left Moon Gate": (BASE_ITEM_OFFSET+97, 1), # junk, shortcut
    "Palace of Winds Progressive Moon Gate": (BASE_ITEM_OFFSET+98, 4), # need 4
    "Palace of Winds 2F East Key": (BASE_ITEM_OFFSET+99, 1),
    "Palace of Winds Progressive 2F North Key": (BASE_ITEM_OFFSET+100, 2), # need 2, 2nd is not required
}

REGULAR_PROGRESSION_ITEMS: dict[str, tuple[int, int]] = {
    **KEY_ITEMS,
    **IMPORTANT_ITEMS,
    **LEVEL_PROGRESSION_ITEMS,
    **JEWEL_ITEMS,
    **SAGE_ITEMS,
}

ALL_PROGRESSION_ITEMS: dict[str, tuple[int, int]] = {
    #"Progressive Link": (BASE_ITEM_OFFSET+101, 3),
    **REGULAR_PROGRESSION_ITEMS,
    #**FORMATION_ITEMS,
    **TICKET_ITEMS,
}

ALL_ITEMS_TABLE: dict[str, tuple[int, int]] = {
    **ALL_PROGRESSION_ITEMS,
    **JUNK_ITEMS,
    **TRAP_ITEMS,
}
