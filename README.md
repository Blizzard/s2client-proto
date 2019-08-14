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
    * [Download](#downloads)
* **Maps**
    * Maps from the 1v1 ladder and other custom maps.
    * [Download](#downloads)
* **Replays**
    * Replay packs of 1v1 ladder games.
    * [Download](#downloads)

## Community

* **PySC2**
  * DeepMind's python environment wrapper. 
  * [Repository](https://github.com/deepmind/pysc2)
* **CommandCenter**
  * A robust architecture for quickly developing Starcraft AI bots.
  * [Repository](https://github.com/davechurchill/CommandCenter)
* **Bot Ladder**
  * Unofficial community organized ladder.
  * [Website](http://sc2ai.net/)
* **Community Wiki**
  * Unofficial wiki of documentation and tutorials.
  * [Website](http://wiki.sc2ai.net/Main_Page)
* **Discord Server**
  * Unofficial server for discussing AI questions and projects.
  * [Invite Link](https://discord.gg/BH58ZVt)
* **Facebook Group**
  * Unofficial community page.
  * [Website](https://www.facebook.com/groups/969196249883813/)


# Downloads

To access the linux packages, map packs and replay packs, you must agree to the [AI and Machine Learning License](http://blzdistsc2-a.akamaihd.net/AI_AND_MACHINE_LEARNING_LICENSE.html)

The files are password protected with the password 'iagreetotheeula'.

**By typing in the password ‘iagreetotheeula’ you agree to be bound by the terms of the [AI and Machine Learning License](http://blzdistsc2-a.akamaihd.net/AI_AND_MACHINE_LEARNING_LICENSE.html)**

## Linux Packages

* [3.17](http://blzdistsc2-a.akamaihd.net/Linux/SC2.3.17.zip)
* [3.16.1](http://blzdistsc2-a.akamaihd.net/Linux/SC2.3.16.1.zip)
* [4.0.2](http://blzdistsc2-a.akamaihd.net/Linux/SC2.4.0.2.zip)
* [4.1.2](http://blzdistsc2-a.akamaihd.net/Linux/SC2.4.1.2.60604_2018_05_16.zip)
* [4.6](http://blzdistsc2-a.akamaihd.net/Linux/SC2.4.6.0.67926.zip)
* [4.6.1](http://blzdistsc2-a.akamaihd.net/Linux/SC2.4.6.1.68195.zip)
* [4.6.2](http://blzdistsc2-a.akamaihd.net/Linux/SC2.4.6.2.69232.zip)
* [4.7](http://blzdistsc2-a.akamaihd.net/Linux/SC2.AStar.4.7.zip) 
* [4.7.1](http://blzdistsc2-a.akamaihd.net/Linux/SC2.4.7.1.zip) 
* [4.10](http://blzdistsc2-a.akamaihd.net/Linux/SC2.4.10.zip) 

## Map Packs

* [Ladder 2017 Season 1](http://blzdistsc2-a.akamaihd.net/MapPacks/Ladder2017Season1.zip)
* [Ladder 2017 Season 2](http://blzdistsc2-a.akamaihd.net/MapPacks/Ladder2017Season2.zip)
* [Ladder 2017 Season 3 Updated](http://blzdistsc2-a.akamaihd.net/MapPacks/Ladder2017Season3_Updated.zip)
* [Ladder 2017 Season 4](http://blzdistsc2-a.akamaihd.net/MapPacks/Ladder2017Season4.zip)
* [Ladder 2018 Season 1](http://blzdistsc2-a.akamaihd.net/MapPacks/Ladder2018Season1.zip)
* [Ladder 2018 Season 2](http://blzdistsc2-a.akamaihd.net/MapPacks/Ladder2018Season2_Updated.zip)
* [Ladder 2018 Season 3](http://blzdistsc2-a.akamaihd.net/MapPacks/Ladder2018Season3.zip)
* [Ladder 2018 Season 4](http://blzdistsc2-a.akamaihd.net/MapPacks/Ladder2018Season4.zip)
* [Ladder 2019 Season 1](http://blzdistsc2-a.akamaihd.net/MapPacks/Ladder2019Season1.zip)
* [Ladder 2019 Season 2](http://blzdistsc2-a.akamaihd.net/MapPacks/Ladder2019Season2.zip)
* [Ladder 2019 Season 3](http://blzdistsc2-a.akamaihd.net/MapPacks/Ladder2019Season3.zip)
* [Melee](http://blzdistsc2-a.akamaihd.net/MapPacks/Melee.zip)

This is the previous version of the Ladder 2017 Season 3 Map Pack
* [Ladder 2017 Season 3 Original](http://blzdistsc2-a.akamaihd.net/MapPacks/Ladder2017Season3.zip)

## Replay Packs

* [3.16.1 - Pack 1](http://blzdistsc2-a.akamaihd.net/ReplayPacks/3.16.1-Pack_1-fix.zip)
* [3.16.1 - Pack 2](http://blzdistsc2-a.akamaihd.net/ReplayPacks/3.16.1-Pack_2.zip)

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

## Stable IDs

These define the action mappings from ability ids in the protobuf api to the internals of the game.
They also define some general ids that combine multiple abilities that have a similar semantic meaning
(eg various forms of burrow, cancel, lift/land, etc). The `stableid.json` is updated occasionally with
the game, but can also be updated manually by downloading the `stableid.json` from here and placing it
in the root of your `StarCraft II` directory.
