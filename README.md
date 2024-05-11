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

1. **Prerequisites:** Ensure you have Python installed and the required libraries (run `pip install -r requirements.txt`).
2. **PyInstaller:**  Use PyInstaller to package the script into an executable:
   ```bash
   pyinstaller --onefile auto-updater.py
