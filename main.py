import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
from datetime import timedelta
import random
from fpdf import FPDF
import os
import csv

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Detalles de la Reserva", align="C", ln=True)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")


class Reservation:
    def save_reservations_to_csv(self, filename):
        fieldnames = [
            "serial_number",
            "check_in_date",
            "check_out_date",
            "room_type",
            "room_status",
            "guest_name",
            "id_number",
            "guest_preferences"
        ]

        if not self.reservations:
            return  # Return if there are no reservations

        with open(filename, mode='a', newline='') as file:  # Open the file in append mode
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:  # Check if the file is empty
                writer.writeheader()

            writer.writerow(self.reservations[-1])

    def load_reservations_from_csv(self, filename):
        self.reservations = []  # Clear existing reservations

        try:
            with open(filename, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.reservations.append(row)
        except FileNotFoundError:
            pass

    def __init__(self):
        self.reservations = []
        self.serial_numbers = set()

    

    def generate_serial_number(self):
        serial_number = random.randint(10000000, 99999999)
        while serial_number in self.serial_numbers:
            serial_number = random.randint(10000000, 99999999)
        self.serial_numbers.add(serial_number)
        return serial_number

    def create_reservation(self, check_in_date, check_out_date, room_type, room_status, guest_name, id_number,
                           guest_preferences):
        serial_number = self.generate_serial_number()
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
        self.reservations.append(reservation)
        return True

    def delete_reservation(self, index):
        if index >= 0 and index < len(self.reservations):
            del self.reservations[index]

    def get_all_reservations(self):
        return self.reservations

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

            pdf = PDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(0, 10, f"Nombre: {guest_name}", ln=True)
            pdf.cell(0, 10, f"Número de serie: {serial_number}", ln=True)
            pdf.cell(0, 10, f"Fecha de entrada: {check_in_date}", ln=True)
            pdf.cell(0, 10, f"Fecha de salida: {check_out_date}", ln=True)
            pdf.cell(0, 10, f"Cantidad noches: {self.calculate_nights(check_in_date, check_out_date)}", ln=True)
            pdf.cell(0, 10, f"Tipo habitacion: {room_type}", ln=True)
            pdf.cell(0, 10, f"Status: {room_status}", ln=True)
            pdf.cell(0, 10, f"Numero cédula: {id_number}", ln=True)
            pdf.cell(0, 10, f"Preferences: {guest_preferences}", ln=True)

            script_dir = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(script_dir, "pdfs", f"{guest_name}_{serial_number}.pdf")
            pdf.output(filename)

            return True

        return False

    @staticmethod
    def calculate_nights(check_in_date, check_out_date):
        return (check_out_date - check_in_date).days


class HotelReservationApp:

    def save_reservations(self):
        filename = "reservations.csv"
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(script_dir, filename)
        self.reservation.save_reservations_to_csv(filename)
        self.show_message(f"Reservations saved to {filename}")
        self.root.destroy()

    def __init__(self, root):
        self.root = root
        self.reservation = Reservation()

        # GUI Elements
        self.check_in_label = ttk.Label(root, text="Fecha ingreso:")
        self.check_in_label.grid(row=0, column=0, padx=10, pady=5)
        self.check_in_entry = DateEntry(root)
        self.check_in_entry.grid(row=0, column=1, padx=10, pady=5)

        self.check_out_label = ttk.Label(root, text="Fecha salida")
        self.check_out_label.grid(row=1, column=0, padx=10, pady=5)
        self.check_out_entry = DateEntry(root)
        self.check_out_entry.grid(row=1, column=1, padx=10, pady=5)

        self.nights_label = ttk.Label(root, text="Cantidad noches:")
        self.nights_label.grid(row=2, column=0, padx=10, pady=5)
        self.nights_value = tk.StringVar()
        self.nights_entry = ttk.Entry(root, textvariable=self.nights_value, state="readonly")
        self.nights_entry.grid(row=2, column=1, padx=10, pady=5)

        self.room_type_label = ttk.Label(root, text="Tipo habitacion:")
        self.room_type_label.grid(row=3, column=0, padx=10, pady=5)
        self.room_type_value = tk.StringVar()
        self.room_type_combobox = ttk.Combobox(root, textvariable=self.room_type_value, values=["scl 1", "scl 2", "scl 3", "scl 4", "scl 5", "scl 6", "scl 7", "scl 8", "scl 9", "scl 10", "scl 11", "scl 12", "scl 13", "scl 14", "scl 15", "scl 16", "scl 17", "scl 18", "scl 19", "scl 20", "scl 21", "scl 22", "scl 23", "scl 24", "scl 25", "scl 26", "scl 27", "scl 28", "scl 29", "scl 30"])
        self.room_type_combobox.grid(row=3, column=1, padx=10, pady=5)

        self.room_status_label = ttk.Label(root, text="Status:")
        self.room_status_label.grid(row=4, column=0, padx=10, pady=5)
        self.room_status_value = tk.StringVar()
        self.room_status_combobox = ttk.Combobox(root, textvariable=self.room_status_value, values=["VS", "VL", "OS", "OL", "BLK"])
        self.room_status_combobox.grid(row=4, column=1, padx=10, pady=5)

        self.guest_name_label = ttk.Label(root, text="Nombre:")
        self.guest_name_label.grid(row=5, column=0, padx=10, pady=5)
        self.guest_name_entry = ttk.Entry(root)
        self.guest_name_entry.grid(row=5, column=1, padx=10, pady=5)

        self.id_number_label = ttk.Label(root, text="Numero cédula:")
        self.id_number_label.grid(row=6, column=0, padx=10, pady=5)
        self.id_number_entry = ttk.Entry(root)
        self.id_number_entry.grid(row=6, column=1, padx=10, pady=5)

        self.guest_preferences_label = ttk.Label(root, text="Guest Preferences:")
        self.guest_preferences_label.grid(row=7, column=0, padx=10, pady=5)
        self.guest_preferences_entry = ttk.Entry(root)
        self.guest_preferences_entry.grid(row=7, column=1, padx=10, pady=5)

        self.create_reservation_button = ttk.Button(root, text="Create Reservation", command=self.create_reservation)
        self.create_reservation_button.grid(row=8, column=0, padx=10, pady=5)

        self.print_reservation_button = ttk.Button(root, text="Print Reservation", command=self.print_reservation)
        self.print_reservation_button.grid(row=8, column=1, padx=10, pady=5)

        self.reservation_listbox = tk.Listbox(root)
        self.reservation_listbox.grid(row=9, column=0, columnspan=2, padx=10, pady=5)
        self.reservation_listbox.bind("<<ListboxSelect>>", self.update_selection)

        self.delete_button = ttk.Button(root, text="Delete Reservation", command=self.delete_reservation)
        self.delete_button.grid(row=10, column=0, padx=10, pady=5)

        self.new_reservation_button = ttk.Button(root, text="New Reservation", command=self.new_reservation)
        self.new_reservation_button.grid(row=10, column=1, padx=10, pady=5)

        # Populate existing reservations
        self.update_reservation_list()

    def create_reservation(self):
        check_in_date = self.check_in_entry.get_date()
        check_out_date = self.check_out_entry.get_date()
        room_type = self.room_type_value.get()
        room_status = self.room_status_value.get()
        guest_name = self.guest_name_entry.get()
        id_number = self.id_number_entry.get()
        guest_preferences = self.guest_preferences_entry.get()

        if check_in_date and check_out_date and room_type and room_status and guest_name and id_number:
            success = self.reservation.create_reservation(check_in_date, check_out_date, room_type, room_status, guest_name, id_number, guest_preferences)
            if success:
                self.update_reservation_list()
                self.clear_fields()
                self.calculate_nights()
                self.show_message("Reservation created successfully!")
            else:
                self.show_message("Failed to create reservation. Please try again.")
        else:
            self.show_message("Please fill in all required fields.")

    def delete_reservation(self):
        selected_index = self.reservation_listbox.curselection()
        if selected_index:
            index = int(selected_index[0])
            self.reservation.delete_reservation(index)
            self.update_reservation_list()
            self.clear_fields()
            self.show_message("Reservation deleted successfully.")

    def print_reservation(self):
        selected_index = self.reservation_listbox.curselection()
        if selected_index:
            index = int(selected_index[0])
            success = self.reservation.print_reservation(index)
            if success:
                self.show_message("Reservation printed successfully!")
            else:
                self.show_message("Failed to print reservation.")

    def new_reservation(self):
        self.clear_fields()

    def update_reservation_list(self):
        self.reservation_listbox.delete(0, tk.END)
        reservations = self.reservation.get_all_reservations()
        for reservation in reservations:
            guest_name = reservation["guest_name"]
            serial_number = reservation["serial_number"]
            self.reservation_listbox.insert(tk.END, f"{guest_name} ({serial_number})")

    def update_selection(self, event):
        selected_index = self.reservation_listbox.curselection()
        if selected_index:
            index = int(selected_index[0])
            reservations = self.reservation.get_all_reservations()
            reservation = reservations[index]
            self.check_in_entry.set_date(reservation["check_in_date"])
            self.check_out_entry.set_date(reservation["check_out_date"])
            self.room_type_value.set(reservation["room_type"])
            self.room_status_value.set(reservation["room_status"])
            self.guest_name_entry.delete(0, tk.END)
            self.guest_name_entry.insert(tk.END, reservation["guest_name"])
            self.id_number_entry.delete(0, tk.END)
            self.id_number_entry.insert(tk.END, reservation["id_number"])
            self.guest_preferences_entry.delete(0, tk.END)
            self.guest_preferences_entry.insert(tk.END, reservation["guest_preferences"])
            self.calculate_nights()

    def calculate_nights(self):
        check_in_date = self.check_in_entry.get_date()
        check_out_date = self.check_out_entry.get_date()
        if check_in_date and check_out_date:
            nights = self.reservation.calculate_nights(check_in_date, check_out_date)
            self.nights_value.set(nights)

    def clear_fields(self):
        self.check_in_entry.set_date(None)
        self.check_out_entry.set_date(None)
        self.room_type_value.set("")
        self.room_status_value.set("")
        self.guest_name_entry.delete(0, tk.END)
        self.id_number_entry.delete(0, tk.END)
        self.guest_preferences_entry.delete(0, tk.END)
        self.nights_value.set("")

    def show_message(self, message):
        messagebox.showinfo("Hotel Reservation App", message)


if __name__ == "__main__":
    root = tk.Tk()
    app = HotelReservationApp(root)
    root.protocol("WM_DELETE_WINDOW", app.save_reservations)  # Save reservations when the window is closed
    root.title('Aplicación de reserva de hotel')
    root.mainloop()