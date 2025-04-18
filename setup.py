import os
import subprocess
import shutil


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
    subprocess.run(['powershell.exe', 'choco', command], check=True)

def clean_windows():
    print("\n🧹 Cleaning Windows to save space...")

    # Empty Recycle Bin
    run_cmd('PowerShell.exe -Command "Clear-RecycleBin -Force"')

    # Clean Temp Folders
    temp_dirs = [
        os.environ.get("TEMP", r"C:\Windows\Temp"),
        r"C:\Windows\Temp",
        r"C:\Windows\Prefetch"
    ]
    for dir_path in temp_dirs:
        if os.path.exists(dir_path):
            print(f"Clearing {dir_path}")
            try:
                for root, dirs, files in os.walk(dir_path, topdown=False):
                    for name in files:
                        try:
                            os.remove(os.path.join(root, name))
                        except Exception:
                            pass
                    for name in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, name), ignore_errors=True)
                        except Exception:
                            pass
            except Exception as e:
                print(f"Error cleaning {dir_path}: {e}")

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
    choco_installed = shutil.which("choco") is not None
    if not choco_installed:
        run_cmd(r'''PowerShell.exe -NoProfile -ExecutionPolicy Bypass -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; \
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; \
        iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"''')
    else:
        print("✅ Chocolatey is already installed.")

def install_packages():
    print("\n📦 Installing Desktop Applications and WSL...")

    # Update choco
    run_choco_command("upgrade chocolatey -y")

    # Install Applications
    run_choco_command("install docker-desktop -y")
    run_choco_command("install slack -y")
    run_choco_command("install zwift -y")
    run_choco_command("install brave -y")
    run_choco_command("install wsl2 -y")
    run_choco_command("install vscode -y")

def main():
    install_chocolatey()
    install_packages()
    # clean_windows() # not working
    update_hosts_file()
    flush_dns_cache()
    clear_recycle_bin()
    print("\n🎉 Done! Your system is cleaner and has Packages installed.")

if __name__ == "__main__":
    main()
