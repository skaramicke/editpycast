# editpycast
Automatic podcast audio editing in Python

## Disclaimer
This setup is optimized for those who record multi track talk podcasts with mumble, or what ever software you might use that creates one .wav file for each member.

## Getting started
1. Run `pip install -r requirements.txt` or how ever you usually do such things.
2. Copy `config.example.yaml` to `config.yaml` and read the example carefully when making your changes.

## Process (cron is a good idea)
1. Put your wav(!) files in a folder.
2. Name the folder what you want the mp3 name to be.
3. Put the folder in the directory you specified as `input` in `config.yaml`
4. Run `python main.py`
5. ???
6. Upload mp3 to your podcast hosting service of choice.

Good luck!

Please contribute!
