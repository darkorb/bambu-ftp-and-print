
# Bambu Labs X1* FTP and Print

> [!WARNING]
> This has been archived as of 6th October 2023, due to life things on I do not have time to tinker with this any longer.

This is a Python script that provides a little of the "cloud" like functionality that you lose when you run in LAN Only mode. Namely the ability to send prints from the slicer directly to the printer.

Mostly the way that it manages this is through a combo of MQTT messages and file pulls when a command is picked up by the printer (`pushall`). This script emulates that somewhat but instead makes use of the local FTP server to place the `3mf` file onto the printer and then trigger a print of that file for you.

**:warning: This has been _very_ lightly tested on one printer - mine - with an AMS with it causing no issues so far. I cannot guarantee it will not cause issues for you, I'll assist as much as I can but as many, I work full time. Please open an issue if you have problems but please be polite, and respect that I can't reply instantly in all cases. :warning:**

Raise issues [here](https://github.com/darkorb/bambu-ftp-and-print/issues/new) with as much detail as you can provide.

Supported Platforms;
- macOS (12/13 tested), with Python 3
- Linux, Python 3

Sorry Windows users, I don't have an option for testing this easily right this second but will look into it in a short while.

## Required Information
There are a few options that you will need to configure for this to work and a few small bit's of information you will require.
You will need the following details for your printer(s);

- IP Address. I'd recommend you make this a static reservation or the like.
- LAN Only Password.
- Your Device ID

To get the Device ID you can use a tool such as MQTT explorer to connect to the printer on the non-TLS port of 1883. You'll see messages appearing on the topic that looks like this;
`device/00A00A123456789/report`
The string in the middle is your Device ID - in this case it'd be `00A00A123456789`.

## Installing
Pretty quick to install - hopefully. Just do the following;

    git clone https://github.com/darkorb/bambu-ftp-and-print.git
    cd bambu-ftp-and-print
    pip3 install -r requirements.txt
    cp env.example .env

After this you should be good to configure the required settings.

## Configuring
In the last install step above we copied the example enviroment file to `.env` so now open this up in something like `nano` (or `vi` if you like being mean to yourself ;)) and fill out the required information

    FTP_SERVER = ""
    FTP_PASSWORD = ""
    MQTT_SERVER = ""
    DEV_ID = ""
    DIRECTORY_TO_MONITOR = ""
    UPLOADED_FILES_DIRECTORY = ""
The `FTP_SERVER` and `MQTT_SERVER` will be the same in most cases - which is the IP Address of your printer that you collected in the first step. The only time you'd have these differ is if you are bridging the X1's MQTT to another MQTT (e.g., you have one MQTT server you use for Home Assistant). In this situation you could set these differently but honestly, unless you _really_ need to make them the same. 

Fill out the other details you fetched in the first step and create the folders for the monitoring and processed (uploaded) files. 
## Running

:warning: At this point, you need to strongly consider if you are fine with a random Python script firing commands at your printer. If you are not, stop. Now. If things break/go wrong/your printer eats your house or brings around the end of the world YOU HAVE BEEN WARNED that this is a very untested thing. Bambu could break it at a moments notice. Only continue beyond if you are okay with any potential risks.

Should just be a simple case of doing the following;
``python3 ./monitor_upload.py``
You'll not see any output to start with, so the next step would be to put a file in the folder you created for your `DIRECTORY_TO_MONITOR`. What should happen then is something like the following being outputted to your screen;

    Uploaded the file: CatGhost.3mf
    Moved the file: CatGhost.3mf
    Sent a "Print Start" notification for: CatGhost.3mf
All going well, this should then result in your print starting!
## Notes

If you are using the AMS you the prints will start using the filament slot selected in the slicer. So, if you have slot three selected as the filament for an object or are doing switches (which I've not tested!) it should work fine. 

Keep in mind that purging when switching isn't built into the defaults, so you may want to manually load a color if bleed is going to cause you issues.

There are known things I skipped for easy when doing this such as MD5'ing the `3mf` files and having the printer validate them. This seems like effort for little gain in a local enviroment but if you want to add it go for it.

Also, I'm not a developer. I know the code could probably be better and I welcome constructive feedback, PR's etc. if people want to help out.

## Known Issues

While you probably won't be using it, the image of the object being printed doesn't appear in Bambu Handy.
There is a distinct lack of error checking. If your FTP upload fails, the script will crash. If the MQTT Server explodes, the script will crash.

**Consider this a MVP. As I get spare time, I'll add better handling.**

### Thanks
Quick thanks to the folks in the NZ and AU channels on the official Discord for putting up with my rambling nonsense about this and the prodding I've been doing with MQTT for both this and Home Assistant Intergrations and for those there that have willingly tested stuff I've provided; it's made it much easier :thumbsup:
