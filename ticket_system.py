import csv
import time

class TicketSystem:
    def __init__(self, file="tickets.csv"):
        self.file = file
        self.ensure_file_exists()

    def ensure_file_exists(self):
        try:
            with open(self.file, "x", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Ticket ID", "Issue", "Timestamp", "Status"])
        except FileExistsError:
            pass

    def create_ticket(self, issue):
        ticket_id = int(time.time())
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        status = "Pending"

        with open(self.file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([ticket_id, issue, timestamp, status])

        return ticket_id
