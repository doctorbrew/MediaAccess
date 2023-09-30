import os
import subprocess
import time

_cachedOutput = "NULL"
songFile = "/tmp/currentsong.txt"
exe = "playerctl"
delay = 2
print("Started!  Exit the application using 'q'")


def get_error(val):
    if val == "NULL":
        return 1
    elif val == "No players found":
        return 2
    else:
        return 0


def set_file(file_name, contents):
    # print("Setting file: " + contents)
    file = open(file_name, "w")
    file.write(contents)


def get_status():
    proc = subprocess.run(["playerctl", "-p", "spotify", "status"], shell=False, capture_output=True)
    output = proc.stdout.decode("utf-8").strip('\n')
    if proc.returncode != 0:
        print("[playerctl] Error: " + proc.stderr.decode("utf-8").strip('\n') + " Code: " + str(proc.returncode))
        return proc.stderr.decode("utf-8").strip('\n')
    return output


def get_metadata(name):
    # print(os.system("playerctl -p spotify metadata title"))
    proc = subprocess.run(["playerctl", "-p", "spotify", "metadata", name], shell=False, capture_output=True)
    output = proc.stdout.decode("utf-8").strip('\n')
    if proc.returncode != 0:
        print("[playerctl] Error: " + proc.stderr.decode("utf-8").strip('\n') + " Code: " + str(proc.returncode))
        return proc.stderr.decode("utf-8").strip('\n')
    # print(output)
    return output
    # return ""


while True:
    status = get_status()
    time.sleep(delay)
    if status == "Paused":
        set_file(songFile, "Paused")
        continue
    artist = get_metadata("artist")
    if get_error(artist) != 0:
        set_file(songFile, "Error getting info.")
        continue
    title = get_metadata("title")
    if get_error(title) != 0:
        set_file(songFile, "Error getting info.")
        continue
    set_file(songFile, artist + " - " + title)
