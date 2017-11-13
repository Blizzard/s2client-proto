# Protocol

## Connection

The SC2API is a protobuf based protocol that uses websockets as the connection layer.

The address/port of the websocket server is specified on the command line:
> -listen 127.0.0.1 -port 5000

The SC2API can be accessed by connecting to the websocket URL:
> /sc2api

The protocol for the connection is defined in protobuf. [The protocol definition can be found here.](../s2clientprotocol/sc2api.proto)

All communication over the connection is based around **Request** and **Response** messages. Requests are used for controlling the state of the application, retrieving data and controlling gameplay. 

The data sent into the game must be exactly a series of protobuf defined “Request” objects. The data sent back from the game will be exactly a series of protobuf defined “Response” objects, whose type exactly matches the order of incoming “Request” objects.

You are allowed to send additional requests before receiving a response to an earlier request. Requests will be queued and processed in received order. Keeping the request queue saturated is best for optimal performance.

## State Machine

The current state of the application is contained in the **status** field of every response.

The possible states:
* **Launched** - Game has been launch and is not yet doing anything.
* **Init_game** - Create game has been called, and the host is awaiting players.
* **In_game** - In a single or multiplayer game.
* **In_replay** -  In a replay.
* **Ended** - Game or replay has ended, can still request game info, but ready for a new game.
* **Quit** - Application is shutting down.  

The state of the application is modified using requests.

Diagram of common state flow and the requests used to transition between the states:

![alt text](State%20Machine.png "State Machine Diagram")

## Game Speed

The game simulation moves forward with a fixed time step. One unit of time is called a **GameLoop**.

There are two supported options for controlling the game speed:
* **Singlestep Mode**
    * The game simulation only advances once all players issue a Step request.
    * There is no restriction on how fast or slow you can step.
* **Realtime Mode**
    * The game simulation will automatically advance.
    * Uses the “faster” game speed (22.4 gameloops per second).

When in realtime mode, the Step transition in the above diagram will occur automatically.

# Usage

## Process a replay
1. Launch one instance of the SC2 client.
2. Send **RequestStartReplay** with a valid replay.
3. Play the replay to completion:
    1.  Send **RequestObservation** to retrieve snapshot of game state.
    2. Check if response status is Ended.
        * If it is, break out of the loop
    3. Process data in **ResponseObservation**.
    4. If running in single step mode, Send **RequestStep**.
    5. Repeat
4. Send **RequestQuit** to shut down application.

## Play a bot against the built in AI
1. Launch one instance of the SC2 client.
2. Send **RequestCreateGame** with a valid single player map. 
3. Send **RequestJoinGame** with desired player config.
4. Play the map to completion:
    1. Send **RequestObservation** to retrieve game state.
    2. Check if response status is Ended.
        * If it is, break out of the loop
    3. Run bot logic to process data in **ResponseObservation**.
    4. Send **RequestAction** containing the actions the bot wanted to make.
    5. If running in single step mode, send **RequestStep**.
    6. Repeat.
5. Send **RequestQuit** to shut down application.

## Play two bots against each other
1. Launch two instances of the SC2 client.
2. Choose one of the instances to act as the game host.
3. Send **RequestCreateGame** to the host with a valid multi player map.
4. Send **RequestJoinGame** to both of the clients with the desired player config.
    1. Clients will synchronize between themselves. 
    2. They will send **ResponseJoinGame** when both clients are ready to start playing.
5. Play the map to completion: (Perform steps for both instances)
    1. Send **RequestObservation** to retrieve game state.
    2. Check if response status is Ended.
        * If it is, break out of the loop
    3. Run bot logic to process data in **ResponseObservation**.
    4. Send **RequestAction** containing the actions the bot wanted to make.
    5. If running in single step mode, send **RequestStep**.
        * Clients will synchronize between themselves.
        * They will send **ResponseStep** when both client are ready to continue.
    6. Repeat.
6. Send **RequestLeave** to each instance to ensure they disconnect cleanly.
7. Send **RequestQuit** to each instance shut down application.


# Interfaces

## Overview

Interacting with gameplay is based on an **Observation** and **Action** model. Observations are a snapshot of the current game state. Actions are an operation that controls gameplay.

This pattern is presented in multiple functionally equivalent interfaces. This allows for different types of agents to be able to play the game.

* **Raw Data Interface**
    * Direct access to game state and control of units.
    * Designed for scripted AI and replay analysis.
* **Feature Layer Interface**
    * Simplified image based representation of game state.
    * Designed for Machine Learning based AI.
* **Rendered Interface**
    * Full fidelity rendered image of the game.
    * Designed for advanced Machine Learned based AI.

There are additional interfaces that can be enabled to provide more data:

* **Score Interface**
    * Provides various values for evaluating the performance of a player.
    * Designed for measuring performance of a bot and replay analysis.

Which interfaces are active is set using the “InterfaceOptions” message when you configure a game/replay. You are allowed to have multiple interfaces active at the same time. 

Observations will contain the same game state represented in each of the enabled interfaces.

You are allowed to input actions using any of the enabled interfaces. When playing replays, the same actions will be reported back in each of the enabled interfaces.

## Raw Data

This is designed to be the simplest possible representation of the game.

All user interface concepts like selection and camera movement are removed. The observation contains the state of all units visible to the player. Units are referenced by tag and are issued actions directly.

Protocol relevant to inspecting game state:
* **RequestObservation** - Snapshot of current game state represented as structured data.
* **RequestGameInfo** - Static information about the map.
* **RequestData** - Static information about gameplay elements.

Protocol relevant to controlling units:
* **RequestAction** - Allows direct control of units.
* **RequestQuery** - Provides additional tests for action validation.

All positions are based on game coordinates. The lower left of the map is (0, 0).

## Feature Layer

This is designed to be the simplest representation of human data that can be consumed by a neural network based learning model.

The full set of functionality of the user interface is represented. However, functionally equivalent parts have been simplified. There are many ways for a human to move the camera, but in this interface it has been simplified to a single action.

The only relevent protocol to this interface is **RequestObservation** and **RequestAction**.

The game world and user interface are represented seperately. Both the observation and action have seperate sections for these two components.

All positions are based on screen space coordinates. The upper left of the images are (0, 0).

## Rendered

This exposes the full fidelty rendered frame buffer that a human player sees.

This interface is fully supported on all platforms including Linux. On Linux it supports both hardware and software rendering.

The action interface is very similar to that of feature layers, where the user interface is represented separately.


# General

## Protocol Errors

There are two main types of errors in the protocol:
* Protocol usage errors.
* Errors processing a request.

Which requests are allowed at any given time depends on the current status. For example, you are not allowed to send **RequestSaveReplay** if the current status is Launched as it isn’t in a game. When this occurs, the game will send back an empty Response message with only the error field populated.

Many requests have errors that are specific to that type of request. For example, if you send **RequestCreateGame** with a map path that doesn’t exist. When this type of error occurs, the game will send back a Response message with the appropriate response type populated (eg. **ResponseCreateGame**), but with only the error field populated.

## Action Errors

When you execute an action with **RequestAction**, the protocol will report back any cases where the actions failed. These are equivalent to the red text error messages that appear on the left side of the screen while playing. There are two different places where these may be reported in the protocol.

All actions are validated before they are executed. If an action fails initial validation, it will be reported back immediately in **ResponseAction**. For example, if you try to build a structure but didn’t have enough resources.

Actions can also fail in the process of being executed. For example, if a unit was trying to build a structure at a distant location, but when it arrived there was an enemy unit in the way. These types of late errors are reported back in **ResponseObservation**.

## BattleNet Maps

You can play any BattleNet published map as long as it has already been downloaded.

The game will automatically cache maps locally if they have been played at least once:
* To download all current ladder maps, log in and queue into a ladder match.
* To download any other map, play a custom game on that map.

BattleNet maps are identified by name. If there are multiple versions of the same map downloaded it will launch the newest one.

You can retrieve a listing of what maps are locally cached by using **RequestAvailableMaps**.

## Replays

The game needs all of the original map data in order to play back a replay.

For ladder replays, all the dependencies will be automatially downloaded. ([Not true for linux](linux.md#battlenet-cache))

For offline game replays, the original .SC2Map file must be available to play back the replay. This can cause problems when sharing the replay between machines. The simplest workflow is to always store maps in the standard maps directory. This is done by creating a folder named "Maps" in the game install directory.

The full set of search rules it uses are as follows:

How the path is stored in replays

1. If an override path was provided in the protocol, use that path.
2. If the map path is relative to the standard maps folder, store the relative path into this folder.
3. Otherwise, store the absolute path to the map.

When resolving a path

1. If the map data is provided explicitly, use that and ignore the path in the replay.
2. If an absolute path was stored, check for the map at that exact path.
3. If a relative path was stored, check for the map relative to the standard maps folder.
4. Otherwise, look for map name in the root of the standard maps folder.

## Randomness

The game simulation is completely deterministic when using the same random seed.
When the seed is not fixed, there is slight randomness for mostly cosmetic reasons.

For example, there is a tiny amount of randomness in the delay between Marine shots. This makes it so if you have a large group of marines that all start firing together, their shooting will quickly become out of sync and look less robotic.

The order in which units update is also randomized. This makes it so that if two players issue an attack on the exact same frame, it will be random which one performs the damage first and wins.

## Inaccuracies of Actions

When processing replays, the actions reported may not exactly line up with what occured in the original game.

The protobuf protocol is slightly different than the internal replay format. This can cause slight inaccuracies when converting between these two formats.

For example, feature layers are a top down orthogonal projection where the actual game is an tilted perspective transformation. This means that rectangle selections from the original game may not line up exactly with the reported rectangle selection in feature layer space.

## APM

There are two types:
* **APM**: Actions Per Minute
    * Counts every action performed.
* **EPM**: Effective Actions Per Minute
    * Filters out actions that have no effect.
    
Example:
* You spam back and forth between control groups a bunch of times before issuing a move order.
* For the APM score, every control group recall will be counted.
* For the EPM score, only the last control group recall will be counted.
 
Different action type incur a different ammount of APM "score":
* Command with target = 2
* Command with no target = 1
* Selection action = 1
* Control group action = 1
* Everything else = 0 
 
The in game replay UI exposes this with two different time intervals:
* Average: Average over the entire game so far.
* Current: Average over the last 5 seconds.
 
In the score interface, the value exposed corresponds to the Average APM.


# Game Versions

## Overview

StarCraft II uses a deterministic game simulation. Replays effectively just contain the user input of all players. When you run a replay, it is re-running the full game simulation by playing back the original user input.
 
This means that to play back the replay deterministically, you need to be running on the exact same version that was used in the original game.

The **Patch Version** (eg. "3.17") corresponds to a specific **Binary Version** and **Data Version**. Patches may update these independently, so they both need to be specified to play back a replay correctly. (eg. There may be multiple data versions that use the same binary version)
 
The **Binary Version** is represented by a **Base Build Number**.
* On disk, this number is stored in the folder names inside the "Versions" folder.
* You can have multiple binary versions available inside the same install.
* This is represented by having a different "BaseXXXXX" subfolders.
 
The **Data Version** is represented by a **Version Hash**.
* On disk, this hash stored inside of the ".build.info" file.
* This hash refers to data inside of the SC2Data folder.
* This folder can contain data from multiple versions inside the same install.
* However, you can only have 1 active data version. (The one specified inside the .build.info file)
 
By default, it is assumed you will always run the latest **Binary Version**, and the game will automatically use the **Data Version** from inside the .build.info file. If you want to override the **Data Version** being used, it can be passed in with the "-dataVersion" command line option.

In order to watch an old replay:
1. Launch the correct executable based on the **Base Build Number**.
2. Pass in the **Data Version** on the command line.

## Finding Version Numbers

All the version information for a replay can be queried using the API with **RequestReplayInfo**.
* **Patch Version**: RequestReplayInfo::game_version
* **Binary Version**: RequestReplayInfo::base_build
* **Data Version**: RequestReplayInfo::data_version

We also provide a static listing of previous patch versions here: [versions.json](../buildinfo/versions.json)
* **Patch Version**: label
* **Binary Version**: base-version
* **Data Version**: data-hash

You can also get the version information of the binary itself using **RequestPing**.

## Downloading Data

On Windows/Mac, only the Binary/Data for the latest patch is guarenteed to be downloaded.

The solution to this is to launch the newest version of the game, and request it to download the required old data for you. This is exposed in the API with this field: RequestReplayInfo::download_data

When playing back a replay using the C++ library, this will automatically be handled for you.

On Linux, this feature is not supported, so the packages already include the Binary/Data for all past versions.
