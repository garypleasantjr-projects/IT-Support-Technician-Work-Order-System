import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

from business_logic import Service, PriorityService, SupportTicket


# SERVICE CATEGORIES AND ESTIMATED PRICES
SERVICES = {
    "Computer Troubleshooting ($40)": Service("Computer Troubleshooting", 40.0),
    "Wi-Fi / Network Support ($50)": Service("Wi-Fi / Network Support", 50.0),
    "Account Access Assistance ($25)": Service("Account Access Assistance", 25.0),
}

OPTIONAL_TASKS = [
    {"name": "Data Backup Assistance", "price": 20.0},
    {"name": "Device Health Check", "price": 15.0},
]

PRIORITY_FEE = 15.0


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("IT Support Technician - Work Order System")
        self.geometry("780x690")

        ttk.Label(self, text="IT SUPPORT WORK ORDER SYSTEM", font=("Arial", 17, "bold")).pack(pady=(10, 2))
        ttk.Label(self, text="Support request intake and appointment scheduling", font=("Arial", 10)).pack(pady=(0, 10))

        self.status_var = tk.StringVar(value="Status: Ready")
        ttk.Label(self, textvariable=self.status_var, font=("Arial", 9)).pack(anchor="w", padx=12)

        # REQUESTER INFORMATION
        requester_frame = ttk.LabelFrame(self, text="Requester and Issue", padding=10)
        requester_frame.pack(fill="x", padx=12, pady=6)

        ttk.Label(requester_frame, text="Requester Name:").pack(anchor="w")
        self.name_var = tk.StringVar()
        ttk.Entry(requester_frame, textvariable=self.name_var).pack(fill="x", pady=3)

        ttk.Label(requester_frame, text="Brief Problem Description:").pack(anchor="w")
        self.issue_var = tk.StringVar()
        ttk.Entry(requester_frame, textvariable=self.issue_var).pack(fill="x", pady=3)

        # SELECT THE KIND OF TECHNICAL SUPPORT
        service_frame = ttk.LabelFrame(self, text="Support Service", padding=10)
        service_frame.pack(fill="x", padx=12, pady=6)

        ttk.Label(service_frame, text="Support Category:").pack(anchor="w")
        self.service_var = tk.StringVar(value=list(SERVICES.keys())[0])
        ttk.Combobox(
            service_frame,
            textvariable=self.service_var,
            values=list(SERVICES.keys()),
            state="readonly"
        ).pack(fill="x", pady=3)

        ttk.Label(service_frame, text="Service Priority:").pack(anchor="w", pady=(5, 0))
        self.priority_var = tk.StringVar(value="Standard")
        ttk.Combobox(
            service_frame,
            textvariable=self.priority_var,
            values=["Standard", "Priority"],
            state="readonly"
        ).pack(fill="x", pady=3)

        # THE REQUESTED APPOINTMENT MUST BE WITHIN ONE YEAR
        appt_frame = ttk.LabelFrame(self, text="Requested Appointment", padding=10)
        appt_frame.pack(fill="x", padx=12, pady=6)

        ttk.Label(appt_frame, text="Date and Time (YYYY-MM-DD HH:MM) - within the next 365 days:").pack(anchor="w")
        self.dt_var = tk.StringVar(value=self.default_appointment())
        ttk.Entry(appt_frame, textvariable=self.dt_var).pack(fill="x", pady=3)

        # OPTIONAL TECHNICIAN TASKS
        tasks_frame = ttk.LabelFrame(self, text="Additional Technician Tasks", padding=10)
        tasks_frame.pack(fill="x", padx=12, pady=6)

        self.task_vars = []
        for task in OPTIONAL_TASKS:
            selected = tk.BooleanVar(value=False)
            self.task_vars.append(selected)
            ttk.Checkbutton(
                tasks_frame,
                text=f"{task['name']} (+${task['price']:.2f})",
                variable=selected
            ).pack(anchor="w")

        button_frame = ttk.Frame(self, padding=10)
        button_frame.pack(fill="x", padx=12, pady=4)
        ttk.Button(button_frame, text="Preview Ticket", command=self.preview).pack(side="left", padx=(0, 8))
        ttk.Button(button_frame, text="Save Ticket", command=self.save).pack(side="left", padx=(0, 8))
        ttk.Button(button_frame, text="Clear", command=self.clear).pack(side="left")

        ttk.Label(self, text="Work Order Preview:", font=("Arial", 10, "bold")).pack(anchor="w", padx=12)
        self.out = tk.Text(self, height=10, wrap="word", bd=2, relief="sunken")
        self.out.pack(fill="both", expand=True, padx=12, pady=6)

        ttk.Label(self, text="Python / Tkinter educational project - CIS30A", font=("Arial", 9)).pack(pady=(0, 8))

    def default_appointment(self):
        tomorrow = datetime.now() + timedelta(days=1)
        return tomorrow.strftime("%Y-%m-%d 13:00")

    def validate_within_365_days(self, appointment):
        now = datetime.now()
        latest = now + timedelta(days=365)

        if appointment <= now:
            raise ValueError("Appointment must be in the future")
        if appointment > latest:
            raise ValueError("Appointment must be within the next 365 days")

    # VALIDATE THE FORM AND BUILD A SUPPORT TICKET OBJECT
    def build_ticket(self):
        requester = self.name_var.get().strip()
        problem = self.issue_var.get().strip()

        if not requester:
            raise ValueError("Requester name is required")
        if len(requester) > 40:
            raise ValueError("Requester name must be 40 characters or fewer")
        if not problem:
            raise ValueError("A brief problem description is required")
        if len(problem) > 120:
            raise ValueError("Problem description must be 120 characters or fewer")

        service_key = self.service_var.get()
        base_service = SERVICES[service_key]

        try:
            appointment = datetime.strptime(self.dt_var.get().strip(), "%Y-%m-%d %H:%M")
        except ValueError:
            raise ValueError("Date/time must use YYYY-MM-DD HH:MM (24-hour)")

        self.validate_within_365_days(appointment)

        # Subclass adds a fee when a priority appointment is selected
        if self.priority_var.get() == "Priority":
            service = PriorityService(base_service.name, base_service.get_price(), PRIORITY_FEE)
        else:
            service = Service(base_service.name, base_service.get_price())

        chosen_tasks = []
        for selected, task in zip(self.task_vars, OPTIONAL_TASKS):
            if selected.get():
                chosen_tasks.append(task)

        return SupportTicket(requester, problem, service, chosen_tasks, appointment)

    def preview(self):
        self.out.delete("1.0", "end")
        try:
            ticket = self.build_ticket()
            self.out.insert("end", ticket.summary())
            self.status_var.set("Status: Ticket preview generated")
        except (ValueError, KeyError) as error:
            messagebox.showerror("Invalid Request", str(error))
            self.status_var.set("Status: Please check the form")

    def save(self):
        try:
            ticket = self.build_ticket()
            filename = ticket.save()
            self.out.delete("1.0", "end")
            self.out.insert("end", ticket.summary())
            messagebox.showinfo("Ticket Saved", f"Support ticket saved to:\n{filename}")
            self.status_var.set(f"Status: Saved to {filename}")
        except (ValueError, KeyError, OSError) as error:
            messagebox.showerror("Unable to Save", str(error))
            self.status_var.set("Status: Unable to save ticket")

    def clear(self):
        self.name_var.set("")
        self.issue_var.set("")
        self.service_var.set(list(SERVICES.keys())[0])
        self.priority_var.set("Standard")
        self.dt_var.set(self.default_appointment())
        for selected in self.task_vars:
            selected.set(False)

        self.out.delete("1.0", "end")
        self.status_var.set("Status: Ready")


if __name__ == "__main__":
    App().mainloop()
