import random
import json
import os

class Reservation:
    def __init__(self):
        self.reservations = []
        self.file_path = os.path.join(os.path.dirname(__file__), "reservations.json")

    def add_reservation(self, check_in_date, check_out_date, room_type, room_status, guest_name, id_number, guest_preferences):
        # Generate a random 8-digit serial number
        serial_number = str(random.randint(10000000, 99999999))

        # Check if the serial number is already used
        for res in self.reservations:
            if res["serial_number"] == serial_number:
                return False

        # Create a new reservation dictionary
        reservation = {
            "serial_number": serial_number,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
            "room_type": room_type,
            "room_status": room_status,
            "guest_name": guest_name,
            "id_number": id_number,
            "guest_preferences": guest_preferences
        }

        # Add the reservation to the list
        self.reservations.append(reservation)

        # Save the reservations to the JSON file
        self.save_reservations()

        return True

    def delete_reservation(self, index):
        if index >= 0 and index < len(self.reservations):
            del self.reservations[index]

            # Save the updated reservations to the JSON file
            self.save_reservations()

    def get_all_reservations(self):
        # Load reservations from the JSON file
        self.load_reservations()

        return self.reservations

    def save_reservations(self):
        with open(self.file_path, "w") as file:
            json.dump(self.reservations, file)

    def load_reservations(self):
        self.reservations = []

        if not os.path.exists(self.file_path):
            # Create an empty reservations.json file
            with open(self.file_path, "w") as file:
                json.dump([], file)

        try:
            with open(self.file_path, "r") as file:
                self.reservations = json.load(file)
        except FileNotFoundError:
            pass

    def print_reservation(self, index):
        if index >= 0 and index < len(self.reservations):
            reservation = self.reservations[index]
            guest_name = reservation["guest_name"]
            serial_number = reservation["serial_number"]
            check_in_date = reservation["check_in_date"]
            check_out_date = reservation["check_out_date"]
            room_type = reservation["room_type"]
            room_status = reservation["room_status"]
            id_number = reservation["id_number"]
            guest_preferences = reservation["guest_preferences"]



            return True

        return False
