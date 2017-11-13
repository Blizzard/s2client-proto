# Setup

## Installation
1. [Download](../README.md#linux-packages) a data package for the desired game version.
2. Unzip the package directly into your home folder.
3. [Download](../README.md#downloads) and [install](../README.md#installing-map-and-replay-packs) the desired map and replay packs.

## Command line options

Required:
* **listen**
    * Sets the ip address that the websocket server will listen on.
* **port**
    * Sets the port that the websocket server will listen on.

Optional:
* **dataDir**
    * Override the path to find the data package.
    * Required if the binary is not in the standard versions folder location. 
    * Defaults to: ../../
* **tempDir**
    * Overrides the directory that temp files are created in.
    * Defaults to: /tmp/
* **verbose**
    * Enables logging of all protocol requests/responses to std::err.
* **eglpath**
    * Sets the path the to harware rendering library.
    * Required for using the rendered interface with hardware rendering
    * Example: /usr/lib/nvidia-384/libEGL.so
* **osmesapath**
    * Sets the path the to software rendering library.
    * Required for using the rendered interface with software rendering
    * Example: /usr/lib/x86_64-linux-gnu/libOSMesa.so

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
