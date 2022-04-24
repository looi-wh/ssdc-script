
# SSDC-BOT
Script to automate purchase in SSDC


## Disclaimer
This script does not have any affliation with SSDC and is not responsible for any issues that arise from using this script. Please use this script at your own risks.
## Features

- Auto login and book slots with minimal user interactions
- Auto recover from failures
- Auto purchase function [experimental]
- Ability to save login details
- Keeps track of how many times you have ran the script for the day
- Designed to work with Windows, Mac os and Linux
- Uses Chrome as one of the script foundation
## Deployment (Windows only)

To make it easier for people to run, there will be a windows script called "run_me_windows.bat" to launch the python script.
Please however note that this batch file will only be available for Windows users only.
```bash
run_me_windows.bat
```
[Notice] Please make sure you have the latest version of Chrome before running the script
## Deployment (For MacOS and Linux)

Please make sure you have the latest version of Python and Chrome installed first

To run this project:

```bash
python3 ssdc_bot.py
```
## Environment Variables

The variables section exists inside the python script itself

`refreshMaxCount = 45` Daily limit before ssdc blocks any future attempts

`timeToSpare = 300` Delay before retrying

`autoPurchase = 0` [experimental, recommended = 0] Auto purchase slot once booking is successful
