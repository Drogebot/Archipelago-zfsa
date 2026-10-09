# Zelda Four Swords Adventures Multiworld Setup Guide

## Required Software
- [Latest release of Archipelago Multiworld Suite](https://github.com/ArchipelagoMW/Archipelago/releases).
- [Dolphin Gamecube/Wii Emulator](https://dolphin-emu.org/)
- [Latest release of FSAAPPatcher](https://github.com/Drogebot/ZeldaFSA-APPatcher/releases/latest)
- Your **Legally** obtained American ISO file, likely named `Legend of Zelda, The - Four Swords Adventures (USA).iso`

## Setup process
1. Download and install the latest release of Archipelago Multiworld from the link above.

2. Download and install the latest release of Dolphin Emulator from the link above.

3. Download the latest release of FSAAPPatcher from the link above. This will be used to patch your iso file.

4. Download the APWorld from the [releases](https://github.com/Drogebot/archipelago-zfsa/releases/latest) page and place it in your `custom_worlds` folder located in your Archipelago install directory.

5. (Optional) It is recomended to use Universal Tracker (UT) as it can be difficult to figure out what checks are available.

## Create a Config (.yaml) File

### What is a config file and why do I need one?

Your config file contains a set of configuration options which provide the generator with information about how it
should generate your game. Each player of a multiworld will provide their own config file. This setup allows each player
to enjoy an experience customized for their taste, and different players in the same multiworld can all have different
options.

### Where do I get a config file?

Run the ArchipelagoLauncher.exe from your Archipelago install and click `Generate Template Options`.
This will produce a `/Players/Templates` folder in your Archipelago install, which contains default config files for 
every game in your `custom_worlds` folder. You can manually edit the config file using a text editor of your choice.

## Generating a Single-Player Game

1. After modifying your yaml, place it into your Archipelago/player folder
2. Open the Archipelago Launcher and click "Generate". This will create a zip file in Archipelago/output
3. Navigate to the Archipelago website and go to the Host Game page
4. Click upload file and pass it the .zip created in your output folder
5. Click the "Create New Room" link.
6. Run FSAAPPatcher and enter your full file-path to your iso, ex. `C:\Users\Drogebot\...\Games\Legend of Zelda, The - Four Swords Adventures (USA).iso`.
7. Open Dolphin and from Dolphin, open the generated randomized ISO of Four Swords Adventures (Usually located in the same directory as the patch file).
   - Ensure that "Enable CPU Overclock" and "Emulated Memory Size Override" are both off in your Dolphin settings
8. In your Archipelago Launcher run "Zelda Four Swords Adventures Client"
8. In the server page, there will be a port number. Copy this port number into the top of your ZFSAClient. 
   - The field should read `archipelago.gg:<port number>`
9. Once you have loaded into the game, click the `Connect` button at the top of the ZFSAClient. Once it says you are connected you're free to play, choose a brand new file and start playing!
10. You are required to play singleplayer with the GameCube controller.

## Joining a MultiWorld Game

### Setup your randomized ROM

When you join a multiworld game, you will be asked to provide your config file to whoever is hosting. Once that is done,
the host will provide you with a link to the room or the address and port necessary to connect.

### Connect to the client

*Connect as per you would in a single player session* (Follow from step 6 onward). Any time you would need to connect to a new game it is necessary to relaunch the client once your game is back on the File Select Screen.

### Play the game

**Before you start:** It is important that you start from a blank save file in slot 1. Pease backup your save or delete it from Memory Card A `01-G4SE-gc4sword.gci`.
It is also recomended to disable savestates to prevent you from accidentally sending checks.
Remember to be in the File Select screen **BEFORE** connecting in case of starting any new playthroughs as it might send unwanted checks if you connect while in a different save file