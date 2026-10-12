"""
Archipelago init file for The Legend of Zelda: Four Swords Adventures
"""
import random
from typing import Dict, Any
import os

from BaseClasses import ItemClassification
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, components, launch_subprocess
from .items import ALL_ITEMS_TABLE, REGULAR_PROGRESSION_ITEMS, LEVEL_PROGRESSION_ITEMS, ALL_PROGRESSION_ITEMS, KEY_ITEMS, TICKET_ITEMS, JUNK_ITEMS, TRAP_ITEMS, ZfsaItem
from .locations import ALL_LOCATIONS_TABLE
from .options import ZfsaOptions
from .regions import create_regions


class ZfsaWebWorld(WebWorld):
    theme = "grass"


class ZfsaWorld(World):
    """
    The Legend of Zelda: Four Swords Adventures follows Link as he splits into four colored copies of himself
    to rescue Princess Zelda and the Shrine Maidens from the wind mage Vaati and the true mastermind, Ganon.
    """
    game = "The Legend of Zelda: Four Swords Adventures"
    web = ZfsaWebWorld()

    data_version = 2

    options_dataclass = ZfsaOptions
    options: ZfsaOptions

    item_name_to_id = {
        name: data[0]
        for name, data in ALL_ITEMS_TABLE.items()
    }
    location_name_to_id = ALL_LOCATIONS_TABLE
    
    glitches_item_name = "Universal Tracker Glitched Logic"

    def generate_early(self):
        temp = False

    def create_regions(self):
        create_regions(self)

    def create_items(self):
        pool = []
        for name in REGULAR_PROGRESSION_ITEMS.keys():
            item_id, item_amount = REGULAR_PROGRESSION_ITEMS[name]
            for i in range(0, item_amount):
                pool.append(self.create_item(name))

        if self.options.level_access == 1:
            for name in TICKET_ITEMS.keys():
                item_id, item_amount = TICKET_ITEMS[name]
                for i in range(0, item_amount):
                    pool.append(self.create_item(name))

        for i in range(0, 32 - self.options.starting_health - 1):
            pool.append(self.create_item("Heart Piece"))
        
        pool_spots_left = len(ALL_LOCATIONS_TABLE) - len(pool)
        for i in range(0, int(pool_spots_left*.1)):
            pool.append(self.create_item(random.choice(list(TRAP_ITEMS))))

        while len(pool) < len(ALL_LOCATIONS_TABLE):
            pool.append(self.create_item(random.choice(list(JUNK_ITEMS))))

        self.multiworld.itempool += pool

    def create_item(self, name: str):
        if name == self.glitches_item_name:
            return ZfsaItem(name, ItemClassification.progression, None, self.player)
        
        if name in ALL_PROGRESSION_ITEMS:
            classification = ItemClassification.progression
        elif name in TRAP_ITEMS:
            classification = ItemClassification.trap
        else:
            classification = ItemClassification.filler

        item_id, item_amount = ALL_ITEMS_TABLE[name]
        return ZfsaItem(name, classification, item_id, self.player)

    def set_rules(self):
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def fill_slot_data(self) -> Dict[str, Any]:
        return {"ticket_mode": self.options.level_access.value,
                "shuffle_stages": self.options.shuffle_stages.value,
                "starting_health": self.options.starting_health.value,
                "death_link": self.options.death_link.value}


def launch_client():
    from .ZFSAClient import main
    launch_subprocess(main, name="ZFSA client")


def add_client_to_launcher() -> None:
    version = "0.0.4"
    found = False
    for c in components:
        if c.display_name == "Zelda Four Swords Adventures Client":
            found = True
            if getattr(c, "version", 0) < version:
                c.version = version
                c.func = launch_client
                return
    if not found:
        components.append(Component("Zelda Four Swords Adventures Client", "ZFSAClient", func=launch_client))


add_client_to_launcher()
