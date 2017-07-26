# Setup

## Installation
1. Download a data package for the desired game version.
2. Download a binary compatible with that data package.
    * Place the binary in the appropriate "Versions/BaseXXXXX/. (Where XXXXX is the build number)
4. If using to process replays, download the desired replay pack. 
    * Place the contained "Battle.net" folder in the root directory of the data package.
5. If using to play games, download the desired maps package.
    * Place the contents in the "Maps" folder located in the root directory of the data package.
6. Launch the binary with the "listen" and "port" command line.

## Command line options
* **listen**
    * Sets the ip address that the websocket server will listen on.
* **port**
    * Sets the port that the websocket server will listen on.
* **dataDir**
    * Override the path to find the data package.
    * Required if the binary is not in the standard versions folder location. 
    * Defaults to: ../../
* **tempDir**
    * Overrides the directory that temp files are created in.
    * Defaults to: /tmp/
* **verbose**
    * Enables logging of all protocol requests/responses to std::err.

## Bug Reporting

To report bugs with the linux build or protocol, create a new issue on this repo containing the following information:

* Data package version.
* Linux build version.
* Name of map or replay issue occurred on.
* Standard error output of linux binary.
* Description of issue.
* If possible, steps to reproduce the issue.

# General

## Battle.net Cache

The game needs all of the original map data in order to play back a replay.
For ladder replays, the Windows and Mac client will automatically download any missing dependencies if they are missing.
The Linux build however runs in an offline mode, so these dependencies need to be provided manually.

A prepopulated cache is provided for all of the replay packs.
To install the data, copy the "Battle.net" folder into the root directory of the data package.

The same issue occurs for if you want to play on these ladder maps.
For simplicity, the loose .SC2Map files are provided which have no dependencies on the Battle.net cache.
