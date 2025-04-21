import os
import subprocess
import shutil

## how to run on windows
# cd "C:\Users\meren\Desktop\windot-main"
# python setup.py


# Path to the hosts file
hosts_path = r"C:\Windows\System32\drivers\etc\hosts"

# The line to add to the hosts file
hostname = 'giggl.local'
ip_address = '127.0.0.1'
entry = f"{ip_address} {hostname}\n"

def update_hosts_file():
    try:
        # Check if we have admin privileges, as the hosts file requires admin access
        if not os.access(hosts_path, os.W_OK):
            print("Permission denied. Please run the script as administrator.")
            return
        
        # Open the hosts file and check for the entry
        with open(hosts_path, 'r+') as file:
            content = file.read()

            # Check if the entry already exists
            if hostname not in content:
                # If not, append the new entry to the end of the file
                file.write(entry)
                print(f"Successfully added {hostname} to the hosts file.")
            else:
                print(f"{hostname} is already in the hosts file.")
    except FileNotFoundError:
        print(f"Hosts file not found at {hosts_path}. Make sure you're on a Windows machine.")
    except PermissionError:
        print("Permission denied. Please run the script as administrator.")
    except Exception as e:
        print(f"An error occurred: {e}")

def flush_dns_cache():
    """Flush DNS cache to apply changes immediately"""
    try:
        # subprocess.run("ipconfig /flushdns", check=True, shell=True)
        # Run ipconfig /flushdns using PowerShell
        subprocess.run(['PowerShell.exe', '-Command', 'ipconfig /flushdns'], check=True)
        print("DNS cache flushed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while flushing DNS cache: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def run_cmd(cmd):
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Command failed: {cmd}")
        print(e)

def run_choco_command(command):
    choco_path = shutil.which("choco") or "C:\\ProgramData\\chocolatey\\bin\\choco.exe"
    
    if not os.path.exists(choco_path):
        print("❌ Chocolatey not found. Skipping command:", command)
        return
    
    try:
        subprocess.run(['powershell.exe', choco_path] + command.split(), check=True)
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Chocolatey command failed: {command}")
        print(e)

def clear_recycle_bin():
    try:
        subprocess.run([
            "powershell.exe",
            "-Command",
            "try { Clear-RecycleBin -Force -ErrorAction Stop } catch { Write-Host 'Recycle Bin is already empty or not available.' }"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print("⚠️ Skipped Recycle Bin clean-up:", e)

def install_chocolatey():
    print("\n🍫 Installing Chocolatey...")

    choco_path = shutil.which("choco")
    if not choco_path:
        try:
            run_cmd(r'''PowerShell.exe -NoProfile -ExecutionPolicy Bypass -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"''')
            print("✅ Chocolatey installation initiated. Please wait a moment...")
        except Exception as e:
            print("❌ Chocolatey installation failed:", e)
    else:
        print("✅ Chocolatey is already installed.")

def install_ubuntu_2404():
    try:
        subprocess.run(["wsl", "--install", "-d", "Ubuntu-24.04"], check=True)
        print("✅ Ubuntu 24.04 is being installed.")
    except subprocess.CalledProcessError as e:
        print("❌ Failed to install Ubuntu 24.04:", e)


def install_packages():
    print("\n📦 Installing Desktop Applications and WSL...")

    # Update choco
    run_choco_command("upgrade chocolatey -y")
+
    # Install device drivers
    run_choco_command("install nvidia-display-driver -y")
    run_choco_command("install amd-ryzen-chipset-driver -y")
    run_choco_command("install realtek-hd-audio-driver -y")
    run_choco_command("install intel-chipset-device-software -y")

    # Install Applications
    run_choco_command("install docker-desktop -y")
    run_choco_command("install slack -y")
    run_choco_command("install zwift -y")
    run_choco_command("install brave -y")
    run_choco_command("install wsl2 -y")
    run_choco_command("install vscode -y")
    run_choco_command("install googlechrome -y")
    run_choco_command("install xbox -y")
    run_choco_command("install 7zip -y")
    run_choco_command("install steam -y")
    run_choco_command("install git-y")
    

def main():
    install_chocolatey()
    install_packages()
    update_hosts_file()
    install_ubuntu_2404()
    flush_dns_cache()
    clear_recycle_bin()
    print("\n🎉 Done! Your system is cleaner and has Packages installed.")

if __name__ == "__main__":
    main()
