import subprocess
import os
from tkinter import Tk, filedialog, Label, Button, Checkbutton, IntVar, messagebox
import tkinter.ttk as ttk
import ctypes
import sys

def run_as_admin():
    if ctypes.windll.shell32.IsUserAnAdmin() == 0:
        # If not running as admin, relaunch the script with admin privileges
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

# Call this function at the beginning of your script
run_as_admin()

# Global variable to store subprocesses
sub_processes = []

def get_number_of_cores():
    return int(subprocess.check_output(["powershell", "(Get-WmiObject -Class Win32_Processor).NumberOfLogicalProcessors"]).decode().strip())

def convert_dec_to_hex(decimal):
    return hex(decimal)

def select_game_file():
    root = Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(title="Select the game executable file")
    return file_path

def apply_priority(game_exe, enable_priority):
    if enable_priority:
        # Extracting just the executable name from the full path
        game_name = os.path.basename(game_exe)
        # Create registry key for setting high priority
        subprocess.run(["reg", "add", r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\%s\PerfOptions" % game_name, "/v", "IoPriority", "/t", "REG_DWORD", "/d", "3", "/f"], shell=True, check=True)
        subprocess.run(["reg", "add", r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\%s\PerfOptions" % game_name, "/v", "CpuPriorityClass", "/t", "REG_DWORD", "/d", "3", "/f"], shell=True, check=True)
        messagebox.showinfo("Success", "High priority added to registry for %s" % game_name)
    else:
        if game_exe:  # Check if a game executable is provided
            # Revert changes by deleting registry key
            try:
                game_name = os.path.basename(game_exe)
                subprocess.run(["reg", "delete", r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\%s\PerfOptions" % game_name, "/v", "IoPriority", "/f"], shell=True, check=True)
                subprocess.run(["reg", "delete", r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\%s\PerfOptions" % game_name, "/v", "CpuPriorityClass", "/f"], shell=True, check=True)
                messagebox.showinfo("Success", "High priority registry settings reverted for %s" % game_name)
            except subprocess.CalledProcessError:
                messagebox.showerror("Error", "Failed to revert registry settings. Registry does not exist.")

def apply_FSE(game_path, enable_FSE):
    if enable_FSE:
        # Extracting directory and filename from the game path
        game_dir, game_exe = os.path.split(game_path)
        # Construct the registry key string with backslashes and without quotation marks
        registry_key = game_path.replace("/", "\\")
        # Create registry key for FSE with the full path to the executable
        subprocess.run(["reg", "add", r"HKCU\SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers", "/v", registry_key, "/t", "REG_SZ", "/d", "~ DISABLEDXMAXIMIZEDWINDOWEDMODE HIGHDPIAWARE", "/f"], shell=True, check=True)
        messagebox.showinfo("Success", "FSE added to registry for %s" % game_exe)
    else:
        messagebox.showinfo("Info", "FSE is not enabled.")

def apply_DSCP(game_path, enable_DSCP):
    if enable_DSCP:
        # Extracting directory and filename from the game path
        game_dir, game_exe = os.path.split(game_path)
        game_name, _ = os.path.splitext(os.path.basename(game_exe))  # Extracting just the executable name from the full path
        
        # Construct the registry key string with backslashes and without quotation marks
        registry_key = os.path.join("HKEY_LOCAL_MACHINE", "Software", "Policies", "Microsoft", "Windows", "QoS", game_exe)

        # Create registry keys for DSCP settings
        subprocess.run(["reg", "add", registry_key, "/v", "Application Name", "/t", "REG_SZ", "/d", game_exe, "/f"], shell=True, check=True)
        subprocess.run(["reg", "add", registry_key, "/v", "Version", "/t", "REG_SZ", "/d", "1.0", "/f"], shell=True, check=True)
        subprocess.run(["reg", "add", registry_key, "/v", "Protocol", "/t", "REG_SZ", "/d", "*", "/f"], shell=True, check=True)
        subprocess.run(["reg", "add", registry_key, "/v", "Local Port", "/t", "REG_SZ", "/d", "*", "/f"], shell=True, check=True)
        subprocess.run(["reg", "add", registry_key, "/v", "Local IP", "/t", "REG_SZ", "/d", "*", "/f"], shell=True, check=True)
        subprocess.run(["reg", "add", registry_key, "/v", "Local IP Prefix Length", "/t", "REG_SZ", "/d", "*", "/f"], shell=True, check=True)
        subprocess.run(["reg", "add", registry_key, "/v", "Remote Port", "/t", "REG_SZ", "/d", "*", "/f"], shell=True, check=True)
        subprocess.run(["reg", "add", registry_key, "/v", "Remote IP", "/t", "REG_SZ", "/d", "*", "/f"], shell=True, check=True)
        subprocess.run(["reg", "add", registry_key, "/v", "Remote IP Prefix Length", "/t", "REG_SZ", "/d", "*", "/f"], shell=True, check=True)
        subprocess.run(["reg", "add", registry_key, "/v", "DSCP Value", "/t", "REG_SZ", "/d", "46", "/f"], shell=True, check=True)
        subprocess.run(["reg", "add", registry_key, "/v", "Throttle Rate", "/t", "REG_SZ", "/d", "-1", "/f"], shell=True, check=True)
        
        # PowerShell command to create a NetQoSPolicy
        subprocess.run(["powershell", "New-NetQosPolicy", "-Name", game_exe, "-AppPathNameMatchCondition", game_exe, "-Precedence", "127", "-DSCPAction", "46", "-IPProtocol", "Both"], check=True)

        messagebox.showinfo("Success", "DSCP settings applied for %s" % game_name)
    else:
        messagebox.showinfo("Info", "DSCP is not enabled.")

def generate_script(game_path, formatted_mask_hex):
    game_dir, game_exe = os.path.split(game_path)
    game_name, _ = os.path.splitext(os.path.basename(game_exe))  # Extracting just the executable name from the full path

    script_content = (
        "@echo off\n"
        "cd /d \"%s\"\n"
        "start /affinity %s /high %s\n"  # Remove the quotes around %s
    ) % (game_dir, formatted_mask_hex, game_exe)

    script_file = os.path.join(os.path.expanduser("~"), "Desktop", "%s_high_affinities.bat" % game_name)
    with open(script_file, "w") as f:
        f.write(script_content)

    messagebox.showinfo("Success", "Script saved to: %s" % script_file)

# Function to allow users to select the game executable
def explore():
    apply_priority_var = enable_priority_var.get()
    apply_FSE_var = enable_FSE_var.get()
    apply_DSCP_var = enable_DSCP_var.get()  # Get the value of the DSCP checkbox
    game_path = select_game_file()
    if not game_path:
        messagebox.showwarning("Warning", "No file selected.")
        return
    num_cores = get_number_of_cores() - 1
    mask = 0
    for i in range(1, num_cores + 1):
        mask |= 1 << i

    formatted_mask_hex = convert_dec_to_hex(mask)

    if apply_priority_var:
        apply_priority(game_path, apply_priority_var)
    generate_script(game_path, formatted_mask_hex)
    apply_FSE(game_path, apply_FSE_var)
    apply_DSCP(game_path, apply_DSCP_var)  # Apply DSCP settings

def revert_FSE():
    game_path = select_game_file()
    if not game_path:
        messagebox.showwarning("Warning", "No file selected.")
        return
    # Extracting directory and filename from the game path
    game_dir, game_exe = os.path.split(game_path)
    # Construct the registry key string with backslashes and without quotation marks
    registry_key = game_path.replace("/", "\\")
    # Delete the registry key for FSE
    subprocess.run(["reg", "delete", r"HKCU\SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers", "/v", registry_key, "/f"], shell=True, check=True)
    messagebox.showinfo("Success", "FSE reverted for %s" % game_exe)

def revert_DSCP(game_path):
    if not game_path:
        messagebox.showwarning("Warning", "No file selected.")
        return
    # Extracting directory and filename from the game path
    game_dir, game_exe = os.path.split(game_path)
    game_name, _ = os.path.splitext(os.path.basename(game_exe))  # Extracting just the executable name from the full path
    
    # Construct the registry key string with backslashes and without quotation marks
    registry_key = os.path.join("HKEY_LOCAL_MACHINE", "Software", "Policies", "Microsoft", "Windows", "QoS", game_exe)

    # Delete the registry key for DSCP settings
    try:
        subprocess.run(["reg", "delete", registry_key, "/f"], shell=True, check=True)
        # Remove the NetQoSPolicy
        subprocess.run(["powershell", "Remove-NetQosPolicy", "-Name", game_exe], check=True)
        messagebox.showinfo("Success", "DSCP settings reverted for %s" % game_name)
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Failed to revert DSCP settings. Registry does not exist or policy not found.")

# Function to revert only DSCP settings
def revert_DSCP_only():
    game_path = select_game_file()
    revert_DSCP(game_path)

def revert():
    game_path = select_game_file()
    if not game_path:
        messagebox.showwarning("Warning", "No file selected.")
        return
    apply_priority(game_path, False)

# Function to explicitly terminate subprocesses
def terminate_subprocesses():
    global sub_processes
    for process in sub_processes:
        process.terminate()

# Function to handle window closing event
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        terminate_subprocesses()
        root.destroy()

# Create the main Tkinter window
root = Tk()
root.title("Game Affinity Script Generator")
root.resizable(False, False)  # Lock the window size

# Define a variable to track whether DSCP should be applied
enable_DSCP_var = IntVar()

# Define variables to track whether high priority and FSE should be applied
enable_priority_var = IntVar()
enable_FSE_var = IntVar()

# Create and position the label prompting the user to select the game executable
label = Label(root, text="Press the button to select the game executable:")
label.pack()

# Create and position the "Explore" button
explore_button = Button(root, text="Explore", command=explore)
explore_button.pack()

# Create and position the frame to contain high priority checkbox and revert button
priority_frame = ttk.LabelFrame(root, text="Add high priority to registry?")
priority_frame.pack(pady=10)

# Create and position the checkbox for enabling high priority
priority_checkbutton = Checkbutton(priority_frame, text="Yes", variable=enable_priority_var)
priority_checkbutton.pack(side="left")

# Create and position the revert button for reverting changes made by the script
revert_button = Button(priority_frame, text="Revert", command=revert)
revert_button.pack(side="right")

# Create and position the frame to contain FSE checkbox
fse_frame = ttk.LabelFrame(root, text="Enable Full-Screen Exclusive (FSE)?")
fse_frame.pack(pady=10)

# Create and position the checkbox for enabling FSE
fse_checkbutton = Checkbutton(fse_frame, text="Yes", variable=enable_FSE_var)
fse_checkbutton.pack(side="left")

# Create and position the revert button for reverting FSE changes made by the script
revert_FSE_button = Button(fse_frame, text="Revert", command=revert_FSE)
revert_FSE_button.pack(side="right")

# Create and position the frame to contain DSCP checkbox
dscp_frame = ttk.LabelFrame(root, text="Enable DSCP settings?")
dscp_frame.pack(pady=10)

# Create and position the checkbox for enabling DSCP
dscp_checkbutton = Checkbutton(dscp_frame, text="Yes", variable=enable_DSCP_var)
dscp_checkbutton.pack(side="left")

# Create and position the revert button for reverting only DSCP changes made by the script
revert_DSCP_button = Button(root, text="Revert DSCP", command=revert_DSCP_only)
revert_DSCP_button.pack()

# Modify Tkinter window setup to call on_closing function when closing
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the Tkinter event loop
root.mainloop()