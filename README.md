# Processes Management App

This script provides a simple GUI application using Tkinter for managing processes on a Windows system. It allows users to view, kill processes by ID or name, and create new processes.

## Prerequisites

1. **Python:**
   - Ensure that Python is installed on your system. If not, you can download and install it from [python.org](https://www.python.org/downloads/).

2. **Tkinter:**
   - Tkinter is included with most Python installations, but you may need to install it separately on some systems. Use the following command to install Tkinter:
     ```bash
     pip install tk
     ```

## Usage

1. Run the script using a Python interpreter.
   ```bash
   python processes_management_app.py
   ```

2. The application GUI will appear with a list of processes, their details, and options for managing them.

## Features

- View a list of running processes with details such as ID, start date, start time, CPU usage, process name, and window title.
- Kill a process by entering its ID or name.
- Create a new process by providing its full path or name.

## How to Use

1. **Kill Process by ID:**
   - Enter the process ID in the "Enter process ID to kill" field.
   - Click the "Kill ID" button.

2. **Kill Process by Name:**
   - Enter the process name in the "Enter process Name to kill" field.
   - Click the "Kill Name" button.

3. **Create New Process:**
   - Enter the process path or name in the "Enter process Path to create" field.
   - Click the "Create Process" button.

4. **Refresh Process List:**
   - Click the "Refresh" button to update the list of running processes.

5. **Show System Processes:**
   - Click the "Show System Processes" button to display all processes, including system processes.

6. **Show Main Processes:**
   - Click the "Show Main Processes" button to display only user-level processes.
