import subprocess
import os
from tkinter import Tk, filedialog, Label, Button, Checkbutton, IntVar, messagebox
import tkinter.ttk as ttk
import ctypes
import sys
import winreg

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
    return os.cpu_count()

def convert_dec_to_hex(decimal):
    return hex(decimal)

def select_game_file():
    root = Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(title="Select the game executable file")
    return file_path

def apply_priority(game_exe, enable_priority):
    if enable_priority:
        try:
            game_name = os.path.basename(game_exe)
            key_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\%s\PerfOptions" % game_name
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
                winreg.SetValueEx(key, "IoPriority", 0, winreg.REG_DWORD, 3)
                winreg.SetValueEx(key, "CpuPriorityClass", 0, winreg.REG_DWORD, 3)
            messagebox.showinfo("Success", "High priority added to registry for %s" % game_name)
        except Exception as e:
            messagebox.showerror("Error", "Failed to add high priority to registry: %s" % str(e))
    else:
        if game_exe:
            try:
                game_name = os.path.basename(game_exe)
                key_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\%s\PerfOptions" % game_name
                winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, key_path)
                messagebox.showinfo("Success", "High priority registry settings reverted for %s" % game_name)
            except Exception as e:
                messagebox.showerror("Error", "Failed to revert registry settings: %s" % str(e))

def apply_FSE(game_path, enable_FSE):
    if enable_FSE:
        if game_path:
            try:
                # Replace forward slashes with backslashes in the game path
                game_path = game_path.replace("/", "\\")
                # Extracting directory and filename from the game path
                game_dir, game_exe = os.path.split(game_path)
                # Open the registry key for writing
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers", 0, winreg.KEY_ALL_ACCESS) as key:
                    # Set the registry value for the game executable
                    winreg.SetValueEx(key, game_path, 0, winreg.REG_SZ, "~ DISABLEDXMAXIMIZEDWINDOWEDMODE HIGHDPIAWARE")
                messagebox.showinfo("Success", "FSE added to registry for %s" % game_exe)
            except Exception as e:
                messagebox.showerror("Error", "Failed to add FSE to registry: %s" % str(e))

def apply_DSCP(game_path, enable_DSCP):
    if enable_DSCP:
        try:
            # Extracting directory and filename from the game path
            game_dir, game_exe = os.path.split(game_path)
            game_name, _ = os.path.splitext(os.path.basename(game_exe))  # Extracting just the executable name from the full path

            # Construct the registry key path
            registry_key_path = r"Software\Policies\Microsoft\Windows\QoS\%s" % game_exe

            # Open or create the registry key
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, registry_key_path) as key:
                # Set values for DSCP settings
                winreg.SetValueEx(key, "Application Name", 0, winreg.REG_SZ, game_exe)
                winreg.SetValueEx(key, "Version", 0, winreg.REG_SZ, "1.0")
                winreg.SetValueEx(key, "Protocol", 0, winreg.REG_SZ, "*")
                winreg.SetValueEx(key, "Local Port", 0, winreg.REG_SZ, "*")
                winreg.SetValueEx(key, "Local IP", 0, winreg.REG_SZ, "*")
                winreg.SetValueEx(key, "Local IP Prefix Length", 0, winreg.REG_SZ, "*")
                winreg.SetValueEx(key, "Remote Port", 0, winreg.REG_SZ, "*")
                winreg.SetValueEx(key, "Remote IP", 0, winreg.REG_SZ, "*")
                winreg.SetValueEx(key, "Remote IP Prefix Length", 0, winreg.REG_SZ, "*")
                winreg.SetValueEx(key, "DSCP Value", 0, winreg.REG_SZ, "46")
                winreg.SetValueEx(key, "Throttle Rate", 0, winreg.REG_SZ, "-1")

            # Execute PowerShell command to create a NetQoSPolicy
            subprocess.run(["powershell", "New-NetQosPolicy", "-Name", game_exe, "-AppPathNameMatchCondition", game_exe, "-Precedence", "127", "-DSCPAction", "46", "-IPProtocol", "Both"], check=True)

            messagebox.showinfo("Success", "DSCP settings applied for %s" % game_name)
        except Exception as e:
            messagebox.showerror("Error", "Failed to apply DSCP settings: %s" % str(e))

def generate_script(game_path, formatted_mask_hex, enable_high_priority, enable_affinities):
    game_dir, game_exe = os.path.split(game_path)
    game_name, _ = os.path.splitext(os.path.basename(game_exe))  # Extracting just the executable name from the full path

    script_content = (
        "@echo off\n"
        "cd /d \"%s\"\n"  # Change directory to the game directory
        % game_dir +
        "start "  # Start the game process
    )
    if enable_affinities:
        script_content += "/affinity %s " % formatted_mask_hex  # Add affinity option if selected
    if enable_high_priority:
        script_content += "/high "  # Add high priority option if selected
    script_content += "%s\n" % game_exe  # Start the game executable

    script_file = os.path.join(os.path.expanduser("~"), "Desktop", "%s_script.bat" % game_name)
    with open(script_file, "w") as f:
        f.write(script_content)

    messagebox.showinfo("Success", "Script saved to: %s" % script_file)

def explore():
    apply_priority_var = enable_priority_var.get()
    apply_FSE_var = enable_FSE_var.get()
    apply_DSCP_var = enable_DSCP_var.get()
    enable_high_priority = enable_high_priority_var.get()  # Get the value of the /high checkbox
    enable_affinities = enable_affinities_var.get()  # Get the value of the /affinities checkbox

    # Check if at least one option is selected
    if not (apply_priority_var or apply_FSE_var or apply_DSCP_var or enable_high_priority or enable_affinities):
        messagebox.showwarning("Warning", "Pick at least 1 option to use Explore.")
        return

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
    generate_script(game_path, formatted_mask_hex, enable_high_priority, enable_affinities)
    apply_FSE(game_path, apply_FSE_var)
    apply_DSCP(game_path, apply_DSCP_var)

def revert_FSE():
    game_path = select_game_file()
    if not game_path:
        messagebox.showwarning("Warning", "No file selected.")
        return
    try:
        game_dir, game_exe = os.path.split(game_path)
        registry_key = r"HKCU\SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_key, 0, winreg.KEY_ALL_ACCESS) as key:
            winreg.DeleteValue(key, game_path)
        messagebox.showinfo("Success", "FSE reverted for %s" % game_exe)
    except Exception as e:
        messagebox.showerror("Error", "Failed to revert FSE registry settings: %s" % str(e))

def revert_DSCP(game_path):
    if not game_path:
        messagebox.showwarning("Warning", "No file selected.")
        return
    try:
        game_dir, game_exe = os.path.split(game_path)
        game_name, _ = os.path.splitext(os.path.basename(game_exe))
        key_path = r"Software\Policies\Microsoft\Windows\QoS\%s" % game_exe
        winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, key_path)
        subprocess.run(["powershell", "Remove-NetQosPolicy", "-Name", game_exe], check=True)
        messagebox.showinfo("Success", "DSCP settings reverted for %s" % game_name)
    except Exception as e:
        messagebox.showerror("Error", "Failed to revert DSCP settings: %s" % str(e))

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

# Define variables to track whether /high and /affinities should be added to the script
enable_high_priority_var = IntVar()
enable_affinities_var = IntVar()

# Create and position the label prompting the user to select the game executable
label = Label(root, text="Press the button to select the game executable:")
label.pack()

# Create and position the "Explore" button
explore_button = Button(root, text="Explore", command=explore)
explore_button.pack()

# Create and position the frame to contain options for generating the script
generating_script_frame = ttk.LabelFrame(root, text="Generating Script", labelanchor='n')
generating_script_frame.pack(pady=10)

# Create and position the checkbox for enabling /high option
high_checkbutton = Checkbutton(generating_script_frame, text="Add /high option", variable=enable_high_priority_var)
high_checkbutton.pack()

# Create and position the checkbox for enabling /affinities option
affinities_checkbutton = Checkbutton(generating_script_frame, text="Add /affinities option", variable=enable_affinities_var)
affinities_checkbutton.pack()

# Create and position the frame to contain high priority checkbox and revert button
priority_frame = ttk.LabelFrame(root, text="Add high priority to registry?", labelanchor='n')
priority_frame.pack(pady=10)

# Create and position the checkbox for enabling high priority
priority_checkbutton = Checkbutton(priority_frame, text="Yes", variable=enable_priority_var)
priority_checkbutton.pack(side="left")

# Create and position the revert button for reverting changes made by the script
revert_button = Button(priority_frame, text="Revert", command=revert)
revert_button.pack(side="right")

# Create and position the frame to contain FSE checkbox
fse_frame = ttk.LabelFrame(root, text="Enable Full-Screen Exclusive (FSE)?", labelanchor='n')
fse_frame.pack(pady=10)

# Create and position the checkbox for enabling FSE
fse_checkbutton = Checkbutton(fse_frame, text="Yes", variable=enable_FSE_var)
fse_checkbutton.pack(side="left")

# Create and position the revert button for reverting FSE changes made by the script
revert_FSE_button = Button(fse_frame, text="Revert", command=revert_FSE)
revert_FSE_button.pack(side="right")

# Create and position the frame to contain DSCP checkbox
dscp_frame = ttk.LabelFrame(root, text="Enable DSCP settings?", labelanchor='n')
dscp_frame.pack(pady=10)

# Create and position the checkbox for enabling DSCP
dscp_checkbutton = Checkbutton(dscp_frame, text="Yes", variable=enable_DSCP_var)
dscp_checkbutton.pack(side="left")

# Create and position the revert button for reverting only DSCP changes made by the script
revert_DSCP_button = Button(dscp_frame, text="Revert", command=revert_DSCP_only)
revert_DSCP_button.pack(side="right")

# Modify Tkinter window setup to call on_closing function when closing
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the Tkinter event loop
root.mainloop()