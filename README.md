# SPT Auto Updater

[![Latest Release](https://img.shields.io/github/v/release/Hounderd/spt-fika-autoupdater)](https://github.com/Hounderd/spt-fika-autoupdater/releases)

This tool simplifies the process of keeping your SPT-Aki (Single Player Tarkov) installation up-to-date. It automatically checks for and downloads updates for the SPT server itself, as well as updates for essential coop mods like Fika.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [How to Use the Precompiled Executable](#how-to-use-the-precompiled-executable)
- [Building the Executable from Source](#building-the-executable-from-source)
- [Hosting Your Own `manifest.json`](#hosting-your-own-manifestjson)
- [Contributing](#contributing)

## Introduction

SPT-Aki can be tricky to update manually due to the various components and dependencies. This auto updater streamlines the process, ensuring a smooth and hassle-free experience.

## Features
![spt updater screenshot](https://download.nodd.dev/updater-screenshot.png)
- **Automatic Update Checks:**  Checks for new versions of SPT-Aki, Fika, and the updater itself. All with the click of a button!
- **Guided Update Process:**  Intuitive GUI walks you through the update steps.
- **Customizable:**  Can be configured to use your own manifest file to point to different update sources.
- **Easy to Use:**  Whether you're a beginner or an experienced user, this tool is designed to be simple.

## How to Use the Precompiled Executable

1. **Download:**  Grab the latest `auto-updater.exe` from the [Releases](https://github.com/Hounderd/spt-fika-autoupdater/releases) page.
2. **Place:**  Put the executable in the root directory of your SPT-Aki installation (usually `C:\SPT`).
3. **Check for Updates:**  Run auto-updater.exe and then click the "Check for Updates" button.
4. **Follow Instructions:** If updates are found, follow the prompts to download and install them.
5. **Launch SPT:** Once updated, use the "Launch SPT" button to start the SPT launcher and play the game!

## Building the Executable from Source

Building from source is not fully supported at this time. It is not reccomended to use this auto-updater this way. Please download the auto-updater from the [Releases](https://github.com/Hounderd/spt-fika-autoupdater/releases) page.

1. **Prerequisites:**
    * **Python 3.x:**  Ensure Python is installed.
    * **Nuitka:** Install Nuitka using `pip install nuitka`.
    * **Dependencies:** Install the required Python packages: `pip install customtkinter requests pefile`.
2. **Clone:** Clone this repository.
3. **Compile:**  From the project directory, run the following command:
   ```bash
   python -m nuitka --onefile --enable-plugin=tk-inter --disable-console --file-reference-choice=runtime auto-updater.py

## False positive virus warning from the pre-built executable

The pre-built .exe from the releases page will more than likely show up as a virus in windows defender. This is because its compiling a python script that uses functions like copying files, changing directories and other functions that viruses also mimic. This is why i included the code as open-source, and the ability to build your own executable from source. We can see that the source is not malicious, and if you dont trust a pre-built exe, you can build it yourself.

UPDATE: I sent the exe to microsoft as a false malware detection and they actually got back to me pretty quickly and said they didn't find any malware and removed it from the detection algorithm! This is great news as the auto-updater should no longer be falsely flagged as malware. If you still experience these problems, please raise an issue!

## Hosting Your Own manifest.json

coming soon:tm:

## Planned Features

1. Configurable automatic mod updates like SAIN, SWAG+DONUTS etc
2. Ability to backup profiles and mod settings
3. Clean install to latest version or incremental patch to latest version (current default)
4. Ability to rollback to a specific SPT or FIKA version

## Contributing

I started this project just to make it easier for my friends and I to update their clients for SPT and Fika. I still have alot of ideas for this project that I will be adding, but anyone is free to fork the codebase for their own needs. If you find any issues, please submit an issue under the github project page. If you would like to contribute feel free to submit a PR and i will review it :)

LETS MAKE TARKOV GREAT AGAIN!
