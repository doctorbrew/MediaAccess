import subprocess
import time
import sys
import tty

_cachedOutput = "NULL"
lastReturnCode = 0
songFile = "/tmp/currentsong.txt"
exe = "playerctl"
delay = 2
print("Started!  Exit the application using 'q'")


def set_file(file_name, contents):
    file = open(file_name, "w")
    file.write(contents)


def get_status():
    proc = subprocess.run(["playerctl", "-p", "spotify", "status"], shell=False, capture_output=True)
    output = proc.stdout.decode("utf-8").strip('\n')
    global lastReturnCode
    lastReturnCode = proc.returncode
    if lastReturnCode != 0:
        print("[playerctl] Error: " + proc.stderr.decode("utf-8").strip('\n') + " Code: " + str(lastReturnCode))
        return proc.stderr.decode("utf-8").strip('\n')
    return output


def get_metadata(name):
    proc = subprocess.run(["playerctl", "-p", "spotify", "metadata", name], shell=False, capture_output=True)
    output = proc.stdout.decode("utf-8").strip('\n')
    global lastReturnCode
    lastReturnCode = proc.returncode
    if lastReturnCode != 0:
        print("[playerctl] Error: " + proc.stderr.decode("utf-8").strip('\n') + " Code: " + str(lastReturnCode))
        return proc.stderr.decode("utf-8").strip('\n')
    return output


tty.setcbreak(sys.stdin)
while True:
    status = get_status()
    time.sleep(delay)
    if sys.stdin.read(1)[0] == 'q':
        # os.remove(songFile)
        # tty.setraw(sys.stdin)
        exit(0)
    if lastReturnCode != 0:
        set_file(songFile, "Error getting info.")
        continue
    if status == "Paused":
        set_file(songFile, "No media")
        continue
    artist = get_metadata("artist")
    if lastReturnCode != 0:
        set_file(songFile, "Error getting info.")
        continue
    title = get_metadata("title")
    if lastReturnCode != 0:
        set_file(songFile, "Error getting info.")
        continue
    set_file(songFile, "[" + artist + "] " + title)
