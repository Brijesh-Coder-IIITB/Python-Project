# Python-Project
## Smart Home Automation System
A modular and interactive application for managing various smart home devices, including lights, fans, thermostats, and cameras.

### Commands to Start the Application
Run the following command in your terminal to start the project:

```
python project\ 12.py
```
This will initialize the system and open the main interface.

### Supported Operating Systems
- Linux
- Windows
- Mac

## Prerequisite Software and Libraries
### Python Installation

Ensure Python 3.6 or higher is installed. Download from the official Python website.

>**Note:**  
https://www.python.org/downloads/

### Required Libraries
Install required libraries using pip:

```
pip install tk
```
>**Note:** tkinter is typically pre-installed with Python. If not, consult your operating system documentation.

## Features Implemented
---
### Core Features
- User Management:
  - Register and login functionality.
- Device Control:
  - Add, configure, and manage various smart devices, including:
    - Lights: Adjust brightness and change colors.
    - Fans: Set speed levels.
    - Thermostats: Manage temperature and mode.
    - Cameras: Control recording and resolution settings.
- Real-time Reporting:
  - Generate and save a comprehensive status report of all devices.
- Interactive UI:
  - User-friendly graphical interface to manage all devices easily.
---
### Modularity
The system uses individual Python files for device-specific implementations:

- LIGHT.py: Handles light-related functionalities.
- FAN.py: Manages fan operations.
- THERMOSTAT.py: Controls thermostat configurations.
- CAMERA.py: Manages security camera settings.
- DEVICE.py: Provides the base class for all devices, ensuring consistency and extensibility.
  
## Libraries/APIs/Databases Used
- tkinter: For GUI design.
- json: For persistent data storage.
- os: For file system interactions.
- datetime: For generating and logging reports.
## Classes and Modules
### Main Script (project 12.py)
- Acts as the entry point of the application.
- Initializes the user interface and device manager.
### Device-Specific Modules
**1.** DEVICE.py:

  - Contains the base Device class.
  - Common attributes: name, location, owner, and power state.
    
**2.** LIGHT.py:

  - Extends Device with additional attributes for brightness and color.
  - Methods to set brightness and change color.
    
**3.** FAN.py:

  - Extends Device to include speed control.
    
**4.** THERMOSTAT.py:

  - Extends Device to include temperature and mode settings.
**5.** CAMERA.py:

  - Extends Device with functionality for recording and resolution management.

### Data Management
- Device states are stored in the data directory in JSON format.
- User authentication data is securely stored and managed.
## Work Done by Each Team Member
- Team Member 1:
  - Implemented the Device class and core modules like DEVICE.py.
- Team Member 2:
  - Developed device-specific modules (LIGHT.py, FAN.py, THERMOSTAT.py, and CAMERA.py).
- Team Member 3:
  - Designed the project 12.py script to integrate all modules and manage the user interface.
- Team Member 4:
  - Created the data handling and reporting features.
How to Contribute
Fork the repository, make your changes, and submit a pull request. Ensure you follow the coding standards outlined in CONTRIBUTING.md
