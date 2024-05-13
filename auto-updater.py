import customtkinter
import time
import os
import pefile
import requests
import subprocess
import sys
import zipfile
import shutil
import packaging.version

APP_VERSION = "1.0"

current_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
fika_dll_path = os.path.join(current_directory, "BepInEx", "plugins", "Fika.Core.dll")
spt_dll_path = os.path.join(current_directory, "BepInEx", "plugins", "spt", "aki-core.dll")

remote_fika_info = None
remote_spt_info = None

def create_gui():
    global app, status_label, progress_bar, progress_label, check_updates_button, launch_game_button
    global fika_status_label, lfika_status_label, spt_status_label, lspt_status_label
    
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("blue")

    app = customtkinter.CTk()
    app.geometry("470x300")
    app.title(f"SPT Auto Updater v{APP_VERSION}")

    status_label = customtkinter.CTkLabel(app, text="Status: Idle")
    status_label.pack(pady=10)

    progress_bar = customtkinter.CTkProgressBar(app, width=400)
    progress_bar.pack(pady=10)

    progress_label = customtkinter.CTkLabel(app, text="0%")
    progress_label.pack(pady=5)

    button_frame = customtkinter.CTkFrame(app)
    button_frame.pack(pady=20)

    check_updates_button = customtkinter.CTkButton(button_frame, text="Check for Updates")
    check_updates_button.pack(side="left", padx=10)

    launch_game_button = customtkinter.CTkButton(button_frame, text="Launch SPT")
    launch_game_button.pack(pady=10, padx=10)

    info_frame = customtkinter.CTkFrame(app)
    info_frame.pack(side="right", padx=20)

    fika_status_label = customtkinter.CTkLabel(info_frame, text="")
    fika_status_label.pack(side="top")

    lfika_status_label = customtkinter.CTkLabel(info_frame, text="")
    lfika_status_label.pack(side="bottom", padx=10)

    info_frame2 = customtkinter.CTkFrame(app)
    info_frame2.pack(side="left", padx=20)

    spt_status_label = customtkinter.CTkLabel(info_frame2, text="")
    spt_status_label.pack(side="top")

    lspt_status_label = customtkinter.CTkLabel(info_frame2, text="")
    lspt_status_label.pack(side="bottom", padx=10)

    return app

def check_for_updates():
    global app
    if not check_dlls():
        return

    progress_bar.set(0)
    progress_label.configure(text="0%")

    # Remote info fetching
    try:
        gather_update_info_remote()
        progress_bar.set(0.5)
        progress_label.configure(text="50%")
        app.update()
    except requests.exceptions.RequestException as e:
        status_label.configure(text="Status: Error Fetching Remote Manifest!")
        return

    # Local info fetching
    if check_updates_button.cget("text") == "UPDATE":
        status_label.configure(text="Status: Starting update...")
        self_update_download()
        update_fika()
        update_spt()
    else:
        status_label.configure(text="Status: Checking for updates...")
        gather_update_info_local()
        self_update_check()

    progress_bar.set(1)
    progress_label.configure(text="100%")

def get_file_version(dll_path):
    try:
        with pefile.PE(dll_path) as pe:
            for file_info in pe.FileInfo:
                for entry in file_info:
                    if entry.Key.decode() == "StringFileInfo":
                        for string_entry in entry.StringTable:
                            if b"FileVersion" in string_entry.entries:
                                file_version = string_entry.entries[
                                    b"FileVersion"
                                ].decode()
                                return file_version

            return None

    except FileNotFoundError:
        status_label.configure(text=f"Status: Error - {dll_path} not found!", text_color="red")
        return None
    except pefile.PEFormatError:
        status_label.configure(text=f"Status: Error - {dll_path} is corrupt or invalid!", text_color="red")
        return None

def gather_update_info_remote():
    global remote_fika_info, remote_spt_info
    manifest_url = "https://download.nodd.dev/manifest.json"

    try:
        response = requests.get(manifest_url)
        response.raise_for_status()

        manifest_data = response.json()
        remote_fika_version = customtkinter.StringVar()
        remote_spt_version = customtkinter.StringVar()
        remote_spt_info = manifest_data.get("SPT-Version")
        remote_fika_info = manifest_data.get("Fika-Version")

        if remote_spt_version:
            remote_spt_version.set("SPT Version: " + remote_spt_info)
            spt_status_label.configure(textvariable=remote_spt_version)
        else:
            remote_spt_version.set("SPT Version: FOUND NOT")
            spt_status_label.configure(
                textvariable=remote_spt_version, text_color="red"
            )

        if remote_fika_version:
            remote_fika_version.set("Fika Version: " + remote_fika_info)
            fika_status_label.configure(textvariable=remote_fika_version)
        else:
            remote_fika_version.set("Fika Version: FOUND NOT")
            fika_status_label.configure(
                textvariable=remote_fika_version, text_color="red"
            )

    except requests.exceptions.RequestException as e:
        status_label.configure(text="Status: Error Fetching Remote Manifest!")

def gather_update_info_local():
    global remote_fika_info, remote_spt_info

    fika_version_info = get_file_version(fika_dll_path)
    spt_version_info = get_file_version(spt_dll_path)[:-2]  

    # Fika status
    lfika_status_label.configure(
        text="Local Fika Version: " + (fika_version_info or "NOT FOUND"),  
        text_color="green" if fika_version_info == remote_fika_info else "red"  
    )

    # SPT status
    lspt_status_label.configure(
        text="Local SPT Version: " + (spt_version_info or "NOT FOUND"), 
        text_color="green" if spt_version_info == remote_spt_info else "red"
    )

    # Overall update status
    update_required = not all(
        local_ver == remote_ver 
        for local_ver, remote_ver in [
            (fika_version_info, remote_fika_info), 
            (spt_version_info, remote_spt_info)
        ]
        if local_ver is not None  
    )
    
    if update_required:
        update_message = "Status: Update available! ("
        if fika_version_info != remote_fika_info:
            update_message += "Fika "
        if spt_version_info != remote_spt_info:
            update_message += "SPT"
        update_message += ")"
    else:
        update_message = "Status: Up to date!"
    status_label.configure(
        text=update_message,
        text_color="red" if update_required else "green"  
    )

    check_updates_button.configure(
        text="UPDATE" if update_required else "Check for Updates",
        fg_color="orange" if update_required else "#3a7ebf",
    )
    launch_game_button.configure(
        state="normal" if not update_required else "disabled",
        fg_color="orange" if not update_required else "gray",
    )

def check_dlls():
    if not os.path.isfile(fika_dll_path):
        status_label.configure(
            text="Status: Error - Fika core not found!", text_color="red"
        )
        check_updates_button.configure(state="disabled")
        launch_game_button.configure(state="disabled")
        return False

    if not os.path.isfile(spt_dll_path):
        status_label.configure(
            text="Status: Error - SPT core not found!", text_color="red"
        )
        check_updates_button.configure(state="disabled")
        launch_game_button.configure(state="disabled")
        return False

    return True

def launch_spt():
    if not check_dlls():
        return

    status_label.configure(text="Status: Launching SPT...")

    launcher_path = os.path.join(current_directory, "Aki.Launcher.exe")

    try:
        subprocess.Popen(launcher_path)
    except FileNotFoundError:
        status_label.configure(
            text="Status: Aki.Launcher.exe not found!", text_color="red"
        )
        return

    sys.exit(0)

def update_fika():
    global app
    manifest_url = "https://download.nodd.dev/manifest.json"
    response = requests.get(manifest_url)
    response.raise_for_status()
    manifest_data = response.json()
    remote_fika_version = manifest_data.get("Fika-Version")

    if not remote_fika_version:
        status_label.configure(
            text="Status: Remote Fika version not found!", text_color="red"
        )
        return

    download_payload = []
    if remote_fika_version in manifest_data.get("Fika", {}):
        for file_id, file_path in manifest_data["Fika"][remote_fika_version].items():
            download_payload.append(file_path)
    else:
        status_label.configure(
            text="Status: Remote Fika version not found in manifest!", text_color="red"
        )
        return

    download_url = f"https://download.nodd.dev/{remote_fika_version}.zip"

    temp_download_folder = os.path.join(current_directory, "update_temp")
    try:
        os.makedirs(temp_download_folder, exist_ok=True)
    except OSError as e:
        status_label.configure(
            text=f"Status: Error creating temp folder: {e}", text_color="red"
        )
        return

    progress_bar.set(0)
    status_label.configure(text="Status: Downloading update...")

    try:
        with requests.get(download_url, stream=True) as r:
            r.raise_for_status()
            total_size = int(r.headers.get("content-length", 0))
            chunk_size = 8024
            downloaded = 0

            with open(os.path.join(temp_download_folder, "update3.zip"), "wb") as f:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    downloaded += len(chunk)
                    f.write(chunk)
                    progress = downloaded / total_size if total_size != 0 else 0
                    progress_bar.set(progress)
                    progress_label.configure(text=f"{int(progress * 100)}%")
                    app.update()

    except requests.exceptions.RequestException as e:
        status_label.configure(
            text=f"Status: Error downloading update: {e}", text_color="red"
        )
        return
    except IOError as e:
        status_label.configure(
            text=f"Status: Error saving update: {e}", text_color="red"
        )
        return

    try:
        with zipfile.ZipFile(
            os.path.join(temp_download_folder, "update3.zip"), "r"
        ) as zip_ref:
            zip_ref.extractall(temp_download_folder)
    except (IOError, zipfile.BadZipFile) as e:
        status_label.configure(
            text=f"Status: Error extracting update: {e}", text_color="red"
        )
        return

    status_label.configure(text="Status: Applying update...")
    try:
        for file_path in download_payload:
            src_path = os.path.join(temp_download_folder, file_path)
            dst_path = os.path.join(current_directory, file_path)
            shutil.copyfile(src_path, dst_path)
    except (FileNotFoundError, PermissionError, OSError) as e:
        status_label.configure(
            text=f"Status: Error copying files: {e}", text_color="red"
        )
        return

    try:
        shutil.rmtree(temp_download_folder)
    except OSError as e:
        status_label.configure(
            text=f"Status: Error cleaning up temp files: {e}", text_color="red"
        )

    status_label.configure(text="Status: Update Complete!", text_color="green")
    gather_update_info_local()

def update_spt():
    global app
    status_label.configure(text="Status: Starting SPT Update...")

    try:
        spt_version_info = get_file_version(spt_dll_path)[:-2]
        if spt_version_info is None:
            status_label.configure(text="Status: ERROR - Unable to read SPT core", text_color="red")
            return
    except (FileNotFoundError, pefile.PEFormatError) as e:
        status_label.configure(text=f"Status: Error getting SPT version: {e}", text_color="red")
        return

    # Fetch remote SPT version
    manifest_url = "https://download.nodd.dev/manifest.json"
    try:
        response = requests.get(manifest_url)
        response.raise_for_status()  
        manifest_data = response.json()
        remote_spt_version = manifest_data.get("SPT-Version")

        if not remote_spt_version:
            status_label.configure(text="Status: Remote SPT version not found!", text_color="red")
            return
    except requests.exceptions.RequestException as e:
        status_label.configure(text=f"Status: Error fetching manifest: {e}", text_color="red")
        return

    available_versions = [v for v in manifest_data["SPT"].keys()
                         if manifest_data["SPT"][v].get("can_update") in ["yes", "current"]
                         and packaging.version.parse(v) > packaging.version.parse(spt_version_info)]
    available_versions.sort(key=packaging.version.parse)

    if not available_versions:
        status_label.configure(text="Status: SPT is up-to-date!", text_color="green")
        return

    # Install updates incrementally
    for version_to_install in available_versions:
        download_url = f"https://download.nodd.dev/{version_to_install}.zip"
        temp_download_folder = os.path.join(current_directory, "update_temp")

        # Create temp download folder
        try:
            os.makedirs(temp_download_folder, exist_ok=True)
        except OSError as e:
            status_label.configure(text=f"Status: Error creating temp folder: {e}", text_color="red")
            return

        # Download the update (with progress)
        try:
            progress_bar.set(0)
            status_label.configure(text=f"Status: Downloading SPT {version_to_install} update...")

            with requests.get(download_url, stream=True) as r:
                r.raise_for_status()
                total_size = int(r.headers.get("content-length", 0))
                chunk_size = 8024
                downloaded = 0
                with open(os.path.join(temp_download_folder, "update2.zip"), "wb") as f:
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        downloaded += len(chunk)
                        f.write(chunk)
                        progress = downloaded / total_size if total_size != 0 else 0
                        progress_bar.set(progress)
                        progress_label.configure(text=f"{int(progress * 100)}%")
                        app.update()

        except requests.exceptions.RequestException as e:
            status_label.configure(text=f"Status: Error downloading update: {e}", text_color="red")
            return
        except IOError as e:
            status_label.configure(text=f"Status: Error saving update: {e}", text_color="red")
            return

        # Extract update
        try:
            status_label.configure(text="Status: Extracting update...")
            with zipfile.ZipFile(
                os.path.join(temp_download_folder, "update2.zip"), "r"
            ) as zip_ref:
                zip_ref.extractall(temp_download_folder)
        except (IOError, zipfile.BadZipFile) as e:
            status_label.configure(text=f"Status: Error extracting update: {e}", text_color="red")
            return

        # Delete the ZIP file
        zip_file_path = os.path.join(temp_download_folder, "update2.zip")
        try:
            os.remove(zip_file_path)
        except OSError as e:
            status_label.configure(text=f"Status: Error applying update ({e})...")
            return

        # Copy files to the main directory
        status_label.configure(text=f"Status: Applying SPT {version_to_install} update...")
        spt_path = os.path.dirname(sys.argv[0])

        total_size = 0
        for src_dir, dirs, files in os.walk(temp_download_folder):
            for file_ in files:
                src_file = os.path.join(src_dir, file_)
                total_size += os.path.getsize(src_file)

        copied_size = 0
        try:
            for src_dir, dirs, files in os.walk(temp_download_folder):
                dst_dir = src_dir.replace(temp_download_folder, spt_path)
                os.makedirs(dst_dir, exist_ok=True)
                for file_ in files:
                    src_file = os.path.join(src_dir, file_)
                    dst_file = os.path.join(dst_dir, file_)
                    shutil.copyfile(src_file, dst_file)

                    copied_size += os.path.getsize(src_file)
                    progress = copied_size / total_size if total_size != 0 else 0
                    progress_bar.set(progress)
                    progress_label.configure(text=f"{int(progress * 100)}%")
                    app.update()
        except OSError as e:
            status_label.configure(text=f"Status: Error copying files: {e}", text_color="red")
            return
            
        # Step 9: Delete temp files
        try:
            shutil.rmtree(temp_download_folder)
        except OSError as e:
            status_label.configure(text=f"Status: Error cleaning up: {e}", text_color="red")
            return

        # Update UI after each update
        status_label.configure(text=f"Status: SPT {version_to_install} Update Complete!", text_color="green")
        gather_update_info_local()
        
        if manifest_data["SPT"][version_to_install].get("can_update") == "current":
            break

    # Final update of the UI
    status_label.configure(text="Status: SPT Updates Complete!", text_color="green")

def self_update_check():
    status_label.configure(text="Status: Checking updater version...")

    manifest_url = "https://download.nodd.dev/manifest.json"
    try:
        response = requests.get(manifest_url)
        response.raise_for_status()  
        manifest_data = response.json()
        remote_updater_version = manifest_data.get("UPDATER-Version")

        if not remote_updater_version:
            status_label.configure(text="Status: ERROR - Remote updater version not found!", text_color="red")
            return

        if remote_updater_version != APP_VERSION:
            status_label.configure(text="Status: Auto Updater update available!", text_color="orange")
            launch_game_button.configure(state="disabled", fg_color="gray")
            check_updates_button.configure(text="UPDATE", fg_color="orange", command=self_update_download)
        else:
            if status_label.cget("text") == "Status: Checking updater version...": 
                gather_update_info_local()

    except requests.exceptions.RequestException as e:
        status_label.configure(text=f"Status: Error fetching manifest: {e}", text_color="red")

def self_update_download():
    global app
    manifest_url = "https://download.nodd.dev/manifest.json"
    response = requests.get(manifest_url)
    response.raise_for_status()
    manifest_data = response.json()
    remote_updater_version = manifest_data.get("UPDATER-Version")

    if not remote_updater_version:
        status_label.configure(
            text="Status: ERROR - Remote updater version not found!", text_color="red"
        )
        return

    if remote_updater_version == APP_VERSION:
        status_label.configure(
            text="Status: Updater running latest version, no update needed",
            text_color="green",
        )
        return

    download_url = "https://download.nodd.dev/updater.zip"

    temp_download_folder = os.path.join(current_directory, "update_temp")
    os.makedirs(temp_download_folder, exist_ok=True)

    progress_bar.set(0)
    status_label.configure(text="Status: Downloading update...")

    with requests.get(download_url, stream=True) as r:
        r.raise_for_status()
        total_size = int(r.headers.get("content-length", 0))
        chunk_size = 15024
        downloaded = 0
        with open(os.path.join(temp_download_folder, "update1.zip"), "wb") as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                downloaded += len(chunk)
                f.write(chunk)
                progress = downloaded / total_size if total_size != 0 else 0
                progress_bar.set(progress)
                progress_label.configure(text=f"{int(progress * 100)}%")
                app.update()

    status_label.configure(text="Status: Extracting update...")
    with zipfile.ZipFile(
        os.path.join(temp_download_folder, "update1.zip"), "r"
    ) as zip_ref:
        zip_ref.extractall(temp_download_folder)

    zip_file_path = os.path.join(temp_download_folder, "update1.zip")
    try:
        os.remove(zip_file_path)
    except OSError as e:
        status_label.configure(text=f"Status: Error Applying Update ({e})...")

    status_label.configure(text="Status: Applying update...")
    spt_path = os.path.dirname(sys.argv[0])
    shutil.copytree(temp_download_folder, spt_path, dirs_exist_ok=True)

    status_label.configure(text="Status: Cleaning up...")
    shutil.rmtree(temp_download_folder)

    status_label.configure(
        text="Status: Update Complete! RESTARTING IN 5s", text_color="green"
    )
    time.sleep(4)
    start_and_exit()

def start_and_exit():
    original_exe_dir = os.path.dirname(sys.argv[0])
    new_exe_path = os.path.join(original_exe_dir, "auto-updater.exe")

    try:
        subprocess.Popen([new_exe_path])
    except OSError as e:
        status_label.configure(text=f"Status: ERROR - cannot start program: {e}!", text_color="red")

    sys.exit(0)
    
def check_server_availability():
    try:
        response = requests.head("https://download.nodd.dev/manifest.json", timeout=5)
        response.raise_for_status()
        return True
    except requests.RequestException:
        return False

def main():
    global app
    app = create_gui()

    check_updates_button.configure(command=check_for_updates)
    launch_game_button.configure(command=launch_spt)

    if check_server_availability():
        check_for_updates()
    else:
        status_label.configure(text="Status: Error - Update Server unreachable!", text_color="red")
        check_updates_button.configure(state="disabled")
        launch_game_button.configure(state="disabled")

    app.mainloop()

if __name__ == "__main__":
    main()
