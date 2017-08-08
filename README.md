# Overview

The StarCraft II API is an interface that provides full external control of StarCraft II.

This API exposes functionality for developing software for:
* Scripted bots.
* Machine-learning based bots.
* Replay analysis.
* Tool assisted human play.

The API is available in the retail Windows and Mac clients. There are also Linux clients available at the download links below.

# Contents

## Official

* **Protocol**
    * Protobuf protocol definition of the API.
    * [Definition](s2clientprotocol/sc2api.proto)
    * [Documentation](docs/protocol.md)
* **Reference C++ implementation**
    * Library designed for building a scripted bots using the API.
    * [Repository](https://github.com/Blizzard/s2client-api)
* **StarCraft II Linux Packages**
    * Self contained headless linux StarCraft II builds.
    * [Documentation](docs/linux.md)
    * [Download](#linux-packages)
* **Maps**
    * Maps from the 1v1 ladder and other custom maps.
    * [Download](#map-packs)
* **Replays**
    * Replay packs of 1v1 ladder games.
    * [Download](#replay-packs)

## Community

* **PySC2**
   * DeepMind's python environment wrapper. 
   * [Repository](https://github.com/deepmind/pysc2)
* **Command Center**
   * Framework for developing scripted bots.
   * [Repository](https://github.com/davechurchill/CommandCenter)

# Downloads

## Linux Packages

By downloading these additional files, you are agreeing to the [AI AND MACHINE LEARNING LICENSE](DATA_LICENSE).

* [3.16.1](http://blzdistsc2-a.akamaihd.net/Linux/SC2.3.16.1.zip)

## Map Packs

By downloading these additional files, you are agreeing to the [AI AND MACHINE LEARNING LICENSE](DATA_LICENSE).

* [Ladder 2017 Season 1](http://blzdistsc2-a.akamaihd.net/MapPacks/Ladder2017Season1.zip)
* [Ladder 2017 Season 2](http://blzdistsc2-a.akamaihd.net/MapPacks/Ladder2017Season2.zip)
* [Ladder 2017 Season 3](http://blzdistsc2-a.akamaihd.net/MapPacks/Ladder2017Season3.zip)
* [Melee](http://blzdistsc2-a.akamaihd.net/MapPacks/Melee.zip)

## Replay Packs

By downloading these additional files, you are agreeing to the [AI AND MACHINE LEARNING LICENSE](DATA_LICENSE).

* [3.16.1 - Pack 1](http://www.github.com)

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

## Map Packs
* Extract the zip file directly into the "Maps" folder.
* In the API, a map can be specified as either an absolute path or its relative path inside this "Maps" folder.

## Replay Packs
* Replace the "Battle.net" and "Replays" folders with the ones in the zip file.
* In the API, a replay must be specified as an absolute path.
