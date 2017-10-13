## Overview
download_replays.py is for downloading replay packs via Blizzard Game Data APIs.

## Preliminary
1. Create an account for calling the APIs in Blizzard Developer Portal(http://dev.battle.net)
2. Get API key and secret associated with the account
    You can find them in 'My Account' page after logging into the developer portal

## Requirements
The sample script is writting in Python 2.7 and the dependant packages can be installed 
```
pip install -r requirements.txt
```

## How to run
Run download_replays.py with your api key/secret.
```
    python download_replays.py --client-key=<your_key> --client_secret=<your_secret> --s2-client-version=<s2_client_binary_version> --replays-dir=<the directory where to save replay packs>
```
Once the script is run successfully, you may find zipped files under the replays-dir if there's any matching replay packs for the given s2 client version.
To access Starcraft2 replay packs, you must agree to the [AI and Machine Learning License](http://blzdistsc2-a.akamaihd.net/AI_AND_MACHINE_LEARNING_LICENSE.html)
The files are password protected with the password 'iagreetotheeula'.
**By typing in the password ‘iagreetotheeula’ you agree to be bound by the terms of the [AI and Machine Learning License](http://blzdistsc2-a.akamaihd.net/AI_AND_MACHINE_LEARNING_LICENSE.html)**
