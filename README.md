# EasyGameOptions

[![Downloads](https://img.shields.io/github/downloads/eskezje/EasyGameOptions/total.svg)](https://github.com/eskezje/EasyGameOptions/releases)

EasyGameOptions is a powerful utility script designed to optimize gaming experiences on Windows systems. This script simplifies the process of fine-tuning system settings, including CPU affinity, Full-Screen Exclusive (FSE) mode, and Differentiated Services Code Point (DSCP) configurations. With EasyGameOptions, users can effortlessly enhance gaming performance while enjoying the flexibility to revert changes when necessary.

![EasyGameOptions](https://github.com/eskezje/EasyGameOptions/assets/114604325/d7cb196f-171a-46c1-952b-2e0fe2f661ba)

## Features

- **Script Generation**: Generate desktop scripts for easy application of optimizations.
  - *CPU Affinities*: Customize CPU affinities for enhanced performance.
  - *High Priority in Script*: Include high priority settings directly within the generated script.
- **High Priority Registry Setting**: Elevate priority levels for specified game executables in the Windows Registry.
- **Full-Screen Exclusive (FSE) Support**: Enable Full-Screen Exclusive mode for immersive gaming experiences.
- **DSCP Settings Configuration**: Configure Differentiated Services Code Point settings to ensure superior Quality of Service (QoS).
- **Revert Functionality**: Effortlessly undo applied changes using the convenient revert feature.

## Requirements

- Windows operating system.
- Python 3 installed.
- Tkinter library (usually included with Python installations on Windows).

## Usage

1. **Run as Administrator**: Execute the script with administrative privileges to apply system changes.
2. **Select Game Executable**: Click the "Explore" button to navigate and select the game executable file.
3. **Customize Options**:
   - **Script Generation**: Choose options for CPU affinities and high priority settings directly within the generated script.
     - *CPU Affinities*: Customize CPU affinities for enhanced performance.
     - *High Priority in Script*: Include high priority settings directly within the generated script.
   - **High Priority in registry**: Check the box to elevate priority levels for optimized performance.
   - **FSE**: Enable Full-Screen Exclusive mode for an immersive gaming experience.
   - **DSCP**: Configure Differentiated Services Code Point settings for enhanced Quality of Service.
4. **Apply Changes**: Click the "Explore" button to apply selected optimizations.
5. **Revert Changes**: Utilize the "Revert" buttons to undo specific changes or revert all modifications made by the script.

## How to Run

1. Clone the repository or download the script file.
2. Open Command Prompt or PowerShell with administrative privileges.
3. Navigate to the directory containing the script.
4. Run the script using the command: `python EasyGameOptions.py`.

## Disclaimer

- This script modifies system settings and registry entries. Use it at your own risk.
- Always ensure you have backups or restore points before making changes to system configurations.

## Contributing

Contributions to enhance EasyGameOptions are welcome! Feel free to submit issues or pull requests.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
