from BaseClasses import Location
from .static_logic import ALL_REGIONS


class ZfsaLocation(Location):
    game: str = "The Legend of Zelda: Four Swords Adventures"


ALL_LOCATIONS_TABLE: dict[str, int] = {}

for region_name in ALL_REGIONS:
    region = ALL_REGIONS[region_name]
    #for key in region.keys:
    #    ALL_LOCATIONS_TABLE[f"{region.name} - {key.name}"] = key.id
    for chest in region.chests:
        ALL_LOCATIONS_TABLE[f"{region.name} - {chest.name}"] = chest.id
    
    for pedestal in region.pedestals:
        ALL_LOCATIONS_TABLE[f"{region.name} - {pedestal.name}"] = pedestal.id
    
    if region.jewel is not None:
        ALL_LOCATIONS_TABLE[f"{region.name} - {region.jewel.name}"] = region.jewel.id
    
    if region.name != "Palace of Winds":
        ALL_LOCATIONS_TABLE[f"{region.name} - Stage Clear"] = region.id
