from dataclasses import dataclass

from Options import Choice, DefaultOnToggle, PerGameCommonOptions, Range, Toggle


class LevelAccess(Choice):
    """If on "vanilla", the main levels are accessed in the way they are in the base game (e.g. Cave of No Return is accessible after beating Lake Hylia).
    If on "tickets", each level has a ticket item that must be acquired to access the level."""
    display_name = "Level Access"
    option_vanilla = 0
    option_tickets = 1
    default = 1


class ShuffleStages(Toggle):
    """Turn off to keep the normal stage order.
    Temple of Ice, Tower of Winds, The Dark Cloud and Palace of Winds remain in their original place."""
    display_name = "Shuffle Stages"
    default = False


class StartingHealth(Range):
    """How many heart pieces you start with.
    This also determines how many heart pieces are added to the item pool."""
    display_name = "Starting Max Health"
    range_start = 1
    range_end = 32
    default = 12


class DeathLink(Toggle):
    """When enabled, deaths are shared with other DeathLink players."""
    display_name = "Death Link"
    default = False


class LampForDark(Toggle):
    """Turning this off requires you to play mostly blind in a few places, like Cave of No Return."""
    display_name = "Require Lamp for Dark"
    default = True


class MinorTricks(Toggle):
    """Turning this on requires you to use some unintuitive tricks.
    Like killing Gohma's by throwing links, or using link regroups to teleport objects."""
    display_name = "Require Minor Tricks"
    default = False


@dataclass
class ZfsaOptions(PerGameCommonOptions):
    level_access: LevelAccess
    shuffle_stages: ShuffleStages
    starting_health: StartingHealth
    death_link: DeathLink
    lamp_for_dark: LampForDark
    minor_tricks: MinorTricks
