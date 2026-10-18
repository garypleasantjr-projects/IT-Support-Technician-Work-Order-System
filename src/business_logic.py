from datetime import datetime
import os


class Service:
    def __init__(self, name: str, base_price: float):
        self.name = name
        self.base_price = base_price

    def get_price(self) -> float:
        if self.base_price < 0:
            raise ValueError("Service price cannot be negative")
        return float(self.base_price)


class PriorityService(Service):
    # Inheritance allows priority support to use the same service pricing method
    def __init__(self, name: str, base_price: float, priority_fee: float):
        super().__init__(name, base_price)
        self.priority_fee = priority_fee

    def get_price(self) -> float:
        return super().get_price() + float(self.priority_fee)


class SupportTicket:
    def __init__(self, requester: str, problem: str, service: Service, tasks: list, appointment_dt: datetime):
        self.requester = requester
        self.problem = problem
        self.service = service
        self.tasks = tasks
        self.appointment_dt = appointment_dt

    def total(self) -> float:
        # Add the selected technician tasks to the estimated service price
        total_cost = self.service.get_price()

        for task in self.tasks:
            total_cost += task["price"]

        return round(total_cost, 2)

    def summary(self) -> str:
        # FORMAT A WORK ORDER FOR THE SUPPORT TECHNICIAN
        summary = ""
        summary += "========================================\n"
        summary += "IT SUPPORT TECHNICIAN WORK ORDER\n"
        summary += "========================================\n"
        summary += "Status: Appointment Requested (Demo)\n"
        summary += f"Requester: {self.requester}\n"
        summary += f"Problem: {self.problem}\n"
        summary += f"Appointment: {self.appointment_dt.strftime('%Y-%m-%d %H:%M')}\n"
        summary += f"Service: {self.service.name} (${self.service.get_price():.2f})\n"

        if self.tasks:
            summary += "Additional Tasks:\n"
            for task in self.tasks:
                summary += f"  - {task['name']} (${task['price']:.2f})\n"
        else:
            summary += "Additional Tasks: None\n"

        summary += f"\nEstimated Total: ${self.total():.2f}\n"
        summary += "========================================\n"
        return summary

    def save(self) -> str:
        # Each support request is saved as a separate text file
        os.makedirs("records", exist_ok=True)
        filename = f"support_ticket_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.txt"
        path = os.path.join("records", filename)

        with open(path, "w", encoding="utf-8") as file:
            file.write(self.summary())

        return path
