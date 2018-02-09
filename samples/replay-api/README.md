## Overview
`download_replays.py` may be used to download replay packs (aggregated into zip files) via Blizzard Game Data APIs.

## Preliminary Setup
1. Create an account for calling the APIs in the [Blizzard Developer Portal](https://dev.battle.net).
2. Get API key and secret associated with the account.
    1. You can find them under the 'My Account' page after logging into the developer portal.

## Requirements
The script is written in Python. Dependant packages can be installed via:
```
pip install -r requirements.txt
```

## How to run
Run `download_replays.py` providing:  

1. API client key `<key>`
2. API client secret `<secret>`
3. StarCraft II client version `<version>`
    1. **Replays are version dependent**. Ensure the version you request is consistent with the build environment in which you intend to utilize them.  
    2. A version list can be found in [/buildinfo/versions.json](https://github.com/Blizzard/s2client-proto/blob/master/buildinfo/versions.json).  
4. Local Replay directory for storing the replays. `<directory>`
5. Optionally add `--extract` to unzip them to the replay directory.

```
python download_replays.py --key=<key> --secret=<secret> --version=<version> --replays_dir=<directory> [--extract]
```
Once the script is run successfully, any matching replay packs will be downloaded to the directory provided.

To access StarCraft II replay packs, you must agree to the [AI and Machine Learning License](https://blzdistsc2-a.akamaihd.net/AI_AND_MACHINE_LEARNING_LICENSE.html)  
The files are password protected with the password 'iagreetotheeula'.  
**By typing in the password ‘iagreetotheeula’ you agree to be bound by the terms of the [AI and Machine Learning License](https://blzdistsc2-a.akamaihd.net/AI_AND_MACHINE_LEARNING_LICENSE.html)**
