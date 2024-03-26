## EasyGameOptions

EasyGameOptions is a utility script designed to streamline the optimization process for gaming on Windows systems. It allows users to easily apply various performance tweaks such as setting CPU affinity, enabling Full-Screen Exclusive (FSE), and configuring Differentiated Services Code Point (DSCP) settings. Additionally, it provides the option to revert these changes if needed.

![image](https://github.com/eskezje/EasyGameOptions/assets/114604325/d7cb196f-171a-46c1-952b-2e0fe2f661ba)

### Features

- **High Priority Registry Setting**: Adds high priority to the Windows Registry for specified game executables.
- **Full-Screen Exclusive (FSE) Support**: Enables FSE mode for enhanced gaming experience.
- **DSCP Settings Configuration**: Allows users to configure DSCP settings for improved Quality of Service (QoS).
- **Revert Functionality**: Provides the ability to revert applied changes effortlessly.

### Requirements

- Windows operating system.
- Python 3 installed.
- Tkinter library (usually included with Python installations on Windows).

### Usage

1. **Run as Administrator**: The script must be executed with administrative privileges to make changes to the system.
2. **Select Game Executable**: Click on the "Explore" button to select the game executable file.
3. **Customize Options**:
   - **High Priority**: Check the box to add high priority to the game executable.
   - **FSE**: Check the box to enable Full-Screen Exclusive mode.
   - **DSCP**: Check the box to configure DSCP settings.
4. **Apply Changes**: Click the "Explore" button to apply the selected options.
5. **Revert Changes**: Use the "Revert" buttons to revert specific changes or all changes made by the script.

### How to Run

1. Clone the repository or download the script file.
2. Open Command Prompt or PowerShell with administrative privileges.
3. Navigate to the directory containing the script.
4. Run the script using the command: `python easy_game_options.py`.

### Disclaimer

- This script modifies system settings and registry entries. Use it at your own risk.
- Always ensure you have backups or restore points before making changes to system configurations.

### Contributing

Contributions to enhance EasyGameOptions are welcome! Feel free to submit issues or pull requests.

### License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
