# wlSpeaker
Make a speaker wireless with the use of a raspberry Pi or similar

This program is designed to be run on a low-spec computer and hosts a media player that can be accessed through the web browser on any phone or computer that is connected to the same network.

Simply run the program on the desired computer, connect a speaker to the computer's audio output and run main.py. Point any other device on the network to the server machine's ip address and play any spotify playlist of your chosing.

## dependencies
 -Python v3.6+
 
 -VLC 64bit

## Setup

Put Spotify api Client ID and Client Secret in S2Y.py file.

Navigate to directory of "Requirements.txt"

**Linux**

`suo apt install python3-setuptools`

`python3 -m pip install -r Requirements.txt`

**Windows**
`python -m pip install -r Requirements.txt`

## Usage
**Linux** `python3 main.py`

**Windows** `python main.py`
