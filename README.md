# Overview

The StarCraft II API is an interface that provides full external control of StarCraft II.

This API exposes functionality for developing software for:
* Scripted bots.
* Machine-learning based bots.
* Replay analysis.
* Tool assisted human play.

The API is available in the retail Windows and Mac clients. There are also Linux clients available at the download links below.

# Contents

* **Protocol**
    * Protobuf protocol definition of the API.
    * [Definition](sc2api.proto)
    * [Documentation](docs/protobuf.md)
* **Reference C++ implementation**
    * Library designed for building a scripted bots using the API.
    * [Repository](https://github.com/Blizzard/s2client-api)
* **StarCraft II Linux Package**
    * Self contained headless linux StarCraft II builds.
    * [Documentation](docs/linux.md)
    * [Download Links](#Linux-Packages)
* **Maps**
    * Maps from the 1v1 ladder and other custom maps.
    * [Download Links](#Map-Packs)
* **Replays**
    * Replay packs of 1v1 ladder games.
    * [Download Links](#Replay-Packs)

# Downloads

## Linux Packages

EULA disclaimer

* [SC2.3.16.1](http://www.github.com)

## Map Packs

EULA disclaimer

* [Ladder 2017 Season 3](http://www.github.com)
* [Melee](http://www.github.com)

## Replay Packs

EULA disclaimer

### SC2.3.16.1
* [Pack 1](http://www.github.com)

# Installing Map and Replay Packs

All additional game data should be extracted within the installation directory.

The default installation directories are:
* Windows: C:\Program Files (x86)\StarCraft II\
* Mac: /Applications/StarCraft II/

On Linux, the installation directory is the folder you extracted the linux package into.

The folder structure is the same accross all platforms. However you may need to create some folders if they are missing.

Standard folder layout:
* StarCraft II/
    * Battle.net/
    * Maps/
    * Replays/
    * SC2Data/
    * Versions/

To install a map pack: 
* Extract the zip file directly into the "Maps" folder.
* A map can be referred to by either an absolute path or its relative path inside the maps folder.
To install a replay pack:
* Replace the "Battle.net" and "Replays" folders with the ones in the zip file.
* A replay must be specified as an absolute path.