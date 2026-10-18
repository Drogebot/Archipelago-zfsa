from enum import Flag, auto
from typing import Optional, NamedTuple

class ItemType(Flag):
    none = auto()
    pegasus_boots = auto()
    pegasus_bootsL2 = auto()
    lamp = auto()
    lampL2 = auto()
    boomerang = auto()
    boomerangL2 = auto()
    bow = auto()
    bowL2 = auto()
    magic_hammer = auto()
    magic_hammerL2 = auto()
    fire_rod = auto()
    fire_rodL2 = auto()
    rocs_feather = auto()
    rocs_featherL2 = auto()
    bombs = auto()
    bombsL2 = auto()
    shovel = auto()
    shovelL2 = auto()
    slingshot = auto()
    slingshotL2 = auto()
    
    
class FormationType(Flag):
    wide = auto()
    long = auto()
    box = auto()
    cross = auto()
    solo = auto()
    none = auto()


class KeyType(NamedTuple):
    name: str
    amount: int = 1


class Requirements(NamedTuple):
    items: list[list[ItemType]] = []  # conjunctive normal form
    formations: list[FormationType] = []  # conjunctive normal form
    links: int = 0
    keys: list[KeyType] = []
    gems: int = 0  # number of force gems needed
    power_bracelet: bool = False
    jewels: bool = False  # do all jewels need to be collected (configurable)
    wind_tower: bool = False  # is palace of winds access needed (configurable)
    zelda: bool = False  # is zelda required (configurable)
    special_the_mountain_path: bool = False
    special_the_swamp: bool = False
    special_temple_of_darkness: bool = False
    special_palace_of_winds: bool = False
    #options
    lamp_for_dark: bool = False
    # minor_tricks
    projectile_regroup: bool = False #skips needing projectiles, feather or bootsL2
    bomb_regroup: bool = False #skips needing bombs
    helmaroc_regroup: bool = False #skips needing hammer or bombs
    bowless_gohma: bool = False #skips needing bow
    jump_pound: bool = False #skips needing feather or bombs
    jump_pound_side: bool = False #skips needing boots, feather or bombs


class LocationFlag(NamedTuple):
    roomx: int
    roomy: int
    layer: int
    index: int


class Chest(NamedTuple):
    name: str
    id: int
    flagId: LocationFlag
    requirements: Requirements = Requirements()
    hard: Requirements = Requirements()
    advanced: Requirements = Requirements()
    tears: Requirements = Requirements()


class Key(NamedTuple):
    name: str
    id: int
    flagId: LocationFlag
    requirements: Requirements = Requirements()
    hard: Requirements = Requirements()
    advanced: Requirements = Requirements()
    tears: Requirements = Requirements()


class Jewel(NamedTuple):
    name: str
    id: int
    flagId: LocationFlag
    requirements: Requirements = Requirements()
    hard: Requirements = Requirements()
    advanced: Requirements = Requirements()
    tears: Requirements = Requirements()


class DoorType(Flag):
    door = auto(),
    big_chest = auto(),
    moon_gate = auto(),
    local_variable = auto(),
    unknown = auto(),


class Door(NamedTuple):
    key: str
    number: int
    type: DoorType
    flagId: LocationFlag


class ZfsaRegion(NamedTuple):
    name: str
    stageId: int
    id: int
    requirements: Requirements = Requirements()
    keys: list[Key] = []
    chests: list[Chest] = []
    doors: list[Door] = []
    jewel: Jewel = None
    parentRegion: Optional[str] = None

BASE_LOCATION_OFFSET = 379000

ALL_REGIONS: dict[str, ZfsaRegion] = {
    "Lake Hylia": ZfsaRegion("Lake Hylia", 10, BASE_LOCATION_OFFSET+0, Requirements([[ItemType.lamp | ItemType.fire_rod]]), [
        Key("House Key", BASE_LOCATION_OFFSET+1, LocationFlag(3,3,0,20), Requirements([[ItemType.boomerang]])),
    ], [
        Chest("River Passage Chest", BASE_LOCATION_OFFSET+2, LocationFlag(3,3,5,8), Requirements([[ItemType.lamp | ItemType.fire_rod]])),
        Chest("Waterfall Climb Chest", BASE_LOCATION_OFFSET+3, LocationFlag(3,1,5,0), Requirements([[ItemType.lamp | ItemType.fire_rod]])),
        Chest("Lake Cave Chest 1", BASE_LOCATION_OFFSET+4, LocationFlag(3,0,5,0), Requirements([[ItemType.lamp | ItemType.fire_rod]])),
        Chest("Lake Cave Chest 2", BASE_LOCATION_OFFSET+5, LocationFlag(3,0,5,1), Requirements([[ItemType.lamp | ItemType.fire_rod]])),
        Chest("Waterfall Bottom Chest 1", BASE_LOCATION_OFFSET+6, LocationFlag(3,2,6,1), Requirements([[ItemType.lamp | ItemType.fire_rod]])),
        Chest("Waterfall Bottom Chest 2", BASE_LOCATION_OFFSET+7, LocationFlag(3,2,6,2), Requirements([[ItemType.lamp | ItemType.fire_rod]])),
        Chest("Waterfall Bottom River Pasage Chest", BASE_LOCATION_OFFSET+8, LocationFlag(3,2,7,0), Requirements([[ItemType.lamp | ItemType.fire_rod]])),
        Chest("Bridge Chest 1", BASE_LOCATION_OFFSET+9, LocationFlag(2,2,0,4), Requirements([[ItemType.lamp | ItemType.fire_rod]])),
        Chest("Bridge Chest 2", BASE_LOCATION_OFFSET+10, LocationFlag(2,2,0,5), Requirements([[ItemType.lamp | ItemType.fire_rod]])),
    ], [
        Door("Lake Hylia House Key", 1, DoorType.door, LocationFlag(3,3,0,11)),
    ]),
    
    "Cave of No Return": ZfsaRegion("Cave of No Return", 11, BASE_LOCATION_OFFSET+11, Requirements([[ItemType.lamp | ItemType.fire_rod, ItemType.bow | ItemType.pegasus_bootsL2], [ItemType.fire_rod, ItemType.slingshot | ItemType.boomerangL2]], keys=[KeyType("Cave of No Return Progressive Key", 3)], lamp_for_dark=True), [
        Key("Fire Trap Room Key", BASE_LOCATION_OFFSET+12, LocationFlag(5,5,0,20), Requirements([[ItemType.lamp | ItemType.fire_rod]], keys=[KeyType("Cave of No Return Progressive Key", 2)], lamp_for_dark=True)),
    ], [
        Chest("Fire Wall Room Top Left Chest", BASE_LOCATION_OFFSET+13, LocationFlag(1,5,0,0), Requirements([[ItemType.lamp | ItemType.fire_rod]], lamp_for_dark=True)),
        Chest("Fire Wall Room Center Chest", BASE_LOCATION_OFFSET+14, LocationFlag(1,5,0,1), Requirements([[ItemType.lamp | ItemType.fire_rod]], lamp_for_dark=True)),
        Chest("Large Block Push Room Top Chest", BASE_LOCATION_OFFSET+15, LocationFlag(2,5,0,0), Requirements([[ItemType.lamp | ItemType.fire_rod]], keys=[KeyType("Cave of No Return Progressive Key")], lamp_for_dark=True)),
        Chest("Large Block Push Room Bottom Chest", BASE_LOCATION_OFFSET+16, LocationFlag(2,5,0,1), Requirements([[ItemType.lamp | ItemType.fire_rod]], keys=[KeyType("Cave of No Return Progressive Key")], lamp_for_dark=True)),
        Chest("Color Block Push Room Top Chest", BASE_LOCATION_OFFSET+17, LocationFlag(3,5,0,0), Requirements([[ItemType.lamp | ItemType.fire_rod]], keys=[KeyType("Cave of No Return Progressive Key", 2)], lamp_for_dark=True)),
        Chest("Color Block Push Room Bottom Chest", BASE_LOCATION_OFFSET+18, LocationFlag(3,5,0,1), Requirements([[ItemType.lamp | ItemType.fire_rod]], keys=[KeyType("Cave of No Return Progressive Key", 2)], lamp_for_dark=True)),
        Chest("Color Block Push Room Top Right Chest", BASE_LOCATION_OFFSET+19, LocationFlag(3,5,0,2), Requirements([[ItemType.lamp | ItemType.fire_rod]], keys=[KeyType("Cave of No Return Progressive Key", 2)], lamp_for_dark=True)),
        Chest("Trap Room Top Chest", BASE_LOCATION_OFFSET+20, LocationFlag(4,5,5,18), Requirements([[ItemType.lamp | ItemType.fire_rod]], keys=[KeyType("Cave of No Return Progressive Key", 2)], lamp_for_dark=True)),
        Chest("Trap Room Bottom Chest", BASE_LOCATION_OFFSET+21, LocationFlag(4,5,5,24), Requirements([[ItemType.lamp | ItemType.fire_rod]], keys=[KeyType("Cave of No Return Progressive Key", 2)], lamp_for_dark=True)),
        Chest("Fire Trap Room Chest", BASE_LOCATION_OFFSET+22, LocationFlag(5,5,0,0), Requirements([[ItemType.lamp | ItemType.fire_rod]], keys=[KeyType("Cave of No Return Progressive Key", 2)], lamp_for_dark=True)),
        Chest("Ghost Room Chest", BASE_LOCATION_OFFSET+23, LocationFlag(4,4,0,0), Requirements([[ItemType.lamp | ItemType.fire_rod]], keys=[KeyType("Cave of No Return Progressive Key", 2)], lamp_for_dark=True)),
        Chest("Choice Room Chest 1", BASE_LOCATION_OFFSET+24, LocationFlag(4,2,5,2), Requirements([[ItemType.lamp | ItemType.fire_rod, ItemType.bow | ItemType.pegasus_bootsL2], [ItemType.fire_rod, ItemType.slingshot | ItemType.boomerangL2]], keys=[KeyType("Cave of No Return Progressive Key", 3)], lamp_for_dark=True)),
        Chest("Choice Room Chest 2", BASE_LOCATION_OFFSET+25, LocationFlag(4,2,5,3), Requirements([[ItemType.lamp | ItemType.fire_rod, ItemType.bow | ItemType.pegasus_bootsL2], [ItemType.fire_rod, ItemType.slingshot | ItemType.boomerangL2]], keys=[KeyType("Cave of No Return Progressive Key", 3)], lamp_for_dark=True)),
        Chest("Choice Room Chest 3", BASE_LOCATION_OFFSET+26, LocationFlag(4,2,5,4), Requirements([[ItemType.lamp | ItemType.fire_rod, ItemType.bow | ItemType.pegasus_bootsL2], [ItemType.fire_rod, ItemType.slingshot | ItemType.boomerangL2]], keys=[KeyType("Cave of No Return Progressive Key", 3)], lamp_for_dark=True)),
        Chest("Choice Room Chest 4", BASE_LOCATION_OFFSET+27, LocationFlag(4,2,5,5), Requirements([[ItemType.lamp | ItemType.fire_rod, ItemType.bow | ItemType.pegasus_bootsL2], [ItemType.fire_rod, ItemType.slingshot | ItemType.boomerangL2]], keys=[KeyType("Cave of No Return Progressive Key", 3)], lamp_for_dark=True)),
        Chest("Choice Room Pull Chest", BASE_LOCATION_OFFSET+28, LocationFlag(4,2,0,0), Requirements([[ItemType.lamp | ItemType.fire_rod, ItemType.bow | ItemType.pegasus_bootsL2], [ItemType.fire_rod, ItemType.slingshot | ItemType.boomerangL2]], keys=[KeyType("Cave of No Return Progressive Key", 3)], lamp_for_dark=True)),
        # 5 chest in link fight
    ], [
        Door("Cave of No Return Progressive Key", 1, DoorType.door, LocationFlag(1,5,0,3)),
        Door("Cave of No Return Progressive Key", 2, DoorType.door, LocationFlag(2,5,0,3)),
        Door("Cave of No Return Progressive Key", 3, DoorType.door, LocationFlag(4,4,0,1)),
    ], parentRegion="Lake Hylia"),
    
    "Hyrule Castle": ZfsaRegion("Hyrule Castle", 13, BASE_LOCATION_OFFSET+29, Requirements([[ItemType.bombs]], keys=[KeyType("Hyrule Castle Inner Wall Key")]), [], [
        Chest("Castle Gate Upper Chest", BASE_LOCATION_OFFSET+30, LocationFlag(1,6,6,0), Requirements()),
        Chest("Castle Gate Lower Chest", BASE_LOCATION_OFFSET+31, LocationFlag(1,6,6,16), Requirements()),
        Chest("Castle Courtyard Chest 1", BASE_LOCATION_OFFSET+32, LocationFlag(1,5,0,0), Requirements()),
        Chest("Castle Courtyard Chest 2", BASE_LOCATION_OFFSET+33, LocationFlag(1,5,0,1), Requirements()),
        Chest("Castle Wall Left Chest 1", BASE_LOCATION_OFFSET+34, LocationFlag(0,4,2,4), Requirements()),
        Chest("Castle Wall Left Chest 2", BASE_LOCATION_OFFSET+35, LocationFlag(0,4,2,5), Requirements()),
        Chest("Castle Wall Right Yard Chest 1", BASE_LOCATION_OFFSET+36, LocationFlag(2,4,0,0), Requirements([[ItemType.boomerang | ItemType.bow | ItemType.bombs | ItemType.slingshot | ItemType.pegasus_bootsL2]])),
        Chest("Castle Wall Right Yard Chest 2", BASE_LOCATION_OFFSET+37, LocationFlag(2,4,0,1), Requirements([[ItemType.boomerang | ItemType.bow | ItemType.bombs | ItemType.slingshot | ItemType.pegasus_bootsL2]])),
        Chest("Castle Wall Right Inner Chest", BASE_LOCATION_OFFSET+38, LocationFlag(2,4,5,0), Requirements([[ItemType.boomerang | ItemType.bow | ItemType.bombs | ItemType.slingshot | ItemType.pegasus_bootsL2]])),
        Chest("Throne Wall Left Chest", BASE_LOCATION_OFFSET+39, LocationFlag(1,1,0,0), Requirements([[ItemType.bombs]], keys=[KeyType("Hyrule Castle Inner Wall Key")])),
        Chest("Throne Wall Right Chest", BASE_LOCATION_OFFSET+40, LocationFlag(1,1,0,1), Requirements([[ItemType.bombs]], keys=[KeyType("Hyrule Castle Inner Wall Key")])),
        Chest("Throne Room Left Chest", BASE_LOCATION_OFFSET+41, LocationFlag(1,1,4,0), Requirements([[ItemType.bombs]], keys=[KeyType("Hyrule Castle Inner Wall Key")])),
        Chest("Throne Room Right Chest", BASE_LOCATION_OFFSET+42, LocationFlag(1,1,4,1), Requirements([[ItemType.bombs]], keys=[KeyType("Hyrule Castle Inner Wall Key")])),
    ], [
        Door("Hyrule Castle Inner Wall Key", 1, DoorType.door, LocationFlag(1,4,2,0)),
    ], parentRegion="Cave of No Return"),
    
    
    "The Coast": ZfsaRegion("The Coast", 20, BASE_LOCATION_OFFSET+43, Requirements([[ItemType.bombs]]), [], [
        Chest("Start Cave Chest 1", BASE_LOCATION_OFFSET+44, LocationFlag(0,1,6,0), Requirements([[ItemType.bombs]])),
        Chest("Start Cave Chest 2", BASE_LOCATION_OFFSET+45, LocationFlag(0,1,6,1), Requirements([[ItemType.bombs]])),
        Chest("Left Beach Chest", BASE_LOCATION_OFFSET+46, LocationFlag(0,2,0,0), Requirements([], projectile_regroup=True)),
        Chest("House Chest", BASE_LOCATION_OFFSET+47, LocationFlag(1,2,2,0), Requirements([[ItemType.bombs]])),
        Chest("House Cave Chest", BASE_LOCATION_OFFSET+48, LocationFlag(1,2,5,0), Requirements([[ItemType.bombs]])),
        Chest("House Beach Cave Chest", BASE_LOCATION_OFFSET+49, LocationFlag(1,2,6,1), Requirements([[ItemType.bombs]])),
        Chest("Right Beach Left Cave Chest", BASE_LOCATION_OFFSET+50, LocationFlag(2,2,5,0), Requirements([[ItemType.bombs]])),
        Chest("Right Beach Right Cave Chest", BASE_LOCATION_OFFSET+51, LocationFlag(2,2,5,1), Requirements([[ItemType.bombs]])),
        Chest("Grass Hole Chest", BASE_LOCATION_OFFSET+52, LocationFlag(6,2,7,0), Requirements([[ItemType.bombs]])),
        Chest("Grass Cave Chest", BASE_LOCATION_OFFSET+53, LocationFlag(6,2,6,0), Requirements([[ItemType.bombs]])),
        Chest("Right Battle Chest 1", BASE_LOCATION_OFFSET+54, LocationFlag(7,2,0,0), Requirements([[ItemType.bombs]])),
        Chest("Right Battle Chest 2", BASE_LOCATION_OFFSET+55, LocationFlag(7,2,0,1), Requirements([[ItemType.bombs]])),
        Chest("Right Battle Chest 3", BASE_LOCATION_OFFSET+56, LocationFlag(7,2,0,2), Requirements([[ItemType.bombs]])),
        Chest("Right Battle Chest 4", BASE_LOCATION_OFFSET+57, LocationFlag(7,2,0,3), Requirements([[ItemType.bombs]])),
        Chest("Right Ocean Chest", BASE_LOCATION_OFFSET+58, LocationFlag(8,2,0,0), Requirements([[ItemType.bombs]])),
    ], []),
    
    "Village of the Blue Maiden": ZfsaRegion("Village of the Blue Maiden", 21, BASE_LOCATION_OFFSET+59, Requirements([[ItemType.pegasus_boots | ItemType.rocs_feather | ItemType.bombs]], keys=[KeyType("Village of the Blue Maiden Village Entrance Moon Gate"), KeyType("Village of the Blue Maiden Book")]), [
        Key("Village East Forrest Pearl", BASE_LOCATION_OFFSET+60, LocationFlag(2,2,5,74), Requirements([[ItemType.shovel]], keys=[KeyType("Village of the Blue Maiden Village Entrance Moon Gate")])),
    ], [
        Chest("Intersection Chest 1", BASE_LOCATION_OFFSET+61, LocationFlag(1,2,0,4), Requirements([], keys=[KeyType("Village of the Blue Maiden Village Entrance Moon Gate")])),
        Chest("Intersection Chest 2", BASE_LOCATION_OFFSET+62, LocationFlag(1,2,0,5), Requirements([], keys=[KeyType("Village of the Blue Maiden Village Entrance Moon Gate")])),
        Chest("Village East Chest", BASE_LOCATION_OFFSET+63, LocationFlag(2,2,1,17), Requirements([[ItemType.shovel, ItemType.bombs]], keys=[KeyType("Village of the Blue Maiden Village Entrance Moon Gate"), KeyType("Village of the Blue Maiden Village East Moon Gate")])),
        Chest("Village North Chest 1", BASE_LOCATION_OFFSET+64, LocationFlag(1,1,3,4), Requirements([], keys=[KeyType("Village of the Blue Maiden Village Entrance Moon Gate"), KeyType("Village of the Blue Maiden Village North Moon Gate")])),
        Chest("Village North Chest 2", BASE_LOCATION_OFFSET+65, LocationFlag(1,1,3,12), Requirements([], keys=[KeyType("Village of the Blue Maiden Village Entrance Moon Gate"), KeyType("Village of the Blue Maiden Village North Moon Gate")])),
        Chest("Village West Right House Chest", BASE_LOCATION_OFFSET+66, LocationFlag(0,1,2,0), Requirements([], keys=[KeyType("Village of the Blue Maiden Village Entrance Moon Gate")])),
        Chest("Village West Left Dark House Chest", BASE_LOCATION_OFFSET+67, LocationFlag(0,1,3,0), Requirements([], keys=[KeyType("Village of the Blue Maiden Village Entrance Moon Gate"), KeyType("Village of the Blue Maiden Village West Moon Gate")])),
        #2 pearls, the letter and the book are given by npcs, make those checks instead?
    ], [
        Door("Village of the Blue Maiden Village Entrance Moon Gate", 1, DoorType.moon_gate, LocationFlag(1,2,0,16)),
        Door("Village of the Blue Maiden Village East Moon Gate", 1, DoorType.moon_gate, LocationFlag(2,2,0,14)),
        Door("Village of the Blue Maiden Village North Moon Gate", 1, DoorType.moon_gate, LocationFlag(1,1,0,4)),
        Door("Village of the Blue Maiden Village West Moon Gate", 1, DoorType.moon_gate, LocationFlag(0,1,0,40)),
        Door("Village of the Blue Maiden Book", 1, DoorType.local_variable, LocationFlag(1,1,0,16)),
        Door("Village of the Blue Maiden Letter", 1, DoorType.unknown, LocationFlag(1,1,0,0)), #only grants you a roc's feather
    ], parentRegion="The Coast"),
    
    "Eastern Temple": ZfsaRegion("Eastern Temple", 23, BASE_LOCATION_OFFSET+68, Requirements([[ItemType.lamp | ItemType.fire_rod, ItemType.bow | ItemType.pegasus_bootsL2, ItemType.boomerang]], keys=[KeyType("Eastern Temple Entrance Key")]), [
        Key("North East Room Pearl", BASE_LOCATION_OFFSET+69, LocationFlag(3,4,0,24), Requirements([], keys=[KeyType("Eastern Temple Entrance Key")])),
        Key("North West Room Pearl", BASE_LOCATION_OFFSET+70, LocationFlag(1,4,0,5), Requirements([[ItemType.boomerang | ItemType.bow | ItemType.bombs | ItemType.slingshot | ItemType.pegasus_bootsL2]], keys=[KeyType("Eastern Temple Entrance Key")])),
    ], [
        Chest("Entrance Chest 1", BASE_LOCATION_OFFSET+71, LocationFlag(2,8,0,1), Requirements()),
        Chest("Entrance Chest 2", BASE_LOCATION_OFFSET+72, LocationFlag(2,8,0,2), Requirements()),
        Chest("East Room Right Chest", BASE_LOCATION_OFFSET+73, LocationFlag(4,5,5,19), Requirements([[ItemType.bombs]], keys=[KeyType("Eastern Temple Entrance Key")])),
        Chest("East Room Top Chest 1", BASE_LOCATION_OFFSET+74, LocationFlag(4,5,6,1), Requirements([[ItemType.bombs]], keys=[KeyType("Eastern Temple Entrance Key")])),
        Chest("East Room Top Chest 2", BASE_LOCATION_OFFSET+75, LocationFlag(4,5,6,2), Requirements([[ItemType.bombs]], keys=[KeyType("Eastern Temple Entrance Key")])),
        Chest("East Room Bottom Chest 1", BASE_LOCATION_OFFSET+76, LocationFlag(4,5,7,1), Requirements([[ItemType.bombs]], keys=[KeyType("Eastern Temple Entrance Key")])),
        Chest("East Room Bottom Chest 2", BASE_LOCATION_OFFSET+77, LocationFlag(4,5,7,5), Requirements([[ItemType.bombs]], keys=[KeyType("Eastern Temple Entrance Key")])),
        Chest("East Room Bottom Chest 3", BASE_LOCATION_OFFSET+78, LocationFlag(4,5,7,6), Requirements([[ItemType.bombs]], keys=[KeyType("Eastern Temple Entrance Key")])),
        Chest("South East Room Chest", BASE_LOCATION_OFFSET+79, LocationFlag(3,6,2,6), Requirements([], keys=[KeyType("Eastern Temple Entrance Key"), KeyType("Eastern Temple South East Key")])),
        Chest("South Room Chest 1", BASE_LOCATION_OFFSET+80, LocationFlag(2,6,6,4), Requirements([[ItemType.bombs]], keys=[KeyType("Eastern Temple Entrance Key"), KeyType("Eastern Temple South East Key")])),
        Chest("South Room Chest 2", BASE_LOCATION_OFFSET+81, LocationFlag(2,6,5,33), Requirements([[ItemType.bombs]], keys=[KeyType("Eastern Temple Entrance Key"), KeyType("Eastern Temple South East Key")])),
        Chest("West Room Chest 1", BASE_LOCATION_OFFSET+82, LocationFlag(0,5,0,0), Requirements([[ItemType.boomerang | ItemType.bow | ItemType.bombs | ItemType.slingshot | ItemType.pegasus_bootsL2]], keys=[KeyType("Eastern Temple Entrance Key")])),
        Chest("West Room Chest 2", BASE_LOCATION_OFFSET+83, LocationFlag(0,5,0,1), Requirements([[ItemType.boomerang | ItemType.bow | ItemType.bombs | ItemType.slingshot | ItemType.pegasus_bootsL2]], keys=[KeyType("Eastern Temple Entrance Key")])),
        Chest("West Room Lower Chest 1", BASE_LOCATION_OFFSET+84, LocationFlag(0,5,2,0), Requirements([[ItemType.boomerang | ItemType.bow | ItemType.bombs | ItemType.slingshot | ItemType.pegasus_bootsL2]], keys=[KeyType("Eastern Temple Entrance Key")])),
        Chest("West Room Lower Chest 2", BASE_LOCATION_OFFSET+85, LocationFlag(0,5,2,2), Requirements([[ItemType.boomerang | ItemType.bow | ItemType.bombs | ItemType.slingshot | ItemType.pegasus_bootsL2]], keys=[KeyType("Eastern Temple Entrance Key")])),
        Chest("South West Room Chest", BASE_LOCATION_OFFSET+86, LocationFlag(1,6,0,0), Requirements([[ItemType.bow]], keys=[KeyType("Eastern Temple Entrance Key"), KeyType("Eastern Temple South West Key")])),
        Chest("North Room Chest 1", BASE_LOCATION_OFFSET+87, LocationFlag(2,4,0,0), Requirements([[ItemType.lamp | ItemType.fire_rod, ItemType.bow | ItemType.pegasus_bootsL2]], keys=[KeyType("Eastern Temple Entrance Key")])),
        Chest("North Room Chest 2", BASE_LOCATION_OFFSET+88, LocationFlag(2,4,0,1), Requirements([[ItemType.lamp | ItemType.fire_rod, ItemType.bow | ItemType.pegasus_bootsL2]], keys=[KeyType("Eastern Temple Entrance Key")])),
        Chest("Battle Room Right Chest", BASE_LOCATION_OFFSET+89, LocationFlag(2,3,5,0), Requirements([[ItemType.lamp | ItemType.fire_rod, ItemType.bow | ItemType.pegasus_bootsL2]], keys=[KeyType("Eastern Temple Entrance Key")])),
        Chest("Battle Room Left Chest", BASE_LOCATION_OFFSET+90, LocationFlag(2,3,6,0), Requirements([[ItemType.lamp | ItemType.fire_rod, ItemType.bow | ItemType.pegasus_bootsL2]], keys=[KeyType("Eastern Temple Entrance Key")])),
        #Chest("Big Chest", BASE_LOCATION_OFFSET+91, LocationFlag(2,2,0,0), Requirements([[ItemType.lamp | ItemType.fire_rod, ItemType.bow | ItemType.pegasus_bootsL2]], keys=[KeyType("Eastern Temple Entrance Key"), KeyType("Eastern Temple Big Key")])),
    ], [
        Door("Eastern Temple Entrance Key", 1, DoorType.door, LocationFlag(2,8,0,0)),
        Door("Eastern Temple North East Moon Gate", 1, DoorType.moon_gate, LocationFlag(3,4,0,29)),
        Door("Eastern Temple South East Key", 1, DoorType.door, LocationFlag(3,5,0,0)),
        Door("Eastern Temple South West Key", 1, DoorType.door, LocationFlag(1,5,0,0)),
        Door("Eastern Temple South West Moon Gate", 1, DoorType.moon_gate, LocationFlag(1,6,0,25)),
        #Door("Eastern Temple Big Key", 1, DoorType.big_chest, LocationFlag(2,2,0,0)),
    ], parentRegion="Village of the Blue Maiden"),
    
    
    "Death Mountain Foothills": ZfsaRegion("Death Mountain Foothills", 30, BASE_LOCATION_OFFSET+92, Requirements([[ItemType.bow | ItemType.pegasus_bootsL2 | ItemType.rocs_featherL2, ItemType.magic_hammer]]), [], [
        Chest("Start Chest", BASE_LOCATION_OFFSET+93, LocationFlag(0,8,5,2), Requirements()),
        Chest("Past Bridge Chest 1", BASE_LOCATION_OFFSET+94, LocationFlag(0,5,5,42), Requirements([[ItemType.bow | ItemType.pegasus_bootsL2 | ItemType.rocs_featherL2]])),
        Chest("Past Bridge Chest 2", BASE_LOCATION_OFFSET+95, LocationFlag(0,5,5,43), Requirements([[ItemType.bow | ItemType.pegasus_bootsL2 | ItemType.rocs_featherL2]])),
        Chest("Mountain Side Chest 1", BASE_LOCATION_OFFSET+96, LocationFlag(0,4,5,0), Requirements([[ItemType.bow | ItemType.pegasus_bootsL2 | ItemType.rocs_featherL2]])),
        Chest("Mountain Side Chest 2", BASE_LOCATION_OFFSET+97, LocationFlag(0,4,5,1), Requirements([[ItemType.bow | ItemType.pegasus_bootsL2 | ItemType.rocs_featherL2]])),
        Chest("Maze Chest", BASE_LOCATION_OFFSET+98, LocationFlag(1,4,5,2), Requirements([[ItemType.bow | ItemType.pegasus_bootsL2 | ItemType.rocs_featherL2, ItemType.magic_hammer]])),
        Chest("Mountain Side Bomb Chest", BASE_LOCATION_OFFSET+99, LocationFlag(1,3,5,0), Requirements([[ItemType.bow | ItemType.pegasus_bootsL2 | ItemType.rocs_featherL2, ItemType.magic_hammer, ItemType.lamp | ItemType.boomerang | ItemType.bow | ItemType.fire_rod | ItemType.bombs | ItemType.slingshot | ItemType.pegasus_bootsL2 | ItemType.magic_hammerL2]])),
        Chest("Mountain Path Lower Chest", BASE_LOCATION_OFFSET+100, LocationFlag(2,3,5,1), Requirements([[ItemType.bow | ItemType.pegasus_bootsL2 | ItemType.rocs_featherL2, ItemType.magic_hammer, ItemType.boomerang | ItemType.rocs_feather | ItemType.pegasus_bootsL2 | ItemType.bombsL2 | ItemType.slingshotL2]])),
        Chest("Hebra's Hill Chest 1", BASE_LOCATION_OFFSET+101, LocationFlag(2,1,5,0), Requirements([[ItemType.bow | ItemType.pegasus_bootsL2 | ItemType.rocs_featherL2, ItemType.magic_hammer]])),
        Chest("Hebra's Hill Chest 2", BASE_LOCATION_OFFSET+102, LocationFlag(2,1,5,1), Requirements([[ItemType.bow | ItemType.pegasus_bootsL2 | ItemType.rocs_featherL2, ItemType.magic_hammer]])),
    ], []),
    
    "The Mountain Path": ZfsaRegion("The Mountain Path", 31, BASE_LOCATION_OFFSET+103, Requirements([], helmaroc_regroup=True), [
        Key("Water Storage Key", BASE_LOCATION_OFFSET+104, LocationFlag(3,4,0,41), Requirements([[ItemType.magic_hammer]])),#This is a Hammer Bulge
    ], [
        Chest("Platform Wall Center Chest", BASE_LOCATION_OFFSET+105, LocationFlag(0,6,6,0), Requirements()),
        Chest("Platform Wall Right Chest 1", BASE_LOCATION_OFFSET+106, LocationFlag(0,6,7,0), Requirements([], bomb_regroup=True)),
        Chest("Platform Wall Right Chest 2", BASE_LOCATION_OFFSET+107, LocationFlag(0,6,7,1), Requirements([], bomb_regroup=True)),
        Chest("House Chest", BASE_LOCATION_OFFSET+108, LocationFlag(2,4,6,0), Requirements([], special_the_mountain_path=True)),
    ], [
        Door("The Mountain Path Water Storage Key", 1, DoorType.door, LocationFlag(3,4,7,0)),
    ], parentRegion="Death Mountain Foothills"),
    
    "Tower of Flames": ZfsaRegion("Tower of Flames", 33, BASE_LOCATION_OFFSET+109, Requirements([[ItemType.bow | ItemType.slingshot | ItemType.pegasus_bootsL2 | ItemType.boomerangL2 | ItemType.bombsL2, ItemType.rocs_feather | ItemType.pegasus_bootsL2, ItemType.bombs]], keys=[KeyType("Tower of Flames 4F Key")]), [], [
        #Chest("2F Chest 1", BASE_LOCATION_OFFSET+110, LocationFlag(1,7,0,0), Requirements([[ItemType.bow | ItemType.slingshot | ItemType.pegasus_bootsL2 | ItemType.boomerangL2 | ItemType.bombsL2]])),# didn't spawn???
        Chest("2F Chest", BASE_LOCATION_OFFSET+111, LocationFlag(1,7,0,1), Requirements([[ItemType.bow | ItemType.slingshot | ItemType.pegasus_bootsL2 | ItemType.boomerangL2 | ItemType.bombsL2]])),
        #Chest("2F Chest 3", BASE_LOCATION_OFFSET+112, LocationFlag(1,7,0,2), Requirements([[ItemType.bow | ItemType.slingshot | ItemType.pegasus_bootsL2 | ItemType.boomerangL2 | ItemType.bombsL2]])),# didn't spawn???
        Chest("3F Chest 1", BASE_LOCATION_OFFSET+113, LocationFlag(1,6,0,0), Requirements([[ItemType.bow | ItemType.slingshot | ItemType.pegasus_bootsL2 | ItemType.boomerangL2 | ItemType.bombsL2, ItemType.rocs_feather | ItemType.pegasus_bootsL2]])),
        Chest("3F Chest 2", BASE_LOCATION_OFFSET+114, LocationFlag(1,6,0,1), Requirements([[ItemType.bow | ItemType.slingshot | ItemType.pegasus_bootsL2 | ItemType.boomerangL2 | ItemType.bombsL2, ItemType.rocs_feather | ItemType.pegasus_bootsL2]])),
        Chest("4F Chest 1", BASE_LOCATION_OFFSET+115, LocationFlag(1,5,6,2), Requirements([[ItemType.bow | ItemType.slingshot | ItemType.pegasus_bootsL2 | ItemType.boomerangL2 | ItemType.bombsL2, ItemType.rocs_feather | ItemType.pegasus_bootsL2]])),
        Chest("4F Chest 2", BASE_LOCATION_OFFSET+116, LocationFlag(1,5,5,0), Requirements([[ItemType.bow | ItemType.slingshot | ItemType.pegasus_bootsL2 | ItemType.boomerangL2 | ItemType.bombsL2, ItemType.rocs_feather | ItemType.pegasus_bootsL2]])),
        Chest("4F Chest 3", BASE_LOCATION_OFFSET+117, LocationFlag(1,5,5,3), Requirements([[ItemType.bow | ItemType.slingshot | ItemType.pegasus_bootsL2 | ItemType.boomerangL2 | ItemType.bombsL2, ItemType.rocs_feather | ItemType.pegasus_bootsL2]])),
        Chest("6F Chest 1", BASE_LOCATION_OFFSET+118, LocationFlag(1,3,0,1), Requirements([[ItemType.bow | ItemType.slingshot | ItemType.pegasus_bootsL2 | ItemType.boomerangL2 | ItemType.bombsL2, ItemType.rocs_feather | ItemType.pegasus_bootsL2]], keys=[KeyType("Tower of Flames 4F Key")])),
        Chest("6F Chest 2", BASE_LOCATION_OFFSET+119, LocationFlag(1,3,0,2), Requirements([[ItemType.bow | ItemType.slingshot | ItemType.pegasus_bootsL2 | ItemType.boomerangL2 | ItemType.bombsL2, ItemType.rocs_feather | ItemType.pegasus_bootsL2]], keys=[KeyType("Tower of Flames 4F Key")])),
        Chest("6F Chest 3", BASE_LOCATION_OFFSET+120, LocationFlag(1,3,6,0), Requirements([[ItemType.bow | ItemType.slingshot | ItemType.pegasus_bootsL2 | ItemType.boomerangL2 | ItemType.bombsL2, ItemType.rocs_feather | ItemType.pegasus_bootsL2, ItemType.bombs]], keys=[KeyType("Tower of Flames 4F Key")])),
        Chest("7F Chest 1", BASE_LOCATION_OFFSET+121, LocationFlag(0,2,0,0), Requirements([[ItemType.bow | ItemType.slingshot | ItemType.pegasus_bootsL2 | ItemType.boomerangL2 | ItemType.bombsL2, ItemType.rocs_feather | ItemType.pegasus_bootsL2]], keys=[KeyType("Tower of Flames 4F Key")])),
        Chest("7F Chest 2", BASE_LOCATION_OFFSET+122, LocationFlag(0,2,0,1), Requirements([[ItemType.bow | ItemType.slingshot | ItemType.pegasus_bootsL2 | ItemType.boomerangL2 | ItemType.bombsL2, ItemType.rocs_feather | ItemType.pegasus_bootsL2]], keys=[KeyType("Tower of Flames 4F Key")])),
    ], [
        Door("Tower of Flames 4F Key", 1, DoorType.door, LocationFlag(1,5,0,0)),
    ], parentRegion="The Mountain Path"),
    
    
    "The Field": ZfsaRegion("The Field", 40, BASE_LOCATION_OFFSET+123, Requirements([[ItemType.shovel]]), [
        #The son in someone's house gives storeroom key
        Key("Strange Cave Key", BASE_LOCATION_OFFSET+124, LocationFlag(6,0,3,11), Requirements([[ItemType.rocs_feather | ItemType.pegasus_bootsL2]])),
        #Key("Strange Cave Key 2", BASE_LOCATION_OFFSET+125, LocationFlag(6,0,5,20), Requirements()),#? not accessable?
        #Key("Strange Cave Key 3", BASE_LOCATION_OFFSET+126, LocationFlag(6,0,6,74), Requirements()),#? not accessable?
        #Key("Strange Cave Key 4", BASE_LOCATION_OFFSET+127, LocationFlag(6,0,6,79), Requirements()),#? not accessable?
    ], [
        #Chest("West Fire Cannon Chest", BASE_LOCATION_OFFSET+128, LocationFlag(0,8,5,0), Requirements()),# not accessable?
        Chest("Lon Lon Ranch Hole Chest 1", BASE_LOCATION_OFFSET+129, LocationFlag(2,8,6,0), Requirements()),
        Chest("Lon Lon Ranch Hole Chest 2", BASE_LOCATION_OFFSET+130, LocationFlag(2,8,6,1), Requirements()),
        Chest("Lon Lon Ranch Basement Chest 1", BASE_LOCATION_OFFSET+131, LocationFlag(2,8,5,2), Requirements()),
        Chest("Lon Lon Ranch Basement Chest 2", BASE_LOCATION_OFFSET+132, LocationFlag(2,8,5,5), Requirements()),
        Chest("House Right Hole Chest", BASE_LOCATION_OFFSET+133, LocationFlag(6,3,5,0), Requirements()),
        Chest("House Left Hole Chest", BASE_LOCATION_OFFSET+134, LocationFlag(6,3,6,0), Requirements()),
        Chest("House Yard Chest", BASE_LOCATION_OFFSET+135, LocationFlag(6,3,0,0), Requirements()),
        Chest("House North Left Hole Chest", BASE_LOCATION_OFFSET+136, LocationFlag(6,2,5,0), Requirements()),
        Chest("House North Right Hole Chest", BASE_LOCATION_OFFSET+137, LocationFlag(6,2,5,3), Requirements()),
        Chest("Fairy Cave Chest", BASE_LOCATION_OFFSET+138, LocationFlag(7,1,5,0), Requirements([[ItemType.rocs_feather | ItemType.pegasus_bootsL2]])),
        Chest("Fairy Gap Chest", BASE_LOCATION_OFFSET+139, LocationFlag(7,1,0,0), Requirements([[ItemType.rocs_feather | ItemType.pegasus_bootsL2]])),
        #Chest("Strange Cave Chest", BASE_LOCATION_OFFSET+140, LocationFlag(6,0,4,0), Requirements()),#? not accessable?
        Chest("Storeroom North North Hole Chest", BASE_LOCATION_OFFSET+141, LocationFlag(7,2,5,0), Requirements([[ItemType.shovel]])),
        Chest("Storeroom North West Hole Chest", BASE_LOCATION_OFFSET+142, LocationFlag(7,2,5,1), Requirements([[ItemType.shovel]])),
        Chest("Storeroom North East Hole Chest", BASE_LOCATION_OFFSET+143, LocationFlag(7,2,5,2), Requirements([[ItemType.shovel]])),
        #Chest("Storeroom North South Hole Chest", BASE_LOCATION_OFFSET+144, LocationFlag(7,2,6,0), Requirements([[ItemType.shovel]])),# not accessable?
        Chest("Storeroom North South Hole Chest", BASE_LOCATION_OFFSET+145, LocationFlag(7,2,6,3), Requirements([[ItemType.shovel]])),
        Chest("Movable House Hole Chest 1", BASE_LOCATION_OFFSET+146, LocationFlag(8,1,5,0), Requirements([[ItemType.shovel]])),
        Chest("Movable House Hole Chest 2", BASE_LOCATION_OFFSET+147, LocationFlag(8,1,5,1), Requirements([[ItemType.shovel]])),
    ], [
        Door("The Field Storeroom Key", 1, DoorType.door, LocationFlag(7,3,0,0)),
        Door("The Field Stange Cave Key", 1, DoorType.door, LocationFlag(6,0,5,0)),
    ], jewel=Jewel("Blue Royal Jewel", BASE_LOCATION_OFFSET+493, LocationFlag(8,0,0,18), Requirements([[ItemType.shovel]])),
    ),
    
    "The Swamp": ZfsaRegion("The Swamp", 41, BASE_LOCATION_OFFSET+148, Requirements([[ItemType.rocs_feather]], power_bracelet=True), [
        Key("Graveyard East Key", BASE_LOCATION_OFFSET+149, LocationFlag(1,5,6,62), Requirements([[ItemType.rocs_feather, ItemType.bow]], keys=[KeyType("The Swamp Progressive Graveyard East Key")])),
    ], [
        Chest("East Cave Chest", BASE_LOCATION_OFFSET+150, LocationFlag(4,8,5,1), Requirements()),
        Chest("East Lily Pad Chest 1", BASE_LOCATION_OFFSET+151, LocationFlag(3,8,5,6), Requirements([[ItemType.rocs_feather | ItemType.pegasus_bootsL2]], jump_pound=True)),
        Chest("East Lily Pad Chest 2", BASE_LOCATION_OFFSET+152, LocationFlag(3,8,5,16), Requirements([[ItemType.rocs_feather | ItemType.pegasus_bootsL2]], jump_pound=True)),
        Chest("Graveyard Entrance South Cave Chest 1", BASE_LOCATION_OFFSET+153, LocationFlag(0,6,5,2), Requirements([[ItemType.rocs_feather | ItemType.pegasus_bootsL2]], jump_pound=True)),
        Chest("Graveyard Entrance South Cave Chest 2", BASE_LOCATION_OFFSET+154, LocationFlag(0,6,5,3), Requirements([[ItemType.rocs_feather | ItemType.pegasus_bootsL2]], jump_pound=True)),
        Chest("Graveyard Entrance North Cave Chest", BASE_LOCATION_OFFSET+155, LocationFlag(0,6,7,8), Requirements([[ItemType.rocs_feather]])),
        Chest("Graveyard West Grave Chest 1", BASE_LOCATION_OFFSET+156, LocationFlag(0,5,5,0), Requirements([[ItemType.rocs_feather]])),
        Chest("Graveyard West Grave Chest 2", BASE_LOCATION_OFFSET+157, LocationFlag(0,5,5,1), Requirements([[ItemType.rocs_feather]])),
        #Chest("Graveyard West Left Grave Chest", BASE_LOCATION_OFFSET+158, LocationFlag(0,5,7,1), Requirements([[ItemType.rocs_feather]])),# not accessable?
        Chest("Dampe Chest", BASE_LOCATION_OFFSET+159, LocationFlag(0,4,2,0), Requirements([[ItemType.rocs_feather]], special_the_swamp=True)),
        Chest("Graveyard East Chest 1", BASE_LOCATION_OFFSET+160, LocationFlag(1,5,7,16), Requirements([[ItemType.rocs_feather, ItemType.bow]])),
        Chest("Graveyard East Chest 2", BASE_LOCATION_OFFSET+161, LocationFlag(1,5,7,18), Requirements([[ItemType.rocs_feather, ItemType.bow]], keys=[KeyType("The Swamp Progressive Graveyard East Key", 2)])),
        Chest("Graveyard East Chest 3", BASE_LOCATION_OFFSET+162, LocationFlag(1,5,7,21), Requirements([[ItemType.rocs_feather, ItemType.bow]], keys=[KeyType("The Swamp Progressive Graveyard East Key", 2)])),
        Chest("Graveyard East Chest 4", BASE_LOCATION_OFFSET+163, LocationFlag(1,5,6,2), Requirements([[ItemType.rocs_feather, ItemType.bow]], keys=[KeyType("The Swamp Progressive Graveyard East Key", 2)])),
    ], [
        Door("The Swamp Moon Gate", 1, DoorType.moon_gate, LocationFlag(0,4,0,83)),
        Door("The Swamp Progressive Graveyard East Key", 1, DoorType.door, LocationFlag(1,5,6,14)),
        Door("The Swamp Progressive Graveyard East Key", 2, DoorType.door, LocationFlag(1,5,6,33)),
    ], parentRegion="The Field"),
    
    "Infiltration of Hyrule Castle": ZfsaRegion("Infiltration of Hyrule Castle", 43, BASE_LOCATION_OFFSET+164, Requirements([[ItemType.bow | ItemType.fire_rod | ItemType.pegasus_bootsL2, ItemType.lamp | ItemType.fire_rod]], keys=[KeyType("Infiltration of Hyrule Castle Progressive Basement Key", 2)]), [
        Key("Outside Jail Key", BASE_LOCATION_OFFSET+165, LocationFlag(4,6,0,16), Requirements([[ItemType.boomerang]])),
        Key("Basement Stairs Room Pearl", BASE_LOCATION_OFFSET+166, LocationFlag(0,3,0,15), Requirements([], keys=[KeyType("Infiltration of Hyrule Castle Progressive Basement Key")])),
    ], [
        Chest("Outside Jail Chest", BASE_LOCATION_OFFSET+167, LocationFlag(4,6,5,7), Requirements()),
        Chest("Wall East Chest 1", BASE_LOCATION_OFFSET+168, LocationFlag(2,5,0,0), Requirements()),
        Chest("Wall East Chest 2", BASE_LOCATION_OFFSET+169, LocationFlag(2,5,0,1), Requirements()),
        Chest("Wall West Chest 1", BASE_LOCATION_OFFSET+170, LocationFlag(1,5,0,0), Requirements()),
        Chest("Wall West Chest 2", BASE_LOCATION_OFFSET+171, LocationFlag(1,5,0,1), Requirements()),
        Chest("Basement Stairs Room Chest", BASE_LOCATION_OFFSET+172, LocationFlag(0,3,0,0), Requirements()),
        Chest("Basement Stairs Room Moon Gate Chest", BASE_LOCATION_OFFSET+173, LocationFlag(0,3,1,0), Requirements([], keys=[KeyType("Infiltration of Hyrule Castle Basement Stairs Moon Gate")])),
        #Chest("Basement Stairs Room Chest 3", BASE_LOCATION_OFFSET+174, LocationFlag(0,3,2,0), Requirements()),# not accessable?
        #Chest("Basement Stairs Room Chest 4", BASE_LOCATION_OFFSET+175, LocationFlag(0,3,2,1), Requirements()),# not accessable?
        Chest("Eye Void Room Chest 1", BASE_LOCATION_OFFSET+176, LocationFlag(1,3,0,0), Requirements([], keys=[KeyType("Infiltration of Hyrule Castle Progressive Basement Key")])),
        Chest("Eye Void Room Chest 2", BASE_LOCATION_OFFSET+177, LocationFlag(1,3,0,1), Requirements([], keys=[KeyType("Infiltration of Hyrule Castle Progressive Basement Key")])),
        Chest("Eye Void Room Chest 3", BASE_LOCATION_OFFSET+178, LocationFlag(1,3,0,2), Requirements([], keys=[KeyType("Infiltration of Hyrule Castle Progressive Basement Key")])),
        Chest("Yard Jail Chest", BASE_LOCATION_OFFSET+179, LocationFlag(4,5,5,8), Requirements([[ItemType.bow | ItemType.fire_rod | ItemType.pegasus_bootsL2]], keys=[KeyType("Infiltration of Hyrule Castle Progressive Basement Key", 2)])),
        Chest("Yard Chest 1", BASE_LOCATION_OFFSET+180, LocationFlag(2,4,0,0), Requirements([[ItemType.bow | ItemType.fire_rod | ItemType.pegasus_bootsL2]], keys=[KeyType("Infiltration of Hyrule Castle Progressive Basement Key", 2)])),
        Chest("Yard Chest 2", BASE_LOCATION_OFFSET+181, LocationFlag(2,4,0,1), Requirements([[ItemType.bow | ItemType.fire_rod | ItemType.pegasus_bootsL2]], keys=[KeyType("Infiltration of Hyrule Castle Progressive Basement Key", 2)])),
        #Chest("Fire Void Room Chest 1", BASE_LOCATION_OFFSET+182, LocationFlag(2,3,7,0), Requirements([], keys=[KeyType("Infiltration of Hyrule Castle Progressive Basement Key", 2)])),# not accessable?
        #Chest("Fire Void Room Chest 2", BASE_LOCATION_OFFSET+183, LocationFlag(2,3,7,1), Requirements([], keys=[KeyType("Infiltration of Hyrule Castle Progressive Basement Key", 2)])),# not accessable?
    ], [
        Door("Infiltration of Hyrule Castle Lower Jail Key", 1, DoorType.door, LocationFlag(4,6,0,0)),
        Door("Infiltration of Hyrule Castle Basement Stairs Moon Gate", 1, DoorType.moon_gate, LocationFlag(0,3,0,36)),
        Door("Infiltration of Hyrule Castle Progressive Basement Key", 1, DoorType.door, LocationFlag(0,3,0,2)),
        Door("Infiltration of Hyrule Castle Progressive Basement Key", 2, DoorType.door, LocationFlag(1,3,0,6)),
        Door("Infiltration of Hyrule Castle Progressive Basement Key", 3, DoorType.door, LocationFlag(2,3,0,0)),
    ], parentRegion="The Swamp"),
    
    
    "Lost Woods": ZfsaRegion("Lost Woods", 50, BASE_LOCATION_OFFSET+184, Requirements([[ItemType.shovel]]), [
        Key("South Woods Storage Key", BASE_LOCATION_OFFSET+185, LocationFlag(3,5,0,10), Requirements()),
    ], [
        Chest("North Woods Exit Passage Left Hole Chest", BASE_LOCATION_OFFSET+186, LocationFlag(3,1,5,0), Requirements([[ItemType.shovel]])),
        #Chest("North Woods Exit Passage Right Hole Chest", BASE_LOCATION_OFFSET+187, LocationFlag(3,1,5,1), Requirements([[ItemType.shovel]])),# not accessable?
        Chest("North Woods Exit Chest", BASE_LOCATION_OFFSET+188, LocationFlag(4,1,5,7), Requirements([[ItemType.shovel]])),
        #East Woods Moon Gate(r14) use moon pearl to get lamp
        Chest("East Woods Moon Gate Chest", BASE_LOCATION_OFFSET+189, LocationFlag(4,3,0,5), Requirements([[ItemType.lamp | ItemType.fire_rod | ItemType.bombs]])),
        Chest("East Woods Switches Chest 1", BASE_LOCATION_OFFSET+190, LocationFlag(4,4,0,0), Requirements([[ItemType.rocs_feather | ItemType.pegasus_bootsL2]])),
        Chest("East Woods Switches Chest 2", BASE_LOCATION_OFFSET+191, LocationFlag(4,4,0,1), Requirements([[ItemType.rocs_feather | ItemType.pegasus_bootsL2]])),
        Chest("North Woods Storage Right Hole Chest", BASE_LOCATION_OFFSET+192, LocationFlag(2,1,5,5), Requirements([[ItemType.lamp | ItemType.fire_rod | ItemType.bombs, ItemType.shovel]])),
        Chest("North Woods Storage Left Hole Chest 1", BASE_LOCATION_OFFSET+193, LocationFlag(2,1,6,1), Requirements([[ItemType.lamp | ItemType.fire_rod | ItemType.bombs, ItemType.shovel]])),
        Chest("North Woods Storage Left Hole Chest 2", BASE_LOCATION_OFFSET+194, LocationFlag(2,1,6,2), Requirements([[ItemType.lamp | ItemType.fire_rod | ItemType.bombs, ItemType.shovel]])),
        Chest("North Woods Storage Left Hole Chest 3", BASE_LOCATION_OFFSET+195, LocationFlag(2,1,6,3), Requirements([[ItemType.lamp | ItemType.fire_rod | ItemType.bombs, ItemType.shovel]])),
        Chest("West Woods Switches Chest", BASE_LOCATION_OFFSET+196, LocationFlag(0,4,5,0), Requirements([[ItemType.lamp | ItemType.fire_rod | ItemType.bombs]], power_bracelet=True)),
        Chest("Central Woods Kill Chest", BASE_LOCATION_OFFSET+197, LocationFlag(2,2,0,7), Requirements([[ItemType.lamp | ItemType.fire_rod | ItemType.bombs]])),
        #Chest("Central Woods Kill Chest 2", BASE_LOCATION_OFFSET+198, LocationFlag(2,2,0,1), Requirements([ItemType.lamp | ItemType.fire_rod | ItemType.bombs]])),# not accessable?
        #Chest("Central Woods Kill Chest 3", BASE_LOCATION_OFFSET+199, LocationFlag(2,2,0,2), Requirements([ItemType.lamp | ItemType.fire_rod | ItemType.bombs]])),# not accessable?
        #Chest("West Woods Battle 1 Chest", BASE_LOCATION_OFFSET+200, LocationFlag(0,3,5,0), Requirements([ItemType.lamp | ItemType.fire_rod | ItemType.bombs]], power_bracelet=True)),# not accessable?
        Chest("Central Woods Right Chest", BASE_LOCATION_OFFSET+201, LocationFlag(1,3,0,3), Requirements([[ItemType.lamp | ItemType.fire_rod | ItemType.bombs]])),
        Chest("Central Woods Left Chest", BASE_LOCATION_OFFSET+202, LocationFlag(1,3,0,0), Requirements([[ItemType.lamp | ItemType.fire_rod | ItemType.bombs]], power_bracelet=True)),
        Chest("West Woods Battle 2 Chest", BASE_LOCATION_OFFSET+203, LocationFlag(1,2,0,0), Requirements([[ItemType.lamp | ItemType.fire_rod | ItemType.bombs, ItemType.bow]], power_bracelet=True)),
        Chest("South Woods Pot Storage Chest 1", BASE_LOCATION_OFFSET+204, LocationFlag(2,5,0,12), Requirements([[ItemType.lamp | ItemType.fire_rod | ItemType.bombs]])),
        Chest("South Woods Pot Storage Chest 2", BASE_LOCATION_OFFSET+205, LocationFlag(2,5,0,22), Requirements([[ItemType.lamp | ItemType.fire_rod | ItemType.bombs]])),
        #Chest("South Woods Pot Storage Chest 4", BASE_LOCATION_OFFSET+206, LocationFlag(2,5,0,25), Requirements([[ItemType.lamp | ItemType.fire_rod | ItemType.bombs]])),# not accessable?
        Chest("South Woods Pot Storage Chest 3", BASE_LOCATION_OFFSET+207, LocationFlag(2,5,0,26), Requirements([[ItemType.lamp | ItemType.fire_rod | ItemType.bombs]])),
        #Chest("South Woods Pot Storage Chest 5", BASE_LOCATION_OFFSET+208, LocationFlag(2,5,0,27), Requirements([[ItemType.lamp | ItemType.fire_rod | ItemType.bombs]])),# not accessable?
        #South Woods Fetch(r23) guy gives power bracelet, make check?
    ], [
        Door("Lost Woods East Woods Moon Gate", 1, DoorType.moon_gate, LocationFlag(4,3,0,2)),
        Door("Lost Woods North Woods Storage Key", 1, DoorType.door, LocationFlag(2,1,2,0)),
        Door("Lost Woods South Woods Storage Key", 1, DoorType.door, LocationFlag(3,5,2,0)),
    ]),
    
    "Kakariko Village": ZfsaRegion("Kakariko Village", 51, BASE_LOCATION_OFFSET+209, Requirements([[ItemType.pegasus_boots | ItemType.bombs, ItemType.shovel, ItemType.lamp | ItemType.fire_rod]], power_bracelet=True), [], [
        Chest("South East House Chest 1", BASE_LOCATION_OFFSET+210, LocationFlag(1,3,2,2), Requirements([], keys=[KeyType("Kakariko Village South East House Key")])),
        Chest("South East House Chest 2", BASE_LOCATION_OFFSET+211, LocationFlag(1,3,2,5), Requirements([], keys=[KeyType("Kakariko Village South East House Key")])),
        Chest("South East House Chest 3", BASE_LOCATION_OFFSET+212, LocationFlag(1,3,2,6), Requirements([], keys=[KeyType("Kakariko Village South East House Key")])),
        #Chest("South West Chest 1", BASE_LOCATION_OFFSET+213, LocationFlag(0,3,2,0), Requirements()),# not accessable?
        #Chest("South West Chest 2", BASE_LOCATION_OFFSET+214, LocationFlag(0,3,2,1), Requirements()),# not accessable?
        Chest("South West Left House Chest", BASE_LOCATION_OFFSET+215, LocationFlag(0,3,2,3), Requirements()),
        #Chest("South West Chest 4", BASE_LOCATION_OFFSET+216, LocationFlag(0,3,2,3), Requirements()),# not accessable?
        Chest("South West Right Yard Chest 1", BASE_LOCATION_OFFSET+217, LocationFlag(0,3,6,0), Requirements([[ItemType.pegasus_boots | ItemType.bombs, ItemType.shovel, ItemType.lamp | ItemType.fire_rod]], power_bracelet=True)),
        Chest("South West Right Yard Chest 2", BASE_LOCATION_OFFSET+218, LocationFlag(0,3,6,1), Requirements([[ItemType.pegasus_boots | ItemType.bombs, ItemType.shovel, ItemType.lamp | ItemType.fire_rod]], power_bracelet=True)),
        Chest("South West Left Hole Chest", BASE_LOCATION_OFFSET+219, LocationFlag(0,3,6,6), Requirements([[ItemType.pegasus_boots | ItemType.bombs, ItemType.shovel, ItemType.lamp | ItemType.fire_rod]], power_bracelet=True)),
        Chest("North West Chest", BASE_LOCATION_OFFSET+220, LocationFlag(0,2,0,0), Requirements([[ItemType.bombs]])),
        Chest("North East Chest 1", BASE_LOCATION_OFFSET+221, LocationFlag(1,2,0,2), Requirements([[ItemType.pegasus_boots | ItemType.bombs, ItemType.shovel]], power_bracelet=True)),
        Chest("North East Chest 2", BASE_LOCATION_OFFSET+222, LocationFlag(1,2,0,3), Requirements([[ItemType.pegasus_boots | ItemType.bombs, ItemType.shovel]], power_bracelet=True)),
        Chest("North East Chest 3", BASE_LOCATION_OFFSET+223, LocationFlag(1,2,0,4), Requirements([[ItemType.pegasus_boots | ItemType.bombs, ItemType.shovel]], power_bracelet=True)),
        Chest("North East Chest 4", BASE_LOCATION_OFFSET+224, LocationFlag(1,2,0,5), Requirements([[ItemType.pegasus_boots | ItemType.bombs, ItemType.shovel]], power_bracelet=True)),
        Chest("North East House Chest 1", BASE_LOCATION_OFFSET+225, LocationFlag(1,2,2,0), Requirements([], power_bracelet=True)),
        Chest("North East House Chest 2", BASE_LOCATION_OFFSET+226, LocationFlag(1,2,2,1), Requirements([], power_bracelet=True)),
        Chest("Maze Chest", BASE_LOCATION_OFFSET+227, LocationFlag(1,1,0,0), Requirements([[ItemType.pegasus_boots | ItemType.bombs, ItemType.shovel, ItemType.lamp | ItemType.fire_rod]], power_bracelet=True)),
        Chest("Lake Chest", BASE_LOCATION_OFFSET+228, LocationFlag(0,1,0,0), Requirements([[ItemType.pegasus_boots | ItemType.bombs, ItemType.shovel, ItemType.lamp | ItemType.fire_rod]], power_bracelet=True)),
    ], [
        Door("Kakariko Village South East House Key", 1, DoorType.door, LocationFlag(1,3,2,3)),
    ], jewel=Jewel("Green Royal Jewel", BASE_LOCATION_OFFSET+494, LocationFlag(6,8,0,18), Requirements([[ItemType.pegasus_boots | ItemType.bombs, ItemType.shovel, ItemType.lamp | ItemType.fire_rod]], power_bracelet=True)),
    parentRegion="Lost Woods"),
    
    "Temple of Darkness": ZfsaRegion("Temple of Darkness", 53, BASE_LOCATION_OFFSET+229, Requirements([[ItemType.magic_hammer, ItemType.lamp | ItemType.fire_rod]], keys=[KeyType("Temple of Darkness Progressive Key", 5)]), [
        Key("1F Stairs Key", BASE_LOCATION_OFFSET+230, LocationFlag(2,4,5,30), Requirements()),
    ], [
        Chest("Entrance Chest 1", BASE_LOCATION_OFFSET+231, LocationFlag(2,6,0,0), Requirements()),
        Chest("Entrance Chest 2", BASE_LOCATION_OFFSET+232, LocationFlag(2,6,0,1), Requirements()),
        Chest("Entrance Chest 3", BASE_LOCATION_OFFSET+233, LocationFlag(2,6,0,2), Requirements()),
        Chest("Top Stairs Right Chest", BASE_LOCATION_OFFSET+234, LocationFlag(2,4,0,0), Requirements([], keys=[KeyType("Temple of Darkness Progressive Key")])),
        Chest("Top Stairs Center Chest", BASE_LOCATION_OFFSET+235, LocationFlag(2,4,0,2), Requirements()),
        Chest("Top Stairs Top Chest 1", BASE_LOCATION_OFFSET+236, LocationFlag(2,4,0,4), Requirements([], keys=[KeyType("Temple of Darkness Progressive Key")])),
        Chest("Top Stairs Top Chest 2", BASE_LOCATION_OFFSET+237, LocationFlag(2,4,0,5), Requirements([], keys=[KeyType("Temple of Darkness Progressive Key")])),
        Chest("Top Stairs Hole Chest", BASE_LOCATION_OFFSET+238, LocationFlag(2,4,6,0), Requirements([], special_temple_of_darkness=True)),# Can be done with feather or key
        Chest("Spike Room Right Chest", BASE_LOCATION_OFFSET+239, LocationFlag(5,3,0,0), Requirements([[ItemType.magic_hammer]], keys=[KeyType("Temple of Darkness Progressive Key")])),
        Chest("Spike Room Left Center Chest 1", BASE_LOCATION_OFFSET+240, LocationFlag(3,3,0,8), Requirements([[ItemType.magic_hammer]], keys=[KeyType("Temple of Darkness Progressive Key")])),
        Chest("Spike Room Left Center Chest 2", BASE_LOCATION_OFFSET+241, LocationFlag(3,3,0,9), Requirements([[ItemType.magic_hammer]], keys=[KeyType("Temple of Darkness Progressive Key")])),
        Chest("Spike Room Left Left Chest 1", BASE_LOCATION_OFFSET+242, LocationFlag(3,3,0,0), Requirements([[ItemType.magic_hammer]], keys=[KeyType("Temple of Darkness Progressive Key", 4)])),
        Chest("Spike Room Left Left Chest 2", BASE_LOCATION_OFFSET+243, LocationFlag(3,3,0,1), Requirements([[ItemType.magic_hammer]], keys=[KeyType("Temple of Darkness Progressive Key", 4)])),
        Chest("Spike Room Left Left Chest 3", BASE_LOCATION_OFFSET+244, LocationFlag(3,3,0,2), Requirements([[ItemType.magic_hammer]], keys=[KeyType("Temple of Darkness Progressive Key", 4)])),
        Chest("Spike Room Left Left Chest 4", BASE_LOCATION_OFFSET+245, LocationFlag(3,3,0,3), Requirements([[ItemType.magic_hammer]], keys=[KeyType("Temple of Darkness Progressive Key", 4)])),
        Chest("Void I Room Chest", BASE_LOCATION_OFFSET+246, LocationFlag(5,2,0,0), Requirements([[ItemType.magic_hammer]], keys=[KeyType("Temple of Darkness Progressive Key", 2)])),
        Chest("Void I Room Moon Gate Chest", BASE_LOCATION_OFFSET+247, LocationFlag(5,2,1,3), Requirements([[ItemType.magic_hammer]], keys=[KeyType("Temple of Darkness Progressive Key", 2)])),
        Chest("Void Intersection Chest", BASE_LOCATION_OFFSET+248, LocationFlag(4,2,0,0), Requirements([[ItemType.magic_hammer]], keys=[KeyType("Temple of Darkness Progressive Key", 3)])),
        Chest("B1 Spike Room Chest", BASE_LOCATION_OFFSET+249, LocationFlag(4,3,0,30), Requirements([[ItemType.magic_hammer]], keys=[KeyType("Temple of Darkness Progressive Key", 3)])),
        Chest("Void Room Left Chest 1", BASE_LOCATION_OFFSET+250, LocationFlag(3,2,0,0), Requirements([[ItemType.magic_hammer]], keys=[KeyType("Temple of Darkness Progressive Key", 4)])),
        Chest("Void Room Left Chest 2", BASE_LOCATION_OFFSET+251, LocationFlag(3,2,0,1), Requirements([[ItemType.magic_hammer]], keys=[KeyType("Temple of Darkness Progressive Key", 4)])),
        Chest("Dark Room Chest 1", BASE_LOCATION_OFFSET+252, LocationFlag(2,3,2,0), Requirements([[ItemType.magic_hammer, ItemType.lamp | ItemType.fire_rod]], keys=[KeyType("Temple of Darkness Progressive Key", 4)])), #, lamp_for_dark=True
        Chest("Dark Room Chest 2", BASE_LOCATION_OFFSET+253, LocationFlag(2,3,2,1), Requirements([[ItemType.magic_hammer, ItemType.lamp | ItemType.fire_rod]], keys=[KeyType("Temple of Darkness Progressive Key", 4)])), #, lamp_for_dark=True
        Chest("Dark Room Chest 3", BASE_LOCATION_OFFSET+254, LocationFlag(2,3,2,2), Requirements([[ItemType.magic_hammer, ItemType.lamp | ItemType.fire_rod]], keys=[KeyType("Temple of Darkness Progressive Key", 4)])), #, lamp_for_dark=True
        Chest("Color Maze Room Top Chest 1", BASE_LOCATION_OFFSET+255, LocationFlag(2,1,0,0), Requirements([[ItemType.magic_hammer]], keys=[KeyType("Temple of Darkness Progressive Key", 5)])),
        Chest("Color Maze Room Top Chest 2", BASE_LOCATION_OFFSET+256, LocationFlag(2,1,0,1), Requirements([[ItemType.magic_hammer]], keys=[KeyType("Temple of Darkness Progressive Key", 5)])),
        Chest("Color Maze Room Center Chest", BASE_LOCATION_OFFSET+257, LocationFlag(2,1,0,8), Requirements([[ItemType.magic_hammer]], keys=[KeyType("Temple of Darkness Progressive Key", 5)])),
        Chest("Secret Room Chest", BASE_LOCATION_OFFSET+258, LocationFlag(2,2,0,0), Requirements([[ItemType.magic_hammer, ItemType.lamp | ItemType.fire_rod]], keys=[KeyType("Temple of Darkness Progressive Key", 5)])),
        Chest("Bouncy Room Top Chest 1", BASE_LOCATION_OFFSET+259, LocationFlag(1,2,0,0), Requirements([[ItemType.magic_hammer, ItemType.lamp | ItemType.fire_rod]], keys=[KeyType("Temple of Darkness Progressive Key", 5)])),
        Chest("Bouncy Room Top Chest 2", BASE_LOCATION_OFFSET+260, LocationFlag(1,2,0,1), Requirements([[ItemType.magic_hammer, ItemType.lamp | ItemType.fire_rod]], keys=[KeyType("Temple of Darkness Progressive Key", 5)])),
        Chest("Bouncy Room Bottom Chest", BASE_LOCATION_OFFSET+261, LocationFlag(1,2,0,2), Requirements([[ItemType.magic_hammer, ItemType.lamp | ItemType.fire_rod]], keys=[KeyType("Temple of Darkness Progressive Key", 5)])),
    ], [
        Door("Temple of Darkness Progressive Key", 1, DoorType.door, LocationFlag(2,4,0,1)),
        Door("Temple of Darkness Progressive Key", 2, DoorType.moon_gate, LocationFlag(5,3,0,18)),
        Door("Temple of Darkness Progressive Key", 3, DoorType.door, LocationFlag(5,2,1,1)),
        Door("Temple of Darkness Progressive Key", 4, DoorType.door, LocationFlag(4,2,0,1)),
        Door("Temple of Darkness Progressive Key", 5, DoorType.door, LocationFlag(3,1,0,0)),
        Door("Temple of Darkness Secret Room Moon Gate", 1, DoorType.moon_gate, LocationFlag(2,2,0,190)),
    ], parentRegion="Kakariko Village"),
    
    
    "Desert of Doubt": ZfsaRegion("Desert of Doubt", 60, BASE_LOCATION_OFFSET+262, Requirements([[ItemType.pegasus_bootsL2]], keys=[KeyType("Desert of Doubt Gerudo Town North East Moon Gate")]), [], [
        #Chest("Start Chest 1", BASE_LOCATION_OFFSET+263, LocationFlag(1,6,3,1), Requirements()),# not accessable?
        #Chest("Start Chest 2", BASE_LOCATION_OFFSET+264, LocationFlag(1,6,3,2), Requirements()),# not accessable?
        #Chest("Start Chest 3", BASE_LOCATION_OFFSET+265, LocationFlag(1,6,3,3), Requirements()),# not accessable?
        #Chest("Start Chest 4", BASE_LOCATION_OFFSET+266, LocationFlag(1,6,4,2), Requirements()),# not accessable?
        Chest("Gerudo Town Center House Chest 1", BASE_LOCATION_OFFSET+267, LocationFlag(1,5,3,1), Requirements()),
        Chest("Gerudo Town Center House Chest 2", BASE_LOCATION_OFFSET+268, LocationFlag(1,5,3,2), Requirements()),
        Chest("Gerudo Town Center House Chest 3", BASE_LOCATION_OFFSET+269, LocationFlag(1,5,3,3), Requirements()),
        Chest("Gerudo Town Left House Chest", BASE_LOCATION_OFFSET+270, LocationFlag(1,5,4,2), Requirements()),
        Chest("Gerudo Town North Chest", BASE_LOCATION_OFFSET+271, LocationFlag(1,4,7,0), Requirements([[ItemType.pegasus_boots | ItemType.bombs]])),
        Chest("Gerudo Town North East Chest 1", BASE_LOCATION_OFFSET+272, LocationFlag(2,4,5,0), Requirements([[ItemType.pegasus_boots | ItemType.bombs]])),
        Chest("Gerudo Town North East Chest 2", BASE_LOCATION_OFFSET+273, LocationFlag(2,4,5,1), Requirements([[ItemType.pegasus_boots | ItemType.bombs]])),
        Chest("Gerudo Town North East Chest 3", BASE_LOCATION_OFFSET+274, LocationFlag(2,4,5,2), Requirements([[ItemType.pegasus_boots | ItemType.bombs]])),
        Chest("Zuna Village South West Sand Chest 1", BASE_LOCATION_OFFSET+275, LocationFlag(2,3,4,0), Requirements([], keys=[KeyType("Desert of Doubt Gerudo Town North East Moon Gate")])),
        Chest("Zuna Village South West Sand Chest 2", BASE_LOCATION_OFFSET+276, LocationFlag(2,3,4,1), Requirements([], keys=[KeyType("Desert of Doubt Gerudo Town North East Moon Gate")])),
        Chest("Zuna Village South West Cave Chest 1", BASE_LOCATION_OFFSET+277, LocationFlag(2,3,5,10), Requirements([[ItemType.pegasus_boots | ItemType.bombs]], keys=[KeyType("Desert of Doubt Gerudo Town North East Moon Gate")])),
        Chest("Zuna Village South West Cave Chest 2", BASE_LOCATION_OFFSET+278, LocationFlag(2,3,6,10), Requirements([[ItemType.pegasus_boots | ItemType.bombs]], keys=[KeyType("Desert of Doubt Gerudo Town North East Moon Gate")])),
        Chest("Zuna Village South West Cave Chest 3", BASE_LOCATION_OFFSET+279, LocationFlag(2,3,6,18), Requirements([[ItemType.pegasus_boots | ItemType.bombs]], keys=[KeyType("Desert of Doubt Gerudo Town North East Moon Gate")])),
        Chest("Zuna Village South West Cave Chest 4", BASE_LOCATION_OFFSET+280, LocationFlag(2,3,7,1), Requirements([[ItemType.pegasus_boots | ItemType.bombs]], keys=[KeyType("Desert of Doubt Gerudo Town North East Moon Gate")])),
        Chest("Zuna Village South West Cave Chest 5", BASE_LOCATION_OFFSET+281, LocationFlag(2,3,7,2), Requirements([[ItemType.pegasus_boots | ItemType.bombs]], keys=[KeyType("Desert of Doubt Gerudo Town North East Moon Gate")])),
        Chest("Zuna Village South Chest", BASE_LOCATION_OFFSET+282, LocationFlag(3,3,5,0), Requirements([[ItemType.rocs_feather | ItemType.pegasus_bootsL2]], keys=[KeyType("Desert of Doubt Gerudo Town North East Moon Gate")])),
        Chest("Zuna Village Bottom Right House Chest 1", BASE_LOCATION_OFFSET+283, LocationFlag(3,2,2,0), Requirements([[ItemType.pegasus_boots | ItemType.rocs_feather]], keys=[KeyType("Desert of Doubt Gerudo Town North East Moon Gate")])),
        Chest("Zuna Village Bottom Right House Chest 2", BASE_LOCATION_OFFSET+284, LocationFlag(3,2,2,1), Requirements([[ItemType.pegasus_boots | ItemType.rocs_feather]], keys=[KeyType("Desert of Doubt Gerudo Town North East Moon Gate")])),
        Chest("Zuna Village Top House Chest 1", BASE_LOCATION_OFFSET+285, LocationFlag(3,2,3,7), Requirements([[ItemType.pegasus_boots | ItemType.rocs_feather]], keys=[KeyType("Desert of Doubt Gerudo Town North East Moon Gate")])),
        Chest("Zuna Village Top House Chest 2", BASE_LOCATION_OFFSET+286, LocationFlag(3,2,3,8), Requirements([[ItemType.pegasus_boots | ItemType.rocs_feather]], keys=[KeyType("Desert of Doubt Gerudo Town North East Moon Gate")])),
        Chest("Desert Trap Chest 1", BASE_LOCATION_OFFSET+287, LocationFlag(1,3,0,0), Requirements([[ItemType.pegasus_bootsL2]], keys=[KeyType("Desert of Doubt Gerudo Town North East Moon Gate")])),
        Chest("Desert Trap Chest 2", BASE_LOCATION_OFFSET+288, LocationFlag(1,3,0,1), Requirements([[ItemType.pegasus_bootsL2]], keys=[KeyType("Desert of Doubt Gerudo Town North East Moon Gate")])),
        Chest("Desert Trap Chest 3", BASE_LOCATION_OFFSET+289, LocationFlag(1,3,0,2), Requirements([[ItemType.pegasus_bootsL2]], keys=[KeyType("Desert of Doubt Gerudo Town North East Moon Gate")])),
        Chest("Desert Trap Cave Chest", BASE_LOCATION_OFFSET+290, LocationFlag(1,3,5,0), Requirements([[ItemType.pegasus_bootsL2]], keys=[KeyType("Desert of Doubt Gerudo Town North East Moon Gate")])),
        Chest("Desert Crater Sand Chest", BASE_LOCATION_OFFSET+291, LocationFlag(0,3,5,0), Requirements([[ItemType.pegasus_bootsL2]], keys=[KeyType("Desert of Doubt Gerudo Town North East Moon Gate")])),
        Chest("Desert Crater Hole Chest 1", BASE_LOCATION_OFFSET+292, LocationFlag(0,3,6,0), Requirements([[ItemType.pegasus_bootsL2]], keys=[KeyType("Desert of Doubt Gerudo Town North East Moon Gate")])),
        Chest("Desert Crater Hole Chest 2", BASE_LOCATION_OFFSET+293, LocationFlag(0,3,7,0), Requirements([[ItemType.pegasus_bootsL2]], keys=[KeyType("Desert of Doubt Gerudo Town North East Moon Gate")])),
        Chest("Desert Crater Bomb Cave Chest 1", BASE_LOCATION_OFFSET+294, LocationFlag(0,3,7,2), Requirements([[ItemType.pegasus_bootsL2]], keys=[KeyType("Desert of Doubt Gerudo Town North East Moon Gate")])),
        Chest("Desert Crater Bomb Cave Chest 2", BASE_LOCATION_OFFSET+295, LocationFlag(0,3,7,3), Requirements([[ItemType.pegasus_bootsL2]], keys=[KeyType("Desert of Doubt Gerudo Town North East Moon Gate")])),
    ], [
        Door("Desert of Doubt Gerudo Town North East Moon Gate", 1, DoorType.moon_gate, LocationFlag(2,4,0,22)),
    ], jewel=Jewel("Red Royal Jewel", BASE_LOCATION_OFFSET+495, LocationFlag(0,1,0,18), Requirements([[ItemType.pegasus_bootsL2]], keys=[KeyType("Desert of Doubt Gerudo Town North East Moon Gate")])),
    ),
    
    "Desert Temple": ZfsaRegion("Desert Temple", 61, BASE_LOCATION_OFFSET+296, Requirements([[ItemType.bow]], keys=[KeyType("Desert Temple Progressive Key", 3)]), [
        Key("Right Wing Key", BASE_LOCATION_OFFSET+297, LocationFlag(4,6,0,11), Requirements([[ItemType.magic_hammer]])),#This is a Hammer Bulge
        Key("Laser Room Key", BASE_LOCATION_OFFSET+298, LocationFlag(3,4,1,29), Requirements([[ItemType.bow]], keys=[KeyType("Desert Temple Progressive Key"), KeyType("Desert Temple Laser Room Moon Gate")])),
        Key("Armos Circle Key", BASE_LOCATION_OFFSET+299, LocationFlag(2,3,0,68), Requirements([[ItemType.bow]], keys=[KeyType("Desert Temple Progressive Key", 2)])),
    ], [
        Chest("Laser Room Right Chest", BASE_LOCATION_OFFSET+300, LocationFlag(3,4,0,0), Requirements([[ItemType.bow]], keys=[KeyType("Desert Temple Progressive Key")])),
        Chest("Laser Room Left Chest", BASE_LOCATION_OFFSET+301, LocationFlag(3,4,0,1), Requirements([[ItemType.bow]], keys=[KeyType("Desert Temple Progressive Key")])),
        Chest("Laser Room Center Chest", BASE_LOCATION_OFFSET+302, LocationFlag(3,4,0,4), Requirements([[ItemType.bow]], keys=[KeyType("Desert Temple Progressive Key")])),
        Chest("Eyegore Room Right Chest", BASE_LOCATION_OFFSET+303, LocationFlag(3,3,0,0), Requirements([[ItemType.bow]], keys=[KeyType("Desert Temple Progressive Key")])),
        Chest("Eyegore Room Left Chest", BASE_LOCATION_OFFSET+304, LocationFlag(3,3,0,1), Requirements([[ItemType.bow]], keys=[KeyType("Desert Temple Progressive Key")])),
        Chest("North Switch Room Chest 1", BASE_LOCATION_OFFSET+305, LocationFlag(3,2,0,0), Requirements([[ItemType.bow]], keys=[KeyType("Desert Temple Progressive Key")])),
        Chest("North Switch Room Chest 2", BASE_LOCATION_OFFSET+306, LocationFlag(3,2,0,1), Requirements([[ItemType.bow]], keys=[KeyType("Desert Temple Progressive Key")])),
    ], [
        Door("Desert Temple Progressive Key", 1, DoorType.door, LocationFlag(4,6,0,0)),
        Door("Desert Temple Progressive Key", 2, DoorType.door, LocationFlag(3,4,0,2)),
        Door("Desert Temple Progressive Key", 3, DoorType.door, LocationFlag(2,3,0,0)),
        Door("Desert Temple Laser Room Moon Gate", 1, DoorType.moon_gate, LocationFlag(2,4,0,18)),
    ], parentRegion="Desert of Doubt"),
    
    "Pyramid": ZfsaRegion("Pyramid", 63, BASE_LOCATION_OFFSET+307, Requirements([[ItemType.bombs]], keys=[KeyType("Pyramid South Corridor Key")]), [
        Key("North West Key", BASE_LOCATION_OFFSET+308, LocationFlag(0,4,0,21), Requirements([[ItemType.boomerang | ItemType.bow | ItemType.slingshot]])),
        Key("South East Pearl", BASE_LOCATION_OFFSET+309, LocationFlag(3,5,0,63), Requirements([], keys=[KeyType("Pyramid South Corridor Key"), KeyType("Pyramid South East Key")])),
    ], [
        Chest("South Corridor Chest 1", BASE_LOCATION_OFFSET+310, LocationFlag(1,7,0,0), Requirements()),
        Chest("South Corridor Chest 2", BASE_LOCATION_OFFSET+311, LocationFlag(1,7,0,1), Requirements()),
        Chest("South Corridor Hidden Chest", BASE_LOCATION_OFFSET+312, LocationFlag(1,7,5,9), Requirements()),
        Chest("Small Rooms Top Chest", BASE_LOCATION_OFFSET+313, LocationFlag(1,6,0,0), Requirements([], keys=[KeyType("Pyramid South Corridor Key")])),
        Chest("Small Rooms Bottom Chest", BASE_LOCATION_OFFSET+314, LocationFlag(1,6,0,1), Requirements([], keys=[KeyType("Pyramid South Corridor Key")])),
        Chest("North East Chest 1", BASE_LOCATION_OFFSET+315, LocationFlag(3,4,0,0), Requirements([[ItemType.pegasus_bootsL2]], keys=[KeyType("Pyramid South Corridor Key")])),
        Chest("North East Chest 2", BASE_LOCATION_OFFSET+316, LocationFlag(3,4,0,1), Requirements([[ItemType.pegasus_bootsL2]], keys=[KeyType("Pyramid South Corridor Key")])),
        Chest("Center Moon Gate Center Chest", BASE_LOCATION_OFFSET+317, LocationFlag(2,4,1,3), Requirements([[ItemType.rocs_featherL2, ItemType.pegasus_boots | ItemType.bombs], [ItemType.pegasus_bootsL2]], keys=[KeyType("Pyramid South Corridor Key"), KeyType("Pyramid Center Moon Gate")])),
        Chest("Center Moon Gate Left Chest", BASE_LOCATION_OFFSET+318, LocationFlag(2,4,1,22), Requirements([[ItemType.rocs_feather, ItemType.pegasus_boots | ItemType.bombs], [ItemType.pegasus_bootsL2]], keys=[KeyType("Pyramid South Corridor Key"), KeyType("Pyramid Center Moon Gate")])),
        Chest("Center Moon Gate Right Chest", BASE_LOCATION_OFFSET+319, LocationFlag(2,4,1,28), Requirements([[ItemType.pegasus_bootsL2]], keys=[KeyType("Pyramid South Corridor Key"), KeyType("Pyramid Center Moon Gate")])),
        Chest("Center Room Chest 1", BASE_LOCATION_OFFSET+320, LocationFlag(1,4,0,0), Requirements([[ItemType.rocs_featherL2, ItemType.pegasus_boots | ItemType.bombs], [ItemType.pegasus_bootsL2]], keys=[KeyType("Pyramid South Corridor Key"), KeyType("Pyramid Center Moon Gate")])),
        Chest("Center Room Chest 2", BASE_LOCATION_OFFSET+321, LocationFlag(1,4,0,1), Requirements([[ItemType.rocs_featherL2, ItemType.pegasus_boots | ItemType.bombs], [ItemType.pegasus_bootsL2]], keys=[KeyType("Pyramid South Corridor Key"), KeyType("Pyramid Center Moon Gate")])),
        Chest("Center Room Chest 3", BASE_LOCATION_OFFSET+322, LocationFlag(1,4,0,2), Requirements([[ItemType.rocs_featherL2, ItemType.pegasus_boots | ItemType.bombs], [ItemType.pegasus_bootsL2]], keys=[KeyType("Pyramid South Corridor Key"), KeyType("Pyramid Center Moon Gate")])),
        Chest("Center Room Chest 4", BASE_LOCATION_OFFSET+323, LocationFlag(1,4,0,3), Requirements([[ItemType.rocs_featherL2, ItemType.pegasus_boots | ItemType.bombs], [ItemType.pegasus_bootsL2]], keys=[KeyType("Pyramid South Corridor Key"), KeyType("Pyramid Center Moon Gate")])),
        #Chest("Center Room Big Chest", BASE_LOCATION_OFFSET+324, LocationFlag(1,4,0,4), Requirements([[ItemType.rocs_featherL2, ItemType.pegasus_boots | ItemType.bombs], [ItemType.pegasus_bootsL2]], keys=[KeyType("Pyramid South Corridor Key"), KeyType("Pyramid Center Moon Gate"), KeyType("Pyramid Big Key")])),
        Chest("Center Room Chest 5", BASE_LOCATION_OFFSET+325, LocationFlag(1,4,0,5), Requirements([[ItemType.rocs_featherL2, ItemType.pegasus_boots | ItemType.bombs], [ItemType.pegasus_bootsL2]], keys=[KeyType("Pyramid South Corridor Key"), KeyType("Pyramid Center Moon Gate")])),
        Chest("Center Room Chest 6", BASE_LOCATION_OFFSET+326, LocationFlag(1,4,0,6), Requirements([[ItemType.rocs_featherL2, ItemType.pegasus_boots | ItemType.bombs], [ItemType.pegasus_bootsL2]], keys=[KeyType("Pyramid South Corridor Key"), KeyType("Pyramid Center Moon Gate")])),
        Chest("Center Room Chest 7", BASE_LOCATION_OFFSET+327, LocationFlag(1,4,0,7), Requirements([[ItemType.rocs_featherL2, ItemType.pegasus_boots | ItemType.bombs], [ItemType.pegasus_bootsL2]], keys=[KeyType("Pyramid South Corridor Key"), KeyType("Pyramid Center Moon Gate")])),
        Chest("Center Room Chest 8", BASE_LOCATION_OFFSET+328, LocationFlag(1,4,0,8), Requirements([[ItemType.rocs_featherL2, ItemType.pegasus_boots | ItemType.bombs], [ItemType.pegasus_bootsL2]], keys=[KeyType("Pyramid South Corridor Key"), KeyType("Pyramid Center Moon Gate")])),
        Chest("Center Room Bomb Wall Chest", BASE_LOCATION_OFFSET+329, LocationFlag(1,4,6,0), Requirements([[ItemType.bombs]], keys=[KeyType("Pyramid South Corridor Key")])),
    ], [
        Door("Pyramid South Corridor Key", 1, DoorType.door, LocationFlag(1,7,0,2)),
        Door("Pyramid South East Key", 1, DoorType.door, LocationFlag(2,5,0,0)),
        Door("Pyramid South East Moon Gate", 1, DoorType.moon_gate, LocationFlag(3,5,0,14)),
        Door("Pyramid Center Moon Gate", 1, DoorType.moon_gate, LocationFlag(2,4,0,5)),
        #Door("Pyramid Big Key", 1, DoorType.big_chest, LocationFlag(1,4,0,4)),
    ], parentRegion="Desert Temple"),
    
    
    "Frozen Hyrule": ZfsaRegion("Frozen Hyrule", 70, BASE_LOCATION_OFFSET+330, Requirements([[ItemType.fire_rod]], keys=[KeyType("Frozen Hyrule House West Moon Gate")]), [
        Key("House East Key", BASE_LOCATION_OFFSET+331, LocationFlag(4,6,0,7), Requirements([[ItemType.lamp | ItemType.fire_rod]])),#This is a Snowball
        Key("House East Blue Bracelet", BASE_LOCATION_OFFSET+332, LocationFlag(4,6,0,7), Requirements([[ItemType.pegasus_boots]])),
        Key("West Frozen Lake Pearl", BASE_LOCATION_OFFSET+333, LocationFlag(0,7,0,7), Requirements([[ItemType.lamp | ItemType.fire_rod]], power_bracelet=True)),
        #one more?
    ], [
        #Chest("r4 Chest 1", BASE_LOCATION_OFFSET+334, LocationFlag(2,8,5,0), Requirements()),# not accessable?
        #Chest("r4 Chest 2", BASE_LOCATION_OFFSET+335, LocationFlag(2,8,7,0), Requirements()),# not accessable?
        #Chest("r1 Chest 1", BASE_LOCATION_OFFSET+336, LocationFlag(2,7,5,0), Requirements()),# not accessable?
        #Chest("r1 Chest 2", BASE_LOCATION_OFFSET+337, LocationFlag(2,7,7,0), Requirements()),# not accessable?
        Chest("House South Chest", BASE_LOCATION_OFFSET+338, LocationFlag(3,7,6,7), Requirements()),
        Chest("East Wing Zigzag Chest", BASE_LOCATION_OFFSET+339, LocationFlag(4,4,5,0), Requirements()),
        Chest("House West Chest", BASE_LOCATION_OFFSET+340, LocationFlag(2,6,0,0), Requirements([], keys=[KeyType("Frozen Hyrule House Key")])),
        Chest("House Chest", BASE_LOCATION_OFFSET+341, LocationFlag(3,6,2,3), Requirements([], keys=[KeyType("Frozen Hyrule House Key")])),
        #Chest("House Chest 2", BASE_LOCATION_OFFSET+342, LocationFlag(3,6,2,3), Requirements()),# not accessable?
        #Chest("House Chest 3", BASE_LOCATION_OFFSET+343, LocationFlag(3,6,2,3), Requirements()),# not accessable?
        Chest("House North Chest", BASE_LOCATION_OFFSET+344, LocationFlag(3,5,0,0), Requirements([], power_bracelet=True)),
        Chest("West Frozen Lake Chest 1", BASE_LOCATION_OFFSET+345, LocationFlag(0,7,5,0), Requirements([[ItemType.lamp | ItemType.fire_rod, ItemType.bombs]], power_bracelet=True)),
        Chest("West Frozen Lake Chest 2", BASE_LOCATION_OFFSET+346, LocationFlag(0,7,5,1), Requirements([[ItemType.lamp | ItemType.fire_rod, ItemType.bombs]], power_bracelet=True)),
        Chest("West Wing Chest", BASE_LOCATION_OFFSET+347, LocationFlag(1,6,0,0), Requirements([[ItemType.fire_rod]], power_bracelet=True)),
        #Chest("r29 Chest", BASE_LOCATION_OFFSET+348, LocationFlag(2,6,0,0), Requirements()),# not accessable?
        #Chest("r29 Cave Chest 1", BASE_LOCATION_OFFSET+349, LocationFlag(2,6,0,0), Requirements()),# not accessable?
        #Chest("r29 Cave Chest 2", BASE_LOCATION_OFFSET+350, LocationFlag(2,6,0,0), Requirements()),# not accessable?
        #Chest("r29 Cave Chest 3", BASE_LOCATION_OFFSET+351, LocationFlag(2,6,0,0), Requirements()),# not accessable?
        #Chest("r29 Cave Chest 4", BASE_LOCATION_OFFSET+352, LocationFlag(2,6,0,0), Requirements()),# not accessable?
    ], [
        Door("Frozen Hyrule House Key", 1, DoorType.door, LocationFlag(3,6,0,0)),
        Door("Frozen Hyrule House West Moon Gate", 1, DoorType.moon_gate, LocationFlag(2,6,0,21)),
    ], jewel=Jewel("Purple Royal Jewel", BASE_LOCATION_OFFSET+496, LocationFlag(2,1,0,18), Requirements([[ItemType.fire_rod]], keys=[KeyType("Frozen Hyrule House West Moon Gate")])),
    ),
    
    "The Ice Temple": ZfsaRegion("The Ice Temple", 71, BASE_LOCATION_OFFSET+353, Requirements([[ItemType.fire_rodL2]], keys=[KeyType("The Ice Temple Progressive Key", 4)], jewels=True), [], [
        Chest("Entrance Chest", BASE_LOCATION_OFFSET+354, LocationFlag(5,9,0,1), Requirements()),
        Chest("Bomb Break Puzzle Chest", BASE_LOCATION_OFFSET+355, LocationFlag(6,6,6,0), Requirements([], keys=[KeyType("The Ice Temple Progressive Key")])),
        Chest("T Split Center Chest", BASE_LOCATION_OFFSET+356, LocationFlag(5,6,5,0), Requirements([[ItemType.lamp | ItemType.fire_rod]], keys=[KeyType("The Ice Temple Progressive Key")])),
        Chest("T Split Left Chest", BASE_LOCATION_OFFSET+357, LocationFlag(5,6,5,1), Requirements([[ItemType.lamp | ItemType.fire_rod]], keys=[KeyType("The Ice Temple Progressive Key")])),
        Chest("T Split Right Chest", BASE_LOCATION_OFFSET+358, LocationFlag(5,6,5,2), Requirements([[ItemType.lamp | ItemType.fire_rod]], keys=[KeyType("The Ice Temple Progressive Key")])),
        Chest("Void Zigzag Chest", BASE_LOCATION_OFFSET+359, LocationFlag(4,6,0,0), Requirements([[ItemType.lamp | ItemType.fire_rod]], keys=[KeyType("The Ice Temple Progressive Key")])),
        Chest("Ice Wall Room Chest 1", BASE_LOCATION_OFFSET+360, LocationFlag(2,6,0,0), Requirements([[ItemType.fire_rod]], keys=[KeyType("The Ice Temple Progressive Key", 2)])),
        Chest("Ice Wall Room Chest 2", BASE_LOCATION_OFFSET+361, LocationFlag(2,6,0,1), Requirements([[ItemType.lamp | ItemType.fire_rod | ItemType.pegasus_bootsL2 | ItemType.rocs_featherL2]], keys=[KeyType("The Ice Temple Progressive Key", 2)])),
        Chest("Bomb Slide Puzzle Chest 1", BASE_LOCATION_OFFSET+362, LocationFlag(3,3,0,0), Requirements([[ItemType.lamp | ItemType.fire_rod]], keys=[KeyType("The Ice Temple Progressive Key", 2)])),
        Chest("Bomb Slide Puzzle Chest 2", BASE_LOCATION_OFFSET+363, LocationFlag(3,3,0,1), Requirements([[ItemType.lamp | ItemType.fire_rod]], keys=[KeyType("The Ice Temple Progressive Key", 2)])),
        Chest("Block Puzzle Chest", BASE_LOCATION_OFFSET+364, LocationFlag(0,3,0,0), Requirements([[ItemType.lamp | ItemType.fire_rod]], keys=[KeyType("The Ice Temple Progressive Key", 2)])),
        Chest("Fairy Room Chest", BASE_LOCATION_OFFSET+365, LocationFlag(1,3,5,0), Requirements([[ItemType.lamp | ItemType.fire_rod]], keys=[KeyType("The Ice Temple Progressive Key", 2)])),
        Chest("Somaria Void Room East Chest 1", BASE_LOCATION_OFFSET+366, LocationFlag(3,2,0,0), Requirements([[ItemType.lamp | ItemType.fire_rod, ItemType.pegasus_bootsL2 | ItemType.fire_rodL2 | ItemType.rocs_featherL2]], keys=[KeyType("The Ice Temple Progressive Key", 3)])),
        Chest("Somaria Void Room East Chest 2", BASE_LOCATION_OFFSET+367, LocationFlag(3,2,0,1), Requirements([[ItemType.lamp | ItemType.fire_rod, ItemType.pegasus_bootsL2 | ItemType.fire_rodL2 | ItemType.rocs_featherL2]], keys=[KeyType("The Ice Temple Progressive Key", 3)])),
        Chest("Somaria Void Room East Chest 3", BASE_LOCATION_OFFSET+368, LocationFlag(3,2,0,2), Requirements([[ItemType.lamp | ItemType.fire_rod, ItemType.pegasus_bootsL2 | ItemType.fire_rodL2 | ItemType.rocs_featherL2]], keys=[KeyType("The Ice Temple Progressive Key", 3)])),
        Chest("Somaria Void Room East Chest 4", BASE_LOCATION_OFFSET+369, LocationFlag(3,2,0,3), Requirements([[ItemType.lamp | ItemType.fire_rod, ItemType.pegasus_bootsL2 | ItemType.fire_rodL2 | ItemType.rocs_featherL2]], keys=[KeyType("The Ice Temple Progressive Key", 3)])),
        Chest("Fire Puzzle Chest 1", BASE_LOCATION_OFFSET+370, LocationFlag(1,2,0,0), Requirements([[ItemType.fire_rodL2]], keys=[KeyType("The Ice Temple Progressive Key", 3)])),
        Chest("Fire Puzzle Chest 2", BASE_LOCATION_OFFSET+371, LocationFlag(1,2,0,1), Requirements([[ItemType.fire_rodL2]], keys=[KeyType("The Ice Temple Progressive Key", 3)])),
    ], [
        Door("The Ice Temple Progressive Key", 1, DoorType.door, LocationFlag(5,9,0,0)),
        Door("The Ice Temple Progressive Key", 2, DoorType.door, LocationFlag(2,6,0,2)),
        Door("The Ice Temple Progressive Key", 3, DoorType.door, LocationFlag(2,3,0,0)),
        Door("The Ice Temple Progressive Key", 4, DoorType.door, LocationFlag(2,5,0,0)),
    ], parentRegion="Frozen Hyrule"),
    
    "Tower of Winds": ZfsaRegion("Tower of Winds", 73, BASE_LOCATION_OFFSET+372, Requirements([[ItemType.lamp | ItemType.fire_rod, ItemType.rocs_feather]], keys=[KeyType("Tower of Winds Progressive Key", 2)], jewels=True, wind_tower=True), [
        Key("4F Key", BASE_LOCATION_OFFSET+373, LocationFlag(3,6,0,27), Requirements([[ItemType.lamp | ItemType.fire_rod, ItemType.rocs_feather]], keys=[KeyType("Tower of Winds Progressive Key")])),
    ], [
        Chest("2F Chest 1", BASE_LOCATION_OFFSET+374, LocationFlag(3,8,7,4), Requirements()),
        Chest("2F Chest 2", BASE_LOCATION_OFFSET+375, LocationFlag(3,8,5,0), Requirements([], keys=[KeyType("Tower of Winds Progressive Key")])),
        Chest("3F Chest", BASE_LOCATION_OFFSET+376, LocationFlag(3,7,0,6), Requirements([[ItemType.lamp | ItemType.fire_rod, ItemType.rocs_feather]], keys=[KeyType("Tower of Winds Progressive Key")])),
        Chest("3F Inside Left Chest", BASE_LOCATION_OFFSET+377, LocationFlag(3,7,6,0), Requirements([[ItemType.lamp | ItemType.fire_rod]], keys=[KeyType("Tower of Winds Progressive Key")])),
        Chest("3F Inside Right Chest", BASE_LOCATION_OFFSET+378, LocationFlag(3,7,6,1), Requirements([[ItemType.lamp | ItemType.fire_rod, ItemType.rocs_feather]], keys=[KeyType("Tower of Winds Progressive Key")])),
        Chest("4F Left Chest", BASE_LOCATION_OFFSET+379, LocationFlag(3,6,5,12), Requirements([[ItemType.lamp | ItemType.fire_rod, ItemType.rocs_feather]], keys=[KeyType("Tower of Winds Progressive Key")])),
        Chest("4F Right Chest", BASE_LOCATION_OFFSET+380, LocationFlag(3,6,5,13), Requirements([[ItemType.lamp | ItemType.fire_rod, ItemType.rocs_feather]], keys=[KeyType("Tower of Winds Progressive Key")])),
        Chest("6F Top Chest 1", BASE_LOCATION_OFFSET+381, LocationFlag(3,4,5,7), Requirements([[ItemType.lamp | ItemType.fire_rod, ItemType.rocs_feather]], keys=[KeyType("Tower of Winds Progressive Key", 2)])),
        Chest("6F Top Chest 2", BASE_LOCATION_OFFSET+382, LocationFlag(3,4,5,8), Requirements([[ItemType.lamp | ItemType.fire_rod, ItemType.rocs_feather]], keys=[KeyType("Tower of Winds Progressive Key", 2)])),
        Chest("6F Bottom Chest", BASE_LOCATION_OFFSET+383, LocationFlag(3,4,7,6), Requirements([[ItemType.lamp | ItemType.fire_rod, ItemType.rocs_feather]], keys=[KeyType("Tower of Winds Progressive Key", 2)])),
        #Chest("8F Chest", BASE_LOCATION_OFFSET+384, LocationFlag(3,2,5,0), Requirements()),# not accessable?
        #Chest("8F Chest 1", BASE_LOCATION_OFFSET+385, LocationFlag(3,2,6,0), Requirements()),# not accessable?
        #Chest("8F Chest 2", BASE_LOCATION_OFFSET+386, LocationFlag(3,2,6,1), Requirements()),# not accessable?
        #Chest("8F Chest 3", BASE_LOCATION_OFFSET+387, LocationFlag(3,2,6,2), Requirements()),# not accessable?
        #Chest("8F Chest 4", BASE_LOCATION_OFFSET+388, LocationFlag(3,2,6,3), Requirements()),# not accessable?
        Chest("Boss Floor Chest", BASE_LOCATION_OFFSET+389, LocationFlag(3,1,5,7), Requirements([[ItemType.lamp | ItemType.fire_rod, ItemType.rocs_feather]], keys=[KeyType("Tower of Winds Progressive Key", 2)])),
    ], [
        Door("Tower of Winds Progressive Key", 1, DoorType.door, LocationFlag(3,8,5,1)),
        Door("Tower of Winds Progressive Key", 2, DoorType.door, LocationFlag(3,6,6,0)),
    ], parentRegion="The Ice Temple"),
    
    
    "Realm of the Heavens": ZfsaRegion("Realm of the Heavens", 80, BASE_LOCATION_OFFSET+390, Requirements([[ItemType.rocs_feather | ItemType.pegasus_bootsL2, ItemType.bombsL2]], keys=[KeyType("Realm of the Heavens East Side Key")]), [
        Key("South East Side Key", BASE_LOCATION_OFFSET+391, LocationFlag(3,5,0,11), Requirements([[ItemType.rocs_feather | ItemType.pegasus_bootsL2, ItemType.magic_hammer]])),#This is a Hammer Bulge
    ], [
        Chest("South West Side Chest 1", BASE_LOCATION_OFFSET+392, LocationFlag(1,5,2,0), Requirements()),
        Chest("South West Side Chest 2", BASE_LOCATION_OFFSET+393, LocationFlag(1,5,2,1), Requirements()),
        Chest("North West Side Chest", BASE_LOCATION_OFFSET+394, LocationFlag(1,3,0,0), Requirements()),
        Chest("North West Side Top Left Chest 1", BASE_LOCATION_OFFSET+395, LocationFlag(1,3,2,0), Requirements()),
        Chest("North West Side Top Left Chest 2", BASE_LOCATION_OFFSET+396, LocationFlag(1,3,2,1), Requirements()),
        Chest("West Moving Clouds Chest", BASE_LOCATION_OFFSET+397, LocationFlag(2,4,0,0), Requirements([[ItemType.rocs_feather | ItemType.pegasus_bootsL2]])),
        Chest("Rainbow Bridges Chest", BASE_LOCATION_OFFSET+398, LocationFlag(6,4,0,0), Requirements([[ItemType.rocs_feather | ItemType.pegasus_bootsL2]], keys=[KeyType("Realm of the Heavens East Side Key")])),
        Chest("Boss Arena Chest 1", BASE_LOCATION_OFFSET+399, LocationFlag(8,3,0,0), Requirements([[ItemType.rocs_feather | ItemType.pegasus_bootsL2, ItemType.bombs]], keys=[KeyType("Realm of the Heavens East Side Key")])),
        Chest("Boss Arena Chest 2", BASE_LOCATION_OFFSET+400, LocationFlag(8,3,0,1), Requirements([[ItemType.rocs_feather | ItemType.pegasus_bootsL2, ItemType.bombs]], keys=[KeyType("Realm of the Heavens East Side Key")])),
        Chest("Boss Arena Chest 3", BASE_LOCATION_OFFSET+401, LocationFlag(8,3,0,2), Requirements([[ItemType.rocs_feather | ItemType.pegasus_bootsL2, ItemType.bombs]], keys=[KeyType("Realm of the Heavens East Side Key")])),
        Chest("Boss Arena Chest 4", BASE_LOCATION_OFFSET+402, LocationFlag(8,3,0,3), Requirements([[ItemType.rocs_feather | ItemType.pegasus_bootsL2, ItemType.bombs]], keys=[KeyType("Realm of the Heavens East Side Key")])),
    ], [
        Door("Realm of the Heavens South West Side Moon Gate", 1, DoorType.moon_gate, LocationFlag(1,5,0,23)),
        Door("Realm of the Heavens East Side Key", 1, DoorType.door, LocationFlag(3,4,0,0)),
    ]),
    
    "The Dark Cloud": ZfsaRegion("The Dark Cloud", 82, BASE_LOCATION_OFFSET+403, Requirements([[ItemType.bow, ItemType.lamp | ItemType.fire_rod | ItemType.rocs_feather | ItemType.pegasus_bootsL2]], jump_pound_side=True, jewels=True, wind_tower=True, zelda=True), [], [
        Chest("2D Entrance Chest", BASE_LOCATION_OFFSET+404, LocationFlag(1,9,2,0), Requirements()),
        Chest("2D Cannons Chest", BASE_LOCATION_OFFSET+405, LocationFlag(3,8,3,2), Requirements([[ItemType.bow]], jump_pound_side=True)),
        Chest("First Battle Chest", BASE_LOCATION_OFFSET+406, LocationFlag(5,8,0,0), Requirements([[ItemType.bow]], jump_pound_side=True)),
        Chest("Mole Maze Right Chest", BASE_LOCATION_OFFSET+407, LocationFlag(5,7,5,7), Requirements([[ItemType.bow, ItemType.magic_hammer]], jump_pound_side=True)),
        Chest("Mole Maze Left Chest", BASE_LOCATION_OFFSET+408, LocationFlag(5,7,5,2), Requirements([[ItemType.bow, ItemType.magic_hammer]], jump_pound_side=True)),
        
        Chest("Windy Room Chest", BASE_LOCATION_OFFSET+409, LocationFlag(6,6,5,5), Requirements([[ItemType.bow, ItemType.magic_hammer]], jump_pound_side=True)),
        #Chest("Treasure Room Big Chest", BASE_LOCATION_OFFSET+410, LocationFlag(4,5,0,0), Requirements([[ItemType.bow, ItemType.magic_hammer]], jump_pound_side=True, keys=[KeyType("The Dark Cloud Big Key")])),
        Chest("Treasure Room Right Chest", BASE_LOCATION_OFFSET+411, LocationFlag(4,5,0,17), Requirements([[ItemType.bow, ItemType.magic_hammer]], jump_pound_side=True)),
        Chest("Treasure Room Chest 1", BASE_LOCATION_OFFSET+412, LocationFlag(4,5,0,1), Requirements([[ItemType.bow, ItemType.magic_hammer]], jump_pound_side=True)),
        Chest("Treasure Room Chest 2", BASE_LOCATION_OFFSET+413, LocationFlag(4,5,0,2), Requirements([[ItemType.bow, ItemType.magic_hammer]], jump_pound_side=True)),
        Chest("Treasure Room Chest 3", BASE_LOCATION_OFFSET+414, LocationFlag(4,5,0,9), Requirements([[ItemType.bow, ItemType.magic_hammer]], jump_pound_side=True)),
        Chest("Treasure Room Chest 4", BASE_LOCATION_OFFSET+415, LocationFlag(4,5,0,10), Requirements([[ItemType.bow, ItemType.magic_hammer]], jump_pound_side=True)),
        Chest("Treasure Room Chest 5", BASE_LOCATION_OFFSET+416, LocationFlag(4,5,0,3), Requirements([[ItemType.bow, ItemType.magic_hammer]], jump_pound_side=True)),
        Chest("Treasure Room Chest 6", BASE_LOCATION_OFFSET+417, LocationFlag(4,5,0,4), Requirements([[ItemType.bow, ItemType.magic_hammer]], jump_pound_side=True)),
        Chest("Treasure Room Chest 7", BASE_LOCATION_OFFSET+418, LocationFlag(4,5,0,11), Requirements([[ItemType.bow, ItemType.magic_hammer]], jump_pound_side=True)),
        Chest("Treasure Room Chest 8", BASE_LOCATION_OFFSET+419, LocationFlag(4,5,0,12), Requirements([[ItemType.bow, ItemType.magic_hammer]], jump_pound_side=True)),
        Chest("Treasure Room Chest 9", BASE_LOCATION_OFFSET+420, LocationFlag(4,5,0,5), Requirements([[ItemType.bow, ItemType.magic_hammer]], jump_pound_side=True)),
        Chest("Treasure Room Chest 10", BASE_LOCATION_OFFSET+421, LocationFlag(4,5,0,6), Requirements([[ItemType.bow, ItemType.magic_hammer]], jump_pound_side=True)),
        Chest("Treasure Room Chest 11", BASE_LOCATION_OFFSET+422, LocationFlag(4,5,0,13), Requirements([[ItemType.bow, ItemType.magic_hammer]], jump_pound_side=True)),
        Chest("Treasure Room Chest 12", BASE_LOCATION_OFFSET+423, LocationFlag(4,5,0,14), Requirements([[ItemType.bow, ItemType.magic_hammer]], jump_pound_side=True)),
        Chest("Treasure Room Chest 13", BASE_LOCATION_OFFSET+424, LocationFlag(4,5,0,7), Requirements([[ItemType.bow, ItemType.magic_hammer]], jump_pound_side=True)),
        Chest("Treasure Room Chest 14", BASE_LOCATION_OFFSET+425, LocationFlag(4,5,0,8), Requirements([[ItemType.bow, ItemType.magic_hammer]], jump_pound_side=True)),
        Chest("Treasure Room Chest 15", BASE_LOCATION_OFFSET+426, LocationFlag(4,5,0,15), Requirements([[ItemType.bow, ItemType.magic_hammer]], jump_pound_side=True)),
        Chest("Treasure Room Chest 16", BASE_LOCATION_OFFSET+427, LocationFlag(4,5,0,16), Requirements([[ItemType.bow, ItemType.magic_hammer]], jump_pound_side=True)),
        Chest("Merge Left Chest", BASE_LOCATION_OFFSET+428, LocationFlag(6,5,0,0), Requirements([[ItemType.bow, ItemType.magic_hammer]], jump_pound_side=True)),
        #need moon pearl to merge
        Chest("Spike Maze South East Chest 1", BASE_LOCATION_OFFSET+429, LocationFlag(8,7,0,0), Requirements([[ItemType.bow, ItemType.magic_hammer | ItemType.pegasus_bootsL2]], jump_pound_side=True)),
        Chest("Spike Maze South East Chest 2", BASE_LOCATION_OFFSET+430, LocationFlag(8,7,0,1), Requirements([[ItemType.bow, ItemType.magic_hammer | ItemType.pegasus_bootsL2]], jump_pound_side=True)),
        Chest("Spike Maze East Chest 1", BASE_LOCATION_OFFSET+431, LocationFlag(8,6,0,0), Requirements([[ItemType.bow, ItemType.magic_hammer | ItemType.pegasus_bootsL2]], jump_pound_side=True)),
        Chest("Spike Maze East Chest 2", BASE_LOCATION_OFFSET+432, LocationFlag(8,6,0,1), Requirements([[ItemType.bow, ItemType.magic_hammer | ItemType.pegasus_bootsL2]], jump_pound_side=True)),
        Chest("Spike Maze East Chest 3", BASE_LOCATION_OFFSET+433, LocationFlag(8,6,0,2), Requirements([[ItemType.bow, ItemType.magic_hammer | ItemType.pegasus_bootsL2]], jump_pound_side=True)),
        Chest("Spike Maze West Chest", BASE_LOCATION_OFFSET+434, LocationFlag(7,6,0,0), Requirements([[ItemType.bow, ItemType.magic_hammer | ItemType.pegasus_bootsL2]], jump_pound_side=True)),
        Chest("Spike Maze North East Chest 1", BASE_LOCATION_OFFSET+435, LocationFlag(8,5,0,0), Requirements([[ItemType.bow, ItemType.magic_hammer | ItemType.pegasus_bootsL2]], jump_pound_side=True)),
        Chest("Spike Maze North East Chest 2", BASE_LOCATION_OFFSET+436, LocationFlag(8,5,0,1), Requirements([[ItemType.bow, ItemType.magic_hammer | ItemType.pegasus_bootsL2]], jump_pound_side=True)),
        Chest("Spike Maze North East Chest 3", BASE_LOCATION_OFFSET+437, LocationFlag(8,5,0,2), Requirements([[ItemType.bow, ItemType.magic_hammer | ItemType.pegasus_bootsL2]], jump_pound_side=True)),
        Chest("Spike Maze North West Chest", BASE_LOCATION_OFFSET+438, LocationFlag(7,5,0,0), Requirements([[ItemType.bow, ItemType.magic_hammer | ItemType.pegasus_bootsL2]], jump_pound_side=True)),
        #merge is free
        Chest("Candle Room Chest 1", BASE_LOCATION_OFFSET+439, LocationFlag(6,3,0,0), Requirements([[ItemType.bow, ItemType.magic_hammer | ItemType.pegasus_bootsL2, ItemType.lamp | ItemType.fire_rod | ItemType.rocs_feather | ItemType.pegasus_bootsL2]], jump_pound_side=True)),
        Chest("Candle Room Chest 2", BASE_LOCATION_OFFSET+440, LocationFlag(6,3,0,1), Requirements([[ItemType.bow, ItemType.magic_hammer | ItemType.pegasus_bootsL2, ItemType.lamp | ItemType.fire_rod | ItemType.rocs_feather | ItemType.pegasus_bootsL2]], jump_pound_side=True)),
    ], [
        Door("The Dark Cloud 3D Moon Gate", 1, DoorType.moon_gate, LocationFlag(5,9,0,43)),
        #Door("The Dark Cloud Big Key", 1, DoorType.big_chest, LocationFlag(4,5,0,0)),
        Door("The Dark Cloud Merge Left Moon Gate", 1, DoorType.door, LocationFlag(6,5,0,7)),
    ], parentRegion="Realm of the Heavens"),
    
    "Palace of Winds": ZfsaRegion("Palace of Winds", 83, BASE_LOCATION_OFFSET+441, Requirements([[ItemType.rocs_feather, ItemType.bow]], keys=[KeyType("Palace of Winds Progressive Moon Gate", 4), KeyType("Palace of Winds Progressive 2F North Key")], special_palace_of_winds=True, jewels=True, wind_tower=True, zelda=True), [
        Key("2F North Key", BASE_LOCATION_OFFSET+442, LocationFlag(3,5,0,11), Requirements([], keys=4)),
    ], [
        Chest("Entrance Right RNG Chest 1-1", BASE_LOCATION_OFFSET+443, LocationFlag(4,8,0,0), Requirements()),
        Chest("Entrance Right RNG Chest 1-2", BASE_LOCATION_OFFSET+444, LocationFlag(4,8,0,2), Requirements()),
        Chest("Entrance Right RNG Chest 1-3", BASE_LOCATION_OFFSET+445, LocationFlag(4,8,0,4), Requirements()),
        Chest("Entrance Right RNG Chest 1-4", BASE_LOCATION_OFFSET+446, LocationFlag(4,8,0,6), Requirements()),
        Chest("Entrance Right RNG Chest 2-1", BASE_LOCATION_OFFSET+447, LocationFlag(4,8,0,1), Requirements()),
        Chest("Entrance Right RNG Chest 2-2", BASE_LOCATION_OFFSET+448, LocationFlag(4,8,0,3), Requirements()),
        Chest("Entrance Right RNG Chest 2-3", BASE_LOCATION_OFFSET+449, LocationFlag(4,8,0,5), Requirements()),
        Chest("Entrance Right RNG Chest 2-4", BASE_LOCATION_OFFSET+450, LocationFlag(4,8,0,7), Requirements()),
        Chest("Entrance Right RNG Chest 3-1", BASE_LOCATION_OFFSET+451, LocationFlag(4,8,0,8), Requirements()),
        Chest("Entrance Right RNG Chest 3-2", BASE_LOCATION_OFFSET+452, LocationFlag(4,8,0,10), Requirements()),
        Chest("Entrance Right RNG Chest 3-3", BASE_LOCATION_OFFSET+453, LocationFlag(4,8,0,12), Requirements()),
        Chest("Entrance Right RNG Chest 3-4", BASE_LOCATION_OFFSET+454, LocationFlag(4,8,0,14), Requirements()),
        Chest("Entrance Right RNG Chest 4-1", BASE_LOCATION_OFFSET+455, LocationFlag(4,8,0,9), Requirements()),
        Chest("Entrance Right RNG Chest 4-2", BASE_LOCATION_OFFSET+456, LocationFlag(4,8,0,11), Requirements()),
        Chest("Entrance Right RNG Chest 4-3", BASE_LOCATION_OFFSET+457, LocationFlag(4,8,0,13), Requirements()),
        Chest("Entrance Right RNG Chest 4-4", BASE_LOCATION_OFFSET+458, LocationFlag(4,8,0,15), Requirements()),
        Chest("2F East Chest", BASE_LOCATION_OFFSET+459, LocationFlag(4,6,0,6), Requirements()),
        Chest("2F South East Chest", BASE_LOCATION_OFFSET+460, LocationFlag(4,7,0,2), Requirements([[ItemType.magic_hammer]])),
        Chest("2F South East Inside Top Chest", BASE_LOCATION_OFFSET+461, LocationFlag(4,7,2,0), Requirements([[ItemType.magic_hammer]])),
        Chest("2F South East Inside Bottom Chest", BASE_LOCATION_OFFSET+462, LocationFlag(4,7,2,1), Requirements([[ItemType.magic_hammer]])),
        Chest("2F North East Center Chest 1", BASE_LOCATION_OFFSET+463, LocationFlag(4,5,0,0), Requirements([[ItemType.pegasus_bootsL2 | ItemType.rocs_featherL2]], keys=[KeyType("Palace of Winds 2F East Key")])),
        Chest("2F North East Center Chest 2", BASE_LOCATION_OFFSET+464, LocationFlag(4,5,0,7), Requirements([[ItemType.pegasus_bootsL2 | ItemType.rocs_featherL2]], keys=[KeyType("Palace of Winds 2F East Key")])),
        Chest("2F North East Left Chest 1", BASE_LOCATION_OFFSET+465, LocationFlag(4,5,0,1), Requirements([[ItemType.pegasus_bootsL2 | ItemType.rocs_featherL2]], keys=[KeyType("Palace of Winds 2F East Key")])),
        Chest("2F North East Left Chest 2", BASE_LOCATION_OFFSET+466, LocationFlag(4,5,0,2), Requirements([[ItemType.pegasus_bootsL2 | ItemType.rocs_featherL2]], keys=[KeyType("Palace of Winds 2F East Key")])),
        Chest("2F North East Right Chest 1", BASE_LOCATION_OFFSET+467, LocationFlag(4,5,0,3), Requirements([[ItemType.pegasus_bootsL2]], keys=[KeyType("Palace of Winds 2F East Key")])),
        Chest("2F North East Right Chest 2", BASE_LOCATION_OFFSET+468, LocationFlag(4,5,0,5), Requirements([[ItemType.pegasus_bootsL2]], keys=[KeyType("Palace of Winds 2F East Key")])),
        Chest("2F North East Underground 1 Chest 1", BASE_LOCATION_OFFSET+469, LocationFlag(4,5,5,0), Requirements([[ItemType.pegasus_bootsL2 | ItemType.rocs_featherL2]], keys=[KeyType("Palace of Winds 2F East Key")])),
        Chest("2F North East Underground 1 Chest 2", BASE_LOCATION_OFFSET+470, LocationFlag(4,5,5,1), Requirements([[ItemType.pegasus_bootsL2 | ItemType.rocs_featherL2]], keys=[KeyType("Palace of Winds 2F East Key")])),
        Chest("2F North East Underground 3 Chest", BASE_LOCATION_OFFSET+471, LocationFlag(4,5,7,0), Requirements([[ItemType.pegasus_bootsL2]], keys=[KeyType("Palace of Winds 2F East Key")])),
        Chest("2F Far West Chest 1", BASE_LOCATION_OFFSET+472, LocationFlag(1,6,2,0), Requirements([[ItemType.boomerang]])),
        Chest("2F Far West Chest 2", BASE_LOCATION_OFFSET+473, LocationFlag(1,6,2,1), Requirements([[ItemType.boomerang]])),
        Chest("2F North West Top Left Chest", BASE_LOCATION_OFFSET+474, LocationFlag(2,5,0,0), Requirements([[ItemType.bow]])),
        Chest("2F North West Top Right Chest", BASE_LOCATION_OFFSET+475, LocationFlag(2,5,0,14), Requirements([[ItemType.bow]])),
        Chest("2F North West Center Chest 1", BASE_LOCATION_OFFSET+476, LocationFlag(2,5,0,3), Requirements([[ItemType.bow]])),
        Chest("2F North West Center Chest 2", BASE_LOCATION_OFFSET+477, LocationFlag(2,5,0,15), Requirements([[ItemType.bow]])),
        Chest("2F Central Top Left Chest", BASE_LOCATION_OFFSET+478, LocationFlag(3,6,1,0), Requirements([], keys=[KeyType("Palace of Winds Progressive Moon Gate")])),# or 1 pearl if they are not progressive
        Chest("2F Central Top Right Chest", BASE_LOCATION_OFFSET+479, LocationFlag(3,6,1,4), Requirements([], keys=[KeyType("Palace of Winds Progressive Moon Gate", 2)])),# or 1 pearl if they are not progressive
        Chest("2F Central Bottom Left Chest", BASE_LOCATION_OFFSET+480, LocationFlag(3,6,1,3), Requirements([], keys=[KeyType("Palace of Winds Progressive Moon Gate", 3)])),# or 1 pearl if they are not progressive
        Chest("2F Central Bottom Right Chest", BASE_LOCATION_OFFSET+481, LocationFlag(3,6,1,7), Requirements([], keys=[KeyType("Palace of Winds Progressive Moon Gate", 4)])),# or 1 pearl if they are not progressive
        Chest("2F North Flip Hole Chest", BASE_LOCATION_OFFSET+482, LocationFlag(4,4,5,0), Requirements([], keys=[KeyType("Palace of Winds Progressive Moon Gate", 4), KeyType("Palace of Winds Progressive 2F North Key")], bowless_gohma=True)),
        Chest("2F North Flip Flip Chest 1", BASE_LOCATION_OFFSET+483, LocationFlag(4,4,6,16), Requirements([[ItemType.magic_hammer | ItemType.rocs_feather]], keys=[KeyType("Palace of Winds Progressive Moon Gate", 4), KeyType("Palace of Winds Progressive 2F North Key")], bowless_gohma=True)),
        Chest("2F North Flip Flip Chest 2", BASE_LOCATION_OFFSET+484, LocationFlag(4,4,6,17), Requirements([[ItemType.magic_hammer | ItemType.rocs_feather]], keys=[KeyType("Palace of Winds Progressive Moon Gate", 4), KeyType("Palace of Winds Progressive 2F North Key")], bowless_gohma=True)),
        # Can be done with key 6 or [ItemType.rocs_feather | ItemType.pegasus_bootsL2, ItemType.bombs]
        Chest("2F North Void Chest", BASE_LOCATION_OFFSET+485, LocationFlag(3,4,2,9), Requirements([], keys=[KeyType("Palace of Winds Progressive Moon Gate", 4), KeyType("Palace of Winds Progressive 2F North Key")], special_palace_of_winds=True)),
        Chest("Descent B3F Chest", BASE_LOCATION_OFFSET+486, LocationFlag(9,4,0,8), Requirements([], keys=[KeyType("Palace of Winds Progressive Moon Gate", 4), KeyType("Palace of Winds Progressive 2F North Key")], special_palace_of_winds=True)),
        Chest("Descent B4F Left Chest", BASE_LOCATION_OFFSET+487, LocationFlag(9,5,0,0), Requirements([], keys=[KeyType("Palace of Winds Progressive Moon Gate", 4), KeyType("Palace of Winds Progressive 2F North Key")], special_palace_of_winds=True)),
        Chest("Descent B4F Right Chest", BASE_LOCATION_OFFSET+488, LocationFlag(9,5,0,1), Requirements([], keys=[KeyType("Palace of Winds Progressive Moon Gate", 4), KeyType("Palace of Winds Progressive 2F North Key")], special_palace_of_winds=True)),
        Chest("Descent B5F Left Chest", BASE_LOCATION_OFFSET+489, LocationFlag(9,6,6,0), Requirements([], keys=[KeyType("Palace of Winds Progressive Moon Gate", 4), KeyType("Palace of Winds Progressive 2F North Key")], special_palace_of_winds=True)),
        Chest("Descent B5F Right Chest 1", BASE_LOCATION_OFFSET+490, LocationFlag(9,6,6,1), Requirements([[ItemType.rocs_feather]], keys=[KeyType("Palace of Winds Progressive Moon Gate", 4), KeyType("Palace of Winds Progressive 2F North Key")], special_palace_of_winds=True)),
        Chest("Descent B5F Right Chest 2", BASE_LOCATION_OFFSET+491, LocationFlag(9,6,6,6), Requirements([[ItemType.rocs_feather]], keys=[KeyType("Palace of Winds Progressive Moon Gate", 4), KeyType("Palace of Winds Progressive 2F North Key")], special_palace_of_winds=True)),
        Chest("Descent B6F Chest", BASE_LOCATION_OFFSET+492, LocationFlag(9,7,0,0), Requirements([[ItemType.rocs_feather]], keys=[KeyType("Palace of Winds Progressive Moon Gate", 4), KeyType("Palace of Winds Progressive 2F North Key")], special_palace_of_winds=True)),
    ], [
        Door("Palace of Winds Progressive Moon Gate", 1, DoorType.moon_gate, LocationFlag(3,6,0,28)),
        Door("Palace of Winds Progressive Moon Gate", 2, DoorType.moon_gate, LocationFlag(3,6,0,29)),
        Door("Palace of Winds Progressive Moon Gate", 3, DoorType.moon_gate, LocationFlag(3,6,0,32)),
        Door("Palace of Winds Progressive Moon Gate", 4, DoorType.moon_gate, LocationFlag(3,6,0,33)),
        Door("Palace of Winds 2F East Key", 1, DoorType.door, LocationFlag(3,6,0,0)),
        Door("Palace of Winds Progressive 2F North Key", 1, DoorType.door, LocationFlag(3,5,0,0)),
        Door("Palace of Winds Progressive 2F North Key", 2, DoorType.door, LocationFlag(3,4,0,1)),
    ], parentRegion="The Dark Cloud"),
}
