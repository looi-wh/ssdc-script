
# SSDC-SCRIPT
Script to automate purchase in SSDC

Script is still in testing phrase and is likely to crash during the initiation process. If so, just restart the script and it will run as normal.


## Disclaimer
This script does not have any affliation with SSDC and is not responsible for any issues that arise from using this script. Please use this script at your own risks.
## Features

- Auto login and book slots with minimal user interactions
- Auto recover from failures
- Auto purchase function [experimental]
- Ability to save login details
- Keeps track of how many times you have ran the script for the day (limitations of ssdc)
- Designed to work with Windows, Mac os and Linux
- Uses Chrome as one of the script foundation
## Deployment (Windows only)

To make it easier for people to run, there will be a windows script called "run_me_windows.bat" to launch the python script.
Please however note that this batch file will only be available for Windows users only.

- Download the latest release from the releases section of this repository first

- Then run the file below like how you would run a normal software
```bash
run_me.bat
```
[Notice] Please make sure you have the latest version of Chrome before running the script!
## Deployment (For MacOS and Linux)
- Please make sure you have the latest version of Python3 and Chrome installed first

- Download the latest release from the releases section of this repository

Then run this project with the code below in any terminal:

```bash
python3 ssdc_script.py
```
## Environment Variables

The variables section exists inside the python script itself

`refreshMaxCount = 45` Daily limit before ssdc blocks any future attempts

`timeToSpare = 300` Delay before retrying

`autoPurchase = 0` [experimental, recommended = 0] Auto purchase slot once booking is successful

## Debugging

If you met some errors with pickle, please delete configs.p in the local directory and try the script again. This is a known issue and will be fixed in future updates.
## What is planned for this script ahead

- Stability testings (This script is still quite new and likely to be extremely unstable)

- Add bookings for TP simulator slots (Not anytime soon)

- Add support for Telegram booking (definitely not fighting against some clowns. This kind of services should be free and not chargable)
