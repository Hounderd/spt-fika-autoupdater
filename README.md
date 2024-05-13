# SPT Auto Updater

[![License](https://img.shields.io/github/license/Hounderd/SPT-Auto-Updater)](LICENSE)
[![Latest Release](https://img.shields.io/github/v/release/Hounderd/SPT-Auto-Updater)](https://github.com/YOUR_GITHUB_USERNAME/SPT-Auto-Updater/releases)

This tool simplifies the process of keeping your SPT-Aki (Single Player Tarkov) installation up-to-date. It automatically checks for and downloads updates for the SPT server itself, as well as updates for essential coop mods like Fika.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [How to Use the Precompiled Executable](#how-to-use-the-precompiled-executable)
- [Building the Executable from Source](#building-the-executable-from-source)
- [Hosting Your Own `manifest.json`](#hosting-your-own-manifestjson)
- [Contributing](#contributing)
- [License](#license)

## Introduction

SPT-Aki can be tricky to update manually due to the various components and dependencies. This auto updater streamlines the process, ensuring a smooth and hassle-free experience.

## Features
![spt updater screenshot](https://download.nodd.dev/updater-screenshot.png)
- **Automatic Update Checks:**  Regularly checks for new versions of SPT-Aki, Fika, and the updater itself.
- **Guided Update Process:**  Intuitive GUI walks you through the update steps.
- **Customizable:**  Can be configured to use your own manifest file to point to different update sources.
- **Easy to Use:**  Whether you're a beginner or an experienced user, this tool is designed to be simple.

## How to Use the Precompiled Executable

1. **Download:**  Grab the latest `auto-updater.exe` from the [Releases](https://github.com/Hounderd/SPT-Auto-Updater/releases) page.
2. **Place:**  Put the executable in the root directory of your SPT-Aki installation (usually `C:\SPT`).
3. **Check for Updates:**  Run auto-updater.exe and then click the "Check for Updates" button.
4. **Follow Instructions:** If updates are found, follow the prompts to download and install them.
5. **Launch SPT:** Once updated, use the "Launch SPT" button to start the SPT launcher and play the game!

## Building the Executable from Source

Building from source is not fully supported at this time. It is not reccomended to use this auto-updater this way. Please download the auto-updater from the [Releases](https://github.com/Hounderd/SPT-Auto-Updater/releases) page.

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

I believe the PAID version of the nuitka compiler has options to make it so the exe doesnt show up as a virus, but this is a free project that im not making any money off of so im not paying money to compile.

## Hosting Your Own manifest.json

coming soon:tm:

## Contributing

I started this project just to make it easier for my friends and I to update their clients for SPT and Fika. I still have alot of ideas for this project that I will be adding, but anyone is free to fork the codebase for their own needs. If you find any issues, please submit an issue under the github project page. If you would like to contribute feel free to submit a PR and i will review it :)

LETS MAKE TARKOV GREAT AGAIN!
