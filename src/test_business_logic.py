import os
import tempfile
import unittest
from datetime import datetime

from business_logic import Service, PriorityService, SupportTicket


class SupportTicketTests(unittest.TestCase):
    def test_standard_service_price(self):
        service = Service("Computer Troubleshooting", 40.0)
        self.assertEqual(service.get_price(), 40.0)

    def test_priority_service_price(self):
        service = PriorityService("Network Support", 50.0, 15.0)
        self.assertEqual(service.get_price(), 65.0)

    def test_invalid_base_price(self):
        with self.assertRaises(ValueError):
            Service("Example", -10.0).get_price()

    def test_ticket_total_and_summary(self):
        service = PriorityService("Computer Troubleshooting", 40.0, 15.0)
        tasks = [{"name": "Data Backup Assistance", "price": 20.0}]
        ticket = SupportTicket("Demo User", "Computer is running slowly", service,
                               tasks, datetime(2027, 2, 1, 14, 30))
        self.assertEqual(ticket.total(), 75.0)
        self.assertIn("Computer is running slowly", ticket.summary())
        self.assertIn("Estimated Total: $75.00", ticket.summary())

    def test_saving_ticket(self):
        ticket = SupportTicket("Demo User", "Cannot connect to Wi-Fi",
                               Service("Network Support", 50.0), [],
                               datetime(2027, 2, 1, 14, 30))
        old_dir = os.getcwd()
        with tempfile.TemporaryDirectory() as directory:
            try:
                os.chdir(directory)
                filename = ticket.save()
                with open(filename, encoding="utf-8") as file:
                    saved_text = file.read()
                self.assertIn("Cannot connect to Wi-Fi", saved_text)
                self.assertIn("Additional Tasks: None", saved_text)
            finally:
                os.chdir(old_dir)


if __name__ == "__main__":
    unittest.main()
