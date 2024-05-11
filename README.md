# SPT Auto Updater

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Latest Release](https://img.shields.io/github/v/release/Hounderd/SPT-Auto-Updater)](https://github.com/Hounderd/SPT-Auto-Updater/releases)

This tool simplifies the process of keeping your SPT-Aki (Escape from Tarkov server mod) installation up-to-date. It automatically checks for and downloads updates for the SPT server itself, as well as essential mods like Fika.

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

1. **Download:**  Grab the latest `auto-updater.exe` from the [Releases](https://github.com/YOUR_GITHUB_USERNAME/SPT-Auto-Updater/releases) page.
2. **Place:**  Put the executable in the root directory of your SPT-Aki installation (usually `C:\SPT`).
3. **Run:**  Double-click the executable to launch it.
4. **Check for Updates:**  Click the "Check for Updates" button.
5. **Follow Instructions:** If updates are found, follow the prompts to download and install them.
6. **Launch SPT:** Once updated, use the "Launch SPT" button to start your server.

## Building the Executable from Source

1. **Prerequisites:**
    * **Python 3.x:**  Ensure Python is installed.
    * **Nuitka:** Install Nuitka using `pip install nuitka`.
    * **Dependencies:** Install the required Python packages: `pip install customtkinter requests pefile`.
2. **Clone:** Clone this repository.
3. **Compile:**  From the project directory, run the following command:
   ```bash
   python -m nuitka --onefile --enable-plugin=tk-inter --disable-console --file-reference-choice=runtime auto-updater.py
