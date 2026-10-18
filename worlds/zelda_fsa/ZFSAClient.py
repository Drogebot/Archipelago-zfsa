from __future__ import annotations

import asyncio
import collections
import time
import traceback
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass

import ModuleUpdate
from .options import ZfsaOptions
from .bit_helper import change_endian, bit_flagger, extract_bits
import dolphin_memory_engine as dme
from . import addresses, WORLD_VERSION
from .static_logic import ALL_REGIONS, DoorType
from .items import ALL_ITEMS_TABLE

ModuleUpdate.update()

import Utils

''' "Comment-Dictionary"
    #Gravi01    Preventing Crash when game is closed/disconnected before Client + Allowing client to reconnect

'''


from NetUtils import ClientStatus
from CommonClient import gui_enabled, logger, get_base_parser, ClientCommandProcessor, CommonContext, server_loop

CONNECTION_REFUSED_GAME_STATUS = (
    "Dolphin failed to connect. Please load a randomized ROM for The Legend of Zelda: Four Swords Adventures. Trying again in 5 seconds..."
)
CONNECTION_REFUSED_SAVE_STATUS = (
    "Dolphin failed to connect. Please load into the save file. Trying again in 5 seconds..."
)
CONNECTION_LOST_STATUS = (
    "Dolphin connection was lost. Please restart your emulator and make sure The Legend of Zelda: Four Swords Adventures is running."
)
CONNECTION_CONNECTED_STATUS = "Dolphin connected successfully."
CONNECTION_INITIAL_STATUS = "Dolphin connection has not been initiated."

debug = False

#game_ver = 0x3a

BASE_ITEM_OFFSET = 379000

@dataclass
class KeyItem:
    item_name: str
    ap_item_id: int
    item_lvl: int = 0
    active: bool = False


KEYITEMS: list[KeyItem] = [
    KeyItem("None", 0, 0, True),
    KeyItem("Pegasus Boots", BASE_ITEM_OFFSET+0),
    KeyItem("Lamp", BASE_ITEM_OFFSET+1),
    KeyItem("Boomerang", BASE_ITEM_OFFSET+2),
    KeyItem("Bow", BASE_ITEM_OFFSET+3),
    KeyItem("Magic Hammer", BASE_ITEM_OFFSET+4),
    KeyItem("Fire Rod", BASE_ITEM_OFFSET+5),
    KeyItem("Roc's Feather", BASE_ITEM_OFFSET+6),
    KeyItem("Bombs", BASE_ITEM_OFFSET+7),
    KeyItem("Shovel", BASE_ITEM_OFFSET+8),
    KeyItem("Slingshot", BASE_ITEM_OFFSET+9),
]


class ZfsaCommandProcessor(ClientCommandProcessor):
    def _cmd_connect(self, address: str = "") -> bool:
        if isinstance(self.ctx, ZfsaContext):
            logger.info(f"Dolphin Status: {self.ctx.dolphin_status}")

    def _cmd_resync(self):
        """Manually trigger a resync."""
        self.output(f"Syncing items.")
        self.ctx.syncing = True
        refresh_collection_counts(self.ctx)


class ZfsaContext(CommonContext):
    command_processor: ZfsaCommandProcessor
    game = "The Legend of Zelda: Four Swords Adventures"
    items_handling = 0b111  # full remote

    options: ZfsaOptions

    ap_connected = False
    hook_check = False
    hook_nagged = False

    believe_hooked = False

    lives_given = 0
    lives_switch = False

    ticket_mode = False
    shuffle_stages = False
    has_blue_bracelet = False
    has_power_bracelet = False
    jewels = 0
    maidens = 0
    gemtotal = 0
    starting_health = 16
    current_health = 16
    current_level = 0
    current_screen = 0
    current_layer = 0
    reset_doors = False
    victory = False
    
    deathlink_enabled = False
    deathlink_pending = False
    deathlink_sent_this_death = False
    deathlink_killed_player = False
    
    is_first_item_sync = True
    known_items_loaded = False
    save_known_items = False
    known_items = {}
    received_hearts = 0
    received_fairies = 0
    remaining_fairies = 0
    fairy_storage_loaded = False
    fairy_storage_applied = False
    save_fairies = False
    received_tingle_traps = 0
    received_fire_traps = 0
    queued_messages = []

    ap_keyitems_received = []

    def __init__(self, server_address, password):
        super(ZfsaContext, self).__init__(server_address, password)
        self.send_index: int = 0
        self.syncing = False
        self.awaiting_bridge = False
        self.dolphin_sync_task: Optional[asyncio.Task[None]] = None
        self.dolphin_status: str = CONNECTION_INITIAL_STATUS
        self.awaiting_rom: bool = False

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(ZfsaContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    @property
    def endpoints(self):
        if self.server:
            return [self.server]
        else:
            return []

    def run_gui(self):
        """Import kivy UI system and start running it as self.ui_task."""
        from kvui import GameManager

        class ZfsaManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago Zelda Four Swords Adventures Client"

        self.ui = ZfsaManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            slot_data = args.get("slot_data")
            temp = slot_data.get("ticket_mode")
            if temp:
                self.ticket_mode = temp == 1
            temp = slot_data.get("shuffle_stages")
            if temp:
                self.shuffle_stages = temp
            temp = slot_data.get("starting_health")
            if temp:
                self.starting_health = temp
                self.current_health = temp
            temp = slot_data.get("death_link")
            if temp:
                asyncio.create_task(self.update_death_link(True))
                self.deathlink_enabled = temp
            
            self.set_notify(get_known_items_storage_key(self))
            self.set_notify(get_fairy_storage_key_received(self))
            self.set_notify(get_fairy_storage_key_remaining(self))
            
            self.ap_connected = True
    
    def on_deathlink(self, data: dict):
        super().on_deathlink(data)
        if self.deathlink_enabled:
            self.deathlink_pending = True


async def game_watcher(ctx: ZfsaContext):
    while not ctx.exit_event.is_set():

        sync_msg = [{'cmd': 'Sync'}]
        if ctx.locations_checked:
            sync_msg.append({"cmd": "LocationChecks", "locations": list(ctx.locations_checked)})
        await ctx.send_msgs(sync_msg)
        
        #data storage
        known_items_key = get_known_items_storage_key(ctx)
        if known_items_key in ctx.stored_data and not ctx.known_items_loaded:
            ctx.known_items_loaded = True
            known_items = ctx.stored_data[known_items_key]
            #logger.info(known_items)
            if known_items != None:
                for item in known_items:
                    ctx.known_items[int(item)] = known_items[item]
                ctx.known_items = collections.Counter(ctx.known_items)
            logger.info(f"Loaded {sum(ctx.known_items.values())} items from Data Storage")
        if ctx.save_known_items:
            ctx.save_known_items = False
            await save_known_items(ctx)
            
        fairy_key_received = get_fairy_storage_key_received(ctx)
        fairy_key_remaining = get_fairy_storage_key_remaining(ctx)
        if fairy_key_received in ctx.stored_data and fairy_key_remaining in ctx.stored_data and not ctx.fairy_storage_loaded:
            ctx.fairy_storage_loaded = True
            received = ctx.stored_data[fairy_key_received]
            remaining = ctx.stored_data[fairy_key_remaining]
            if received != None and remaining != None:
                ctx.received_fairies = int(received)
                ctx.remaining_fairies = int(remaining)
            logger.info(f"Loaded {ctx.remaining_fairies} fairies from Data Storage")
        if ctx.fairy_storage_loaded and not ctx.fairy_storage_applied:
            ctx.fairy_storage_applied = set_fairy_amount(ctx.remaining_fairies, ctx)
        if ctx.save_fairies:
            ctx.save_fairies = False
            await save_fairy_count(ctx)
        
        #Gravi01 Begin      
        '''
        dme.is_hooked() returns true if just the emulation stops, as dolphin itself is still running
        this causes the dme to write into a non existing memory, resulting in the crashes.
        changed if to check based on connection status, and unhooking DME properly if connection is lost (Exception)
        ''' 
        if ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
            try:
                refresh_all_items(ctx)
            except Exception:
                import traceback
                logger.info(traceback.format_exc())
                logger.info("Connection to Dolphin lost, reconnecting...")
                ctx.dolphin_status = CONNECTION_LOST_STATUS
                dme.un_hook()
        ctx.lives_switch = True
        #Gravi01 End

        if ctx.victory and not ctx.finished_game:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True

        await asyncio.sleep(0.2)
        ctx.lives_switch = False

async def dolphin_sync_task(ctx: ZfsaContext) -> None:
    logger.info("Starting Dolphin connector. Use /dolphin for status information.")
    while not ctx.exit_event.is_set():
        try:
            if dme.is_hooked() and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                # if ctx.slot is not None:
                #     # await give_items(ctx)
                #     # await check_locations(ctx)
                #     # await check_current_stage_changed(ctx)
                #     # self._cmd_resync()
                # else:
                if ctx.awaiting_rom:
                    await ctx.server_auth()
                await asyncio.sleep(0.1)
            else:   
                if ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                    logger.info("Connection to Dolphin lost, reconnecting...")
                    ctx.dolphin_status = CONNECTION_LOST_STATUS
                logger.info("Attempting to connect to Dolphin...")
                dme.hook()
                if dme.is_hooked():
                    if dme.read_bytes(0x80000000, 6) != b"G4SE01":
                        logger.info(CONNECTION_REFUSED_GAME_STATUS)
                        ctx.dolphin_status = CONNECTION_REFUSED_GAME_STATUS
                        dme.un_hook()
                        await asyncio.sleep(5)
                    else:
                        logger.info(CONNECTION_CONNECTED_STATUS)
                        ctx.dolphin_status = CONNECTION_CONNECTED_STATUS
                        ctx.locations_checked = set()
                else:
                    logger.info("Connection to Dolphin failed, attempting again in 5 seconds...")
                    dme_status = dme.get_status()
                    ctx.dolphin_status = CONNECTION_LOST_STATUS
                    await ctx.disconnect()
                    await asyncio.sleep(5)
                    continue
        except Exception:
            dme.un_hook()
            logger.info("Connection to Dolphin failed, attempting again in 5 seconds...")
            logger.error(traceback.format_exc())
            ctx.dolphin_status = CONNECTION_LOST_STATUS
            await ctx.disconnect()
            await asyncio.sleep(5)
            continue


def send_victory(ctx: ZfsaContext):
    if ctx.victory:
        return

    ctx.victory = True
    ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
    time.sleep(1)
    logger.info("Congratulations on completing your seed!")
    time.sleep(.05)
    logger.info("ARCHIPELAGO THE LEGEND OF ZELDA: FOUR SWORDS ADVENTURES CREDITS:")
    time.sleep(.05)
    logger.info("Drogings - APWorld, Client, Patching and Logic")
    time.sleep(.05)
    logger.info("Pink Switch - Patching")
    time.sleep(.05)
    logger.info("Jaybear - Testing")
    time.sleep(.05)
    logger.info("StealMyUserName - Testing")
    #time.sleep(.05)
    #logger.info("placeholder - Additional research")
    time.sleep(.05)
    logger.info("Venomalia - EFSAdvent, FSALib")
    time.sleep(.05)
    logger.info("EverydaySimpleDev - Standalone Randomizer")
    time.sleep(.05)
    logger.info("Super Mario Sunshine AP Team")
    time.sleep(.05)
    logger.info("All Archipelago core devs")
    time.sleep(.05)
    logger.info("Nintendo EAD")
    time.sleep(.05)
    logger.info("...and you. Thanks for playing!")
    return


def get_known_items_storage_key(ctx: ZfsaContext):
    return f"zfsa_known_items_{ctx.team}_{ctx.slot}"
def get_fairy_storage_key_received(ctx: ZfsaContext):
    return f"zfsa_fairies_{ctx.team}_{ctx.slot}_received"
def get_fairy_storage_key_remaining(ctx: ZfsaContext):
    return f"zfsa_fairies_{ctx.team}_{ctx.slot}_remaining"


async def save_known_items(ctx: ZfsaContext):
    if not ctx.known_items_loaded: return
    await ctx.send_msgs([{
        "cmd": "Set",
        "key": get_known_items_storage_key(ctx),
        "default": {},
        "want_reply": False,
        "operations": [
            {
                "operation": "update",
                "value": ctx.known_items,
            }
        ],
    }])
    #logger.info(ctx.known_items)
    #logger.info(f"Saved known items to Data Storage")


async def save_fairy_count(ctx: ZfsaContext):
    if not ctx.fairy_storage_loaded: return
    await ctx.send_msgs([{
        "cmd": "Set",
        "key": get_fairy_storage_key_received(ctx),
        "default": 0,
        "want_reply": False,
        "operations": [
            {
                "operation": "replace",
                "value": ctx.received_fairies,
            }
        ],
    }])
    await ctx.send_msgs([{
        "cmd": "Set",
        "key": get_fairy_storage_key_remaining(ctx),
        "default": 0,
        "want_reply": False,
        "operations": [
            {
                "operation": "replace",
                "value": ctx.remaining_fairies,
            }
        ],
    }])
    #logger.info(f"Saved {ctx.remaining_fairies} fairies to Data Storage")


def refresh_all_items(ctx: ZfsaContext):
    if not ctx.known_items_loaded:
        return
    
    has_new_items = False
    counts = collections.Counter(received_item.item for received_item in ctx.items_received)
    gemtotal = 0
    for item in counts:
        amt = counts[item]
        
        if item not in ctx.known_items:
            has_new_items = True
            if ctx.is_first_item_sync:
                continue
        
        if ctx.known_items[item] != amt:
            has_new_items = True
            if ctx.is_first_item_sync:
                amt = ctx.known_items[item]
        
        if amt > 0:
            unpack_item(item, ctx, amt)
            
            if BASE_ITEM_OFFSET+31 <= item <= BASE_ITEM_OFFSET+42:
                gemvalues = [1, 5, 20, 50, 100, 150, 200, 300, 1000, 1500, 2000, 3000]
                gemtotal += amt*gemvalues[item - (BASE_ITEM_OFFSET+31)]
    
    gemtotal = int(gemtotal/100)
    gemtotal -= ctx.received_tingle_traps*20
    if gemtotal < 0: gemtotal = 0
    if gemtotal != ctx.gemtotal:
        activate_gems(gemtotal - ctx.gemtotal, ctx)
    
    if not ctx.is_first_item_sync:
        ctx.known_items = counts
        if has_new_items:
            ctx.save_known_items = True
    
    if ctx.ap_connected and ctx.is_first_item_sync:
        ctx.is_first_item_sync = False
        for loc_id in ctx.checked_locations:
            if loc_id in LOCMAP_BY_LOCATIONID:
                LOCMAP_BY_LOCATIONID[loc_id].checked = True
            else:
                for loc in STAGEMAP.values():
                    if loc_id == loc.location_id:
                        loc.checked = True


def unpack_item(item, ctx, amt=0):
    if BASE_ITEM_OFFSET <= item <= BASE_ITEM_OFFSET+9:
        activate_item(item, amt, ctx)
    elif item == BASE_ITEM_OFFSET+10:
        activate_blue_bracelet(ctx)
    elif item == BASE_ITEM_OFFSET+11:
        activate_power_bracelet(ctx)
    elif item == BASE_ITEM_OFFSET+12:
        activate_heart_piece(amt, ctx)
    elif BASE_ITEM_OFFSET+13 <= item <= BASE_ITEM_OFFSET+20:
        activate_ticket(item, amt, ctx)
    elif BASE_ITEM_OFFSET+21 <= item <= BASE_ITEM_OFFSET+24:
        activate_jewel(item - (BASE_ITEM_OFFSET+21), ctx)
    elif item == BASE_ITEM_OFFSET+25:
        activate_maiden(amt, ctx)
    elif item == BASE_ITEM_OFFSET+46:
        activate_heart(amt, ctx)
    elif item == BASE_ITEM_OFFSET+47:
        activate_fairy(amt, ctx)
    elif item == BASE_ITEM_OFFSET+48:
        activate_tingle_trap(amt, ctx)
    elif item == BASE_ITEM_OFFSET+49:
        activate_fire_trap(amt, ctx)
    elif BASE_ITEM_OFFSET+51 <= item <= BASE_ITEM_OFFSET+100:
        activate_door(item, amt, ctx)


@dataclass
class Ticket:
    item_name: str
    ap_item_id: int
    bit_position: int
    course_id: int
    active: bool = False


TICKETS: list[Ticket] = [
    Ticket("Level 1-2 Ticket", BASE_ITEM_OFFSET+13, 1, 1),
    Ticket("Level 1-3 Ticket", BASE_ITEM_OFFSET+13, 2, 2),
    Ticket("Level 2-2 Ticket", BASE_ITEM_OFFSET+14, 5, 1),
    Ticket("Level 2-3 Ticket", BASE_ITEM_OFFSET+14, 6, 2),
    Ticket("Level 3-2 Ticket", BASE_ITEM_OFFSET+15, 9, 1),
    Ticket("Level 3-3 Ticket", BASE_ITEM_OFFSET+15, 10, 2),
    Ticket("Level 4-2 Ticket", BASE_ITEM_OFFSET+16, 13, 1),
    Ticket("Level 4-3 Ticket", BASE_ITEM_OFFSET+16, 14, 2),
    Ticket("Level 5-2 Ticket", BASE_ITEM_OFFSET+17, 17, 1),
    Ticket("Level 5-3 Ticket", BASE_ITEM_OFFSET+17, 18, 2),
    Ticket("Level 6-2 Ticket", BASE_ITEM_OFFSET+18, 21, 1),
    Ticket("Level 6-3 Ticket", BASE_ITEM_OFFSET+18, 22, 2),
    Ticket("Level 7-2 Ticket", BASE_ITEM_OFFSET+19, 25, 1),
    Ticket("Level 7-3 Ticket", BASE_ITEM_OFFSET+19, 26, 2),
    Ticket("Level 8-2 Ticket", BASE_ITEM_OFFSET+20, 29, 1),
    Ticket("Level 8-3 Ticket", BASE_ITEM_OFFSET+20, 30, 2),
]


def activate_ticket(id: int, amt: int, ctx):
    for ticket in TICKETS:
        if id == ticket.ap_item_id and amt >= ticket.course_id and not ticket.active:
            ticket.active = True
            show_message(f"Received {ticket.item_name}", ctx)
            return


def activate_item(id, amt, ctx):
    for item in KEYITEMS:
        if id == item.ap_item_id:
            if item.item_lvl >= amt: return
            item.active = True
            item.item_lvl = amt
            show_message(f"Received {item.item_name}{(f" L{amt}"if amt > 1 else "")}", ctx)
            return


def activate_blue_bracelet(ctx):
    if ctx.has_blue_bracelet: return
    ctx.has_blue_bracelet = True
    show_message("Received Blue Bracelet", ctx)


def activate_power_bracelet(ctx):
    if ctx.has_power_bracelet: return
    ctx.has_power_bracelet = True
    show_message("Received Power Bracelet", ctx)


def activate_heart_piece(amt, ctx):
    if ctx.current_health >= ctx.starting_health + amt: return
    ctx.current_health = ctx.starting_health + amt
    show_message("Received Heart Piece", ctx)


def activate_jewel(id, ctx):
    if ctx.jewels & (1 << id) > 0: return
    ctx.jewels |= 1 << id
    jewels = ["Blue", "Green", "Purple", "Red"]
    show_message(f"Received {jewels[id]} Royal Jewel", ctx)


def activate_maiden(amt, ctx):
    for i in range(0, amt):
        if ctx.maidens & (1 << i) > 0: continue
        ctx.maidens |= 1 << i
        maidens = ["Blue Maiden", "Yellow Maiden", "Green Maiden", "White Maiden", "Red Maiden", "Purple Maiden", "Princess Zelda"]
        show_message(f"Received {maidens[i]}", ctx)


def activate_door(id, amt, ctx):
    for i in range(0, amt):
        door = DOORMAP_BY_ITEMID[id][i]
        if door.opened: continue
        door.opened = True
        ctx.reset_doors = True
        show_message(f"Received {door.key_name}", ctx)


def activate_gems(amt, ctx):
    ctx.gemtotal += amt
    if ctx.is_first_item_sync: return
    if ctx.dolphin_status == CONNECTION_CONNECTED_STATUS: #Gravi01  change to connection status
        show_message(f"Received {amt} Force Gems", ctx)
        
        link_arr_adr = dme.read_word(addresses.ZFSA_LINK_ARR_PTR)
        if link_arr_adr > 0:
            link_adr = dme.read_word(link_arr_adr + addresses.ZFSA_LINK_ARR_OFFSET)
            if link_adr > 0:
                gems = dme.read_word(link_adr + addresses.ZFSA_LINK_GEMS_OFFSET)
                dme.write_word(link_adr + addresses.ZFSA_LINK_GEMS_OFFSET, gems + amt)


def activate_heart(amt, ctx):
    if ctx.dolphin_status == CONNECTION_CONNECTED_STATUS: #Gravi01  change to connection status
        if ctx.received_hearts >= amt: return
        ctx.received_hearts = amt
        show_message(f"Received Heart", ctx)
        
        link_arr_adr = dme.read_word(addresses.ZFSA_LINK_ARR_PTR)
        if link_arr_adr > 0:
            link_adr = dme.read_word(link_arr_adr + addresses.ZFSA_LINK_ARR_OFFSET)
            if link_adr > 0:
                health = dme.read_word(link_adr + addresses.ZFSA_LINK_HEALTH_OFFSET)
                maxhealth = dme.read_word(link_adr + addresses.ZFSA_LINK_HEALTHMAX_OFFSET)
                health += 4
                if health > maxhealth: health = maxhealth
                dme.write_word(link_adr + addresses.ZFSA_LINK_HEALTH_OFFSET, health)


def activate_fairy(amt, ctx):
    if not ctx.fairy_storage_loaded: return
    if ctx.dolphin_status == CONNECTION_CONNECTED_STATUS: #Gravi01  change to connection status
        if ctx.received_fairies >= amt: return
        new_fairies = amt - ctx.received_fairies
        ctx.received_fairies = amt
        ctx.remaining_fairies += new_fairies
        ctx.save_fairies = True
        show_message(f"Received Force Fairy", ctx)
        
        fairies = (dme.read_word(addresses.ZFSA_LEVEL_FAIRIES) + new_fairies) & 0b111111
        dme.write_word(addresses.ZFSA_LEVEL_FAIRIES, fairies)
        dme.write_byte(addresses.ZFSA_SAVE_FAIRIES, fairies)


def set_fairy_amount(fairies, ctx):
    if ctx.dolphin_status == CONNECTION_CONNECTED_STATUS: #Gravi01  change to connection status
        game_state = dme.read_word(addresses.ZFSA_GAME_STATE)
        if game_state < 6: return False
        fairies = fairies & 0b111111
        dme.write_word(addresses.ZFSA_LEVEL_FAIRIES, fairies)
        dme.write_byte(addresses.ZFSA_SAVE_FAIRIES, fairies)
        return True
    return False


def activate_tingle_trap(amt, ctx):
    if ctx.received_tingle_traps >= amt: return
    new_tingles = amt - ctx.received_tingle_traps
    ctx.received_tingle_traps = amt
    show_message(f"Received Tingle Trap\nTingle stole {new_tingles*20} Force Gems!", ctx)


def activate_fire_trap(amt, ctx):
    if ctx.is_first_item_sync:
        ctx.received_fire_traps = amt
        return
    if ctx.dolphin_status == CONNECTION_CONNECTED_STATUS: #Gravi01  change to connection status
        if ctx.received_fire_traps >= amt: return
        ctx.received_fire_traps = amt
        show_message(f"Received Fire Trap", ctx)
        
        link_arr_adr = dme.read_word(addresses.ZFSA_LINK_ARR_PTR)
        if link_arr_adr > 0:
            link_adr = dme.read_word(link_arr_adr + addresses.ZFSA_LINK_ARR_OFFSET)
            if link_adr > 0:
                dme.write_word(link_adr + addresses.ZFSA_LINK_FIRE_TIMER_OFFSET, 0)
                dme.write_word(link_adr + addresses.ZFSA_LINK_FIRE_OFFSET2, 80)
                dme.write_word(link_adr + addresses.ZFSA_LINK_FIRE_OFFSET1, 80)


def show_message(message, ctx):
    if ctx.is_first_item_sync:
        return
    ctx.queued_messages.append(message)

# Checks to see if player changed stages to update map_id for Poptracker
async def send_map_id(map_id, screen_id, layer_id, ctx):
    if map_id == ctx.current_level and screen_id == ctx.current_screen and layer_id == ctx.current_layer:
        return
    ctx.current_level = map_id
    ctx.current_screen = screen_id
    ctx.current_layer = layer_id
    await ctx.send_msgs([{
        "cmd": "Set",
        "key": f"zfsa_map_{ctx.team}_{ctx.slot}",
        "default": 0,
        "want_reply": False,
        "operations": [{"operation": "replace", "value": f"{map_id}:{screen_id}:{layer_id}"}]
    }])


@dataclass
class LocationInfo:
    location_id: int
    flagId: "LocationFlag"
    type: DoorType
    checked: bool = False


@dataclass
class DoorInfo:
    key_name: str
    item_id: int
    item_number: int
    stageId: int
    type: DoorType
    flagId: "LocationFlag"
    opened: bool = False


STAGEMAP: dict[int, LocationInfo] = {}
LOCMAP_BY_LOCATIONID: dict[int, LocationInfo] = {}
LOCMAP: dict[int, list[LocationInfo]] = {}
DOORMAP_BY_ITEMID: dict[int, list[DoorInfo]] = {}
DOORMAP: dict[int, list[DoorInfo]] = {}
def create_location_memory_map():
    for region_name in ALL_REGIONS:
        region = ALL_REGIONS[region_name]
        STAGEMAP[region.stageId] = LocationInfo(region.id, None, DoorType.unknown)
        LOCMAP[region.stageId] = []
        for chest in region.chests:
            loc = LocationInfo(chest.id, chest.flagId, DoorType.big_chest)
            LOCMAP_BY_LOCATIONID[chest.id] = loc
            LOCMAP[region.stageId].append(loc)
        if region.jewel is not None:
            loc = LocationInfo(region.jewel.id, region.jewel.flagId, DoorType.local_variable)
            LOCMAP_BY_LOCATIONID[region.jewel.id] = loc
            LOCMAP[region.stageId].append(loc)
        DOORMAP[region.stageId] = []
        for door in region.doors:
            (item_id, _) = ALL_ITEMS_TABLE[door.key]
            door = DoorInfo(door.key, item_id, door.number, region.stageId, door.type, door.flagId)
            if not item_id in DOORMAP_BY_ITEMID: DOORMAP_BY_ITEMID[item_id] = []
            DOORMAP_BY_ITEMID[item_id].append(door)
            DOORMAP[region.stageId].append(door)


async def handle_stage_select(ctx):
    was_in_menu = False
    while not ctx.exit_event.is_set():
        if ctx.dolphin_status == CONNECTION_CONNECTED_STATUS: #Gravi01  change to connection status
            game_state = dme.read_word(addresses.ZFSA_GAME_STATE)
            menu_adr = dme.read_word(addresses.ZFSA_MENU_PTR)
            
            #skip intro
            if game_state == 4:
                dme.write_byte(addresses.ZFSA_SAVE_INTRO_SKIP, 3)
            
            #stages beaten
            if game_state >= 4:
                stage_flags = dme.read_word(addresses.ZFSA_SAVE_STAGES)
                for i in range(0, 32):
                    levelId = (i >> 2)+1
                    stageId = i & 0b11
                    if stageId == 2 and levelId != 8 or stageId == 1 and levelId == 8: continue
                    stageId = levelId*10 + stageId
                    beaten = (stage_flags & (1 << i)) > 0
                    loc = STAGEMAP[stageId]
                    if beaten and not loc.checked:
                        if stageId == 83: send_victory(ctx)
                        loc.checked = True
                        ctx.locations_checked.add(loc.location_id)
                        if not ctx.ticket_mode:
                            ticket_id = (i >> 2)*2 + (1 if (i & 0b11) > 0 else 0)
                            TICKETS[ticket_id].active = True
                    elif not beaten and loc.checked:
                        stage_flags |= 1 << i
                        dme.write_word(addresses.ZFSA_SAVE_STAGES, stage_flags)
                        if not ctx.ticket_mode:
                            ticket_id = (i >> 2)*2 + (1 if (i & 0b11) > 0 else 0)
                            TICKETS[ticket_id].active = True
            
            #fairy sync
            if game_state < 6:
                ctx.fairy_storage_applied = False
            else:
                save_fairies = dme.read_byte(addresses.ZFSA_SAVE_FAIRIES)
                level_fairies = dme.read_word(addresses.ZFSA_LEVEL_FAIRIES)
                if level_fairies != save_fairies:
                    dme.write_byte(addresses.ZFSA_SAVE_FAIRIES, level_fairies)
                    ctx.remaining_fairies = level_fairies
                    ctx.save_fairies = True
            
            if game_state != 6 or menu_adr == 0:
                was_in_menu = False
            else:
                #stage select
                #dme.write_word(menu_adr + addresses.ZFSA_MENU_MAX_WORLDID_OFFSET, 7 if ctx.jewels == 0b1111 else 6)
                stage_select_flags = 0b0001_0001_0001_0001_0001_0001_0001_0001
                for ticket in TICKETS:
                    if not ticket.active:
                        continue
                    if ticket.bit_position >= 28 and ctx.jewels != 0b1111:
                        continue
                    stage_select_flags |= 1 << ticket.bit_position
                dme.write_word(menu_adr + addresses.ZFSA_MENU_STAGE_SELECT_FLAGS_OFFSET, stage_select_flags)
                mapstate = dme.read_word(menu_adr + addresses.ZFSA_MENU_MAPSTATE_OFFSET)
                if not was_in_menu:
                    dme.write_word(menu_adr + addresses.ZFSA_MENU_MAPSTATE_OFFSET, 19)
                if mapstate == 21:
                    dme.write_word(menu_adr + addresses.ZFSA_MENU_MAPSTATE_OFFSET, 15)
                was_in_menu = True
            
        await asyncio.sleep(0.1)


async def handle_stage(ctx):
    prev_level = 0
    prev_screen = -1
    while not ctx.exit_event.is_set():
        if ctx.dolphin_status == CONNECTION_CONNECTED_STATUS: #Gravi01  change to connection status
            try:
                game_state = dme.read_word(addresses.ZFSA_GAME_STATE)
                stage_ptr_ptr_adr = dme.read_word(addresses.ZFSA_STAGE_PTR_PTR)
                if game_state < 7 or stage_ptr_ptr_adr == 0:
                    prev_level = 0
                    prev_screen = -1
                    await send_map_id(0, 0, 0, ctx)
                elif game_state == 7:
                    stage_ptr_adr = dme.read_word(stage_ptr_ptr_adr + addresses.ZFSA_STAGE_PTR_OFFSET)
                    if stage_ptr_adr > 0:
                        stage_adr = dme.read_word(stage_ptr_adr + addresses.ZFSA_STAGE_OFFSET)
                        if stage_adr > 0:
                            # poptracker
                            levelid = dme.read_word(stage_adr + addresses.ZFSA_STAGE_LEVELID_OFFSET)
                            stageid = dme.read_word(stage_adr + addresses.ZFSA_STAGE_STAGEID_OFFSET)
                            cur_screen = dme.read_word(stage_adr + addresses.ZFSA_STAGE_SCREEN_X_OFFSET) + dme.read_word(stage_adr + addresses.ZFSA_STAGE_SCREEN_Y_OFFSET)*10
                            cur_level = levelid*10 + 10 + stageid
                            await send_map_id(cur_level, cur_screen, ctx.current_layer, ctx)
                            
                            #jewels & maidens
                            dme.write_byte(stage_adr + addresses.ZFSA_STAGE_JEWELS_OFFSET, ctx.jewels)
                            dme.write_byte(stage_adr + addresses.ZFSA_STAGE_MAIDENS_OFFSET, ctx.maidens)
                            
                            #locations
                            if cur_level <= 83:
                                for loc in LOCMAP[cur_level]:
                                    if loc.type == DoorType.big_chest:
                                        chest = loc
                                        offset = chest.flagId.roomy*10*8*8 + chest.flagId.roomx*8*8 + chest.flagId.layer*8 + 4 - 4*(chest.flagId.index >> 5)
                                        bit = chest.flagId.index & 0b11111
                                        val = dme.read_word(stage_adr + addresses.ZFSA_STAGE_TILE_FLAGS_OFFSET + offset)
                                        if chest.checked and (prev_level != cur_level or prev_screen != cur_screen):
                                            dme.write_word(stage_adr + addresses.ZFSA_STAGE_TILE_FLAGS_OFFSET + offset, val | (1 << bit))
                                        elif (val & (1 << bit)) > 0:
                                            chest.checked = True
                                            ctx.locations_checked.add(chest.location_id)
                                    elif loc.type == DoorType.local_variable:
                                        jewel = loc
                                        offset = jewel.flagId.roomy*10*4 + jewel.flagId.roomx*4
                                        bit = jewel.flagId.index & 0b11111
                                        val = dme.read_word(stage_adr + addresses.ZFSA_STAGE_VARIABLES_OFFSET + offset)
                                        if (val & (1 << bit)) > 0:
                                            jewel.checked = True
                                            ctx.locations_checked.add(jewel.location_id)
                                
                                #doors
                                if ctx.reset_doors or prev_level != cur_level or prev_screen != cur_screen:
                                    ctx.reset_doors = False
                                    for door in DOORMAP[cur_level]:
                                        if not door.opened: continue
                                        if door.type == DoorType.door:
                                            offset = door.flagId.roomy*10*8*8 + door.flagId.roomx*8*8 + door.flagId.layer*8 + 4 - 4*(door.flagId.index >> 5)
                                            bit = door.flagId.index & 0b11111
                                            val = dme.read_word(stage_adr + addresses.ZFSA_STAGE_TILE_FLAGS_OFFSET + offset)
                                            dme.write_word(stage_adr + addresses.ZFSA_STAGE_TILE_FLAGS_OFFSET + offset, val | (1 << bit))
                                        elif door.type == DoorType.moon_gate:
                                            offset = door.flagId.roomy*10*32*4 + door.flagId.roomx*32*4 + 4*(door.flagId.index >> 5)
                                            bit = door.flagId.index & 0b11111
                                            val = dme.read_word(stage_adr + addresses.ZFSA_STAGE_ACTOR_FLAGS_OFFSET + offset)
                                            dme.write_word(stage_adr + addresses.ZFSA_STAGE_ACTOR_FLAGS_OFFSET + offset, val | (1 << bit))
                                        elif door.type == DoorType.local_variable:
                                            offset = door.flagId.roomy*10*4 + door.flagId.roomx*4
                                            bit = door.flagId.index & 0b11111
                                            val = dme.read_word(stage_adr + addresses.ZFSA_STAGE_VARIABLES_OFFSET + offset)
                                            dme.write_word(stage_adr + addresses.ZFSA_STAGE_VARIABLES_OFFSET + offset, val | (1 << bit))
                            
                            prev_level = cur_level
                            prev_screen = cur_screen
                            
                            # message popups
                            message_box_adr = dme.read_word(addresses.ZFSA_MESSAGE_BOX_PTR)
                            box_state = dme.read_byte(message_box_adr + addresses.ZFSA_MESSAGE_BOX_STATE_OFFSET)
                            if len(ctx.queued_messages) > 0 and message_box_adr > 0 and box_state == 0:
                                message = ctx.queued_messages.pop(0)
                                text_ptr = dme.read_word(message_box_adr + addresses.ZFSA_MESSAGE_TEXT_PTR_OFFSET)
                                text_ptr = dme.read_word(text_ptr + 0x4)
                                back_ptr = dme.read_word(text_ptr + 0xDC)
                                front_ptr = dme.read_word(text_ptr + 0xE0)
                                dme.write_word(back_ptr + 0x3C, addresses.ZFSA_FREE_MEMORY_ADDR)
                                dme.write_word(front_ptr + 0x3C, addresses.ZFSA_FREE_MEMORY_ADDR)
                                dme.write_bytes(addresses.ZFSA_FREE_MEMORY_ADDR, message.encode() + b'\0')
                                #TODO: set box top or bottom depending on link screen height
                                dme.write_bytes(message_box_adr + addresses.ZFSA_MESSAGE_BOX_STATE_OFFSET, b"\1\1")
            except Exception:
                import traceback
                logger.info(traceback.format_exc())
            
        await asyncio.sleep(0.1)


async def handle_link(ctx):
    prev_game_state = 0
    controller_input_prev = 0
    while not ctx.exit_event.is_set():
        if ctx.dolphin_status == CONNECTION_CONNECTED_STATUS: #Gravi01  change to connection status
            try:
                game_state = dme.read_word(addresses.ZFSA_GAME_STATE)
                link_arr_adr = dme.read_word(addresses.ZFSA_LINK_ARR_PTR)
                if game_state == 7 and link_arr_adr > 0:
                    link_adr = dme.read_word(link_arr_adr + addresses.ZFSA_LINK_ARR_OFFSET)
                    if link_adr > 0:
                        #link state legal
                        if prev_game_state < 7 and prev_game_state != 0:
                            dme.write_word(link_adr + addresses.ZFSA_LINK_GEMS_OFFSET, ctx.gemtotal)
                        dme.write_byte(link_adr + addresses.ZFSA_LINK_POWER_BRACELET_OFFSET, 1 if (ctx.has_power_bracelet and not (ctx.current_level == 53 and ctx.current_screen == 43)) else 0)
                        dme.write_byte(link_adr + addresses.ZFSA_LINK_BLUE_BRACELET_OFFSET, 1 if ctx.has_blue_bracelet else 0)
                        dme.write_word(link_adr + addresses.ZFSA_LINK_HEALTHMAX_OFFSET, ctx.current_health)
                        health = dme.read_word(link_adr + addresses.ZFSA_LINK_HEALTH_OFFSET)
                        if health > ctx.current_health:
                            dme.write_word(link_adr + addresses.ZFSA_LINK_HEALTH_OFFSET, ctx.current_health)
                        
                        #poptracker
                        cur_layer = dme.read_word(link_adr + addresses.ZFSA_LINK_LAYER_OFFSET) & 0b111
                        await send_map_id(ctx.current_level, ctx.current_screen, cur_layer, ctx)
                        
                        #deathlink
                        if health <= 0:
                            if not ctx.deathlink_sent_this_death:
                                ctx.deathlink_sent_this_death = True
                                if ctx.deathlink_enabled and not ctx.deathlink_killed_player:
                                    await ctx.send_death("Died in Four Swords Adventures")
                        else:
                            ctx.deathlink_sent_this_death = False
                            ctx.deathlink_killed_player = False
                        if ctx.deathlink_pending:
                            ctx.deathlink_pending = False
                            ctx.deathlink_killed_player = True
                            dme.write_word(link_adr + addresses.ZFSA_LINK_HEALTH_OFFSET, 0)
                        
                        #link item legal
                        equiped_item = dme.read_word(link_adr + addresses.ZFSA_LINK_ITEM_OFFSET)
                        equiped_item_lvl = dme.read_word(link_adr + addresses.ZFSA_LINK_ITEMLVL_OFFSET)
                        if equiped_item <= 10:
                            if not KEYITEMS[equiped_item].active:
                                while not KEYITEMS[equiped_item].active:
                                    equiped_item += 1
                                    if equiped_item > 10:
                                        equiped_item = 0
                                dme.write_word(link_adr + addresses.ZFSA_LINK_ITEM_OFFSET, equiped_item)
                            if equiped_item_lvl != KEYITEMS[equiped_item].item_lvl:
                                dme.write_word(link_adr + addresses.ZFSA_LINK_ITEMLVL_OFFSET, KEYITEMS[equiped_item].item_lvl)
                            
                            #item carousell
                            equip_item = equiped_item
                            controller_input = dme.read_word(addresses.ZFSA_CONTROLLER_INPUT)
                            isDpadLPressed = (controller_input & addresses.ZFSA_CONTROLLER_DL_MASK) > 0
                            wasDpadLPressed = (controller_input_prev & addresses.ZFSA_CONTROLLER_DL_MASK) > 0
                            if isDpadLPressed and not wasDpadLPressed: equip_item -= 1
                            isDpadRPressed = (controller_input & addresses.ZFSA_CONTROLLER_DR_MASK) > 0
                            wasDpadRPressed = (controller_input_prev & addresses.ZFSA_CONTROLLER_DR_MASK) > 0
                            if isDpadRPressed and not wasDpadRPressed: equip_item += 1
                            if equip_item != equiped_item:
                                cycledir = 1 if isDpadRPressed else -1
                                if equip_item > 10: equip_item = 0
                                if equip_item < 0: equip_item = 10
                                while not KEYITEMS[equip_item].active:
                                    equip_item += cycledir
                                    if equip_item > 10: equip_item = 0
                                    if equip_item < 0: equip_item = 10
                                item = KEYITEMS[equip_item]
                                #show_message(f"Equiped {item.item_name} L{item.item_lvl}!", ctx)
                                dme.write_word(link_adr + addresses.ZFSA_LINK_ITEM_OFFSET, equip_item)
                                dme.write_word(link_adr + addresses.ZFSA_LINK_ITEMLVL_OFFSET, KEYITEMS[equip_item].item_lvl)
                            controller_input_prev = controller_input
                prev_game_state = game_state
            except Exception:
                import traceback
                logger.info(traceback.format_exc())
            
        await asyncio.sleep(0.01)


def main(connect= None, password= None):
    Utils.init_logging("ZFSAClient", exception_logger="Client")

    async def _main(connect, password):
        ctx = ZfsaContext(connect, password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        await asyncio.sleep(1)

        ctx.dolphin_sync_task = asyncio.create_task(dolphin_sync_task(ctx), name="DolphinSync")

        # if dme.is_hooked():
        #     logger.info("Hooked to Dolphin!")

        create_location_memory_map()
        
        progression_watcher = asyncio.create_task(game_watcher(ctx), name="ZfsaProgressionWatcher")
        stage_select_watch = asyncio.create_task(handle_stage_select(ctx))
        stage_watch = asyncio.create_task(handle_stage(ctx))
        link_watch = asyncio.create_task(handle_link(ctx))

        await progression_watcher
        await stage_select_watch
        await stage_watch
        await link_watch
        await asyncio.sleep(.25)

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.dolphin_sync_task:
            await asyncio.sleep(3)
            await ctx.dolphin_sync_task


    import colorama

    colorama.init()
    asyncio.run(_main(connect, password))
    colorama.deinit()


if __name__ == "__main__":
    parser = get_base_parser(description="Zelda Four Swords Adventures Client, for text interfacing.")
    args, rest = parser.parse_known_args()
    main(args.connect, args.password)
