# IT Support Technician Work Order System

A desktop application built with **Python and Tkinter** to simulate a support technician receiving service requests, choosing a troubleshooting category, and scheduling an appointment. The application displays a work-order preview and saves each request to a text file.

This is an **educational IT support workflow simulation**, not an active help desk or ticketing service. It began as my CIS-30A Python final project, *Pleasant Tech Services - Business Order and Appointment System*, and was adapted into a technician-focused portfolio project.

## What it does

- Records a requester's name and a short description of the issue
- Offers three support categories: computer troubleshooting, Wi-Fi/network support, and account access assistance
- Allows standard or priority service (with an estimated priority fee)
- Schedules a requested appointment within the next 365 days
- Adds optional technician tasks such as backup assistance and a device health check
- Calculates an **estimated** service cost
- Previews a technician work order and exports it to a timestamped `.txt` file in `records/`
- Checks for missing information and invalid appointment dates

**Note:** The application organizes support requests; it does not diagnose computers, reset real passwords, connect to networks, book real appointments, or perform the selected tasks. Do not enter real passwords or sensitive customer data.

## Python concepts demonstrated

The project uses beginner-to-intermediate Python concepts covered in my CIS-30A coursework: Tkinter GUI controls, classes and objects, a class inheriting from another class, method overriding, a separate Python module, dictionaries and lists, `for` loops, `if` statements, exception handling, date parsing, and basic file output.

The code is split into two main modules:

| File | Responsibility |
|---|---|
| `src/main.py` | Builds the Tkinter GUI, reads form inputs, validates the requested appointment, and responds to button clicks |
| `src/business_logic.py` | Defines the service classes and support ticket, calculates estimated cost, formats summaries, and writes files |

## How to run

Requires Python 3 with Tkinter installed. Tkinter is included with many desktop Python installations, but may need to be installed separately on Linux.

```bash
python src/main.py
```

1. Enter the requester's name and a short problem description
2. Choose a support category, priority level, and desired appointment time
3. Select optional technician tasks
4. Click **Preview Ticket** to review the information
5. Click **Save Ticket** to create a text file in `records/`

Use **Clear** to reset the form. The saved files are local work-order examples, not submitted to any service desk.

## Simple code tests

```bash
python -m unittest discover -s tests -v
```

The tests verify service pricing, validation of invalid pricing, the priority fee, optional-task totals, ticket formatting, and saving to a text file. The test file adds `src/` to Python's module search path so the command above works from the repository root. The graphical interface itself is not covered by these unit tests.

## Project limitations

This project does not store tickets in a database, assign real technicians, track work in progress, authenticate users, integrate with email, or provide automatic troubleshooting. All costs are demonstration estimates. The program is designed as an approachable introduction to a support technician's intake workflow rather than a production ticketing platform.

## Project background

Adapted from a CIS-30A final project demonstrating object-oriented programming, GUI development, loops, validation, and file operations. The service-ordering concept was refocused on documenting and scheduling technical support requests while keeping the same general programming level.
