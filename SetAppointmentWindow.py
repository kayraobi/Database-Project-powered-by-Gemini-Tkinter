import customtkinter
from tkinter import StringVar
from DoctorStore import *
from AppointmentStore import Appointments, AppointmentStore
import re
from datetime import datetime

class SetAppointmentWindow:
    def __init__(self, conn):
        self.conn = conn
        self.window = None
        self.appointment_store = AppointmentStore(self.conn)
        self.doc_store = DoctorStore(self.conn)

    def show(self):
        self.window = customtkinter.CTkToplevel()
        self.window.title("Create Appointment")
        self.window.geometry("400x600")

        def on_close():
            self.window.destroy()
            # Let your main app set this window reference to None

        self.window.protocol("WM_DELETE_WINDOW", on_close)

        # Input validators
        def only_numbers(input_str):
            return input_str.isdigit() or input_str == ""

        def valid_date_input(new_value):
            return re.match(r"^[0-9\-]*$", new_value) is not None

        def valid_time_input(new_value):
            return re.match(r"^[0-9:]*$", new_value) is not None

        def validate_date_format(date_str):
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                return date_obj.year == 2025
            except ValueError:
                return False

        def validate_time_format(time_str):
            try:
                dt = datetime.strptime(time_str, "%H:%M")
                return 0 <= dt.hour <= 23 and 0 <= dt.minute <= 59
            except ValueError:
                return False

        # Register input validation
        vcmd_numbers = (self.window.register(only_numbers), '%P')
        vcmd_date = (self.window.register(valid_date_input), '%P')
        vcmd_time = (self.window.register(valid_time_input), '%P')

        # Fetch doctor list
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, surname FROM Doctors")
        rows = cursor.fetchall()
        doctor_list = [f"{row[0]} {row[1]}" for row in rows] or ["No doctors found"]
        selected_doctor = StringVar(value=doctor_list[0])

        # UI Elements
        customtkinter.CTkLabel(self.window, text="Select Doctor", font=("Arial", 14)).pack(pady=10)
        dropdown = customtkinter.CTkOptionMenu(self.window, variable=selected_doctor, values=doctor_list)
        dropdown.pack(pady=5)

        customtkinter.CTkLabel(self.window, text="Patient ID").pack(pady=5)
        patient_id_entry = customtkinter.CTkEntry(self.window, validate="key", validatecommand=vcmd_numbers)
        patient_id_entry.pack()

        customtkinter.CTkLabel(self.window, text="Date (YYYY-MM-DD)").pack(pady=5)
        date_entry = customtkinter.CTkEntry(self.window, validate="key", validatecommand=vcmd_date)
        date_entry.pack()

        customtkinter.CTkLabel(self.window, text="Start time (HH:MM)").pack(pady=5)
        start_entry = customtkinter.CTkEntry(self.window, validate="key", validatecommand=vcmd_time)
        start_entry.pack()

        customtkinter.CTkLabel(self.window, text="End time (HH:MM)").pack(pady=5)
        end_entry = customtkinter.CTkEntry(self.window, validate="key", validatecommand=vcmd_time)
        end_entry.pack()

        customtkinter.CTkLabel(self.window, text="Description").pack(pady=5)
        desc_entry = customtkinter.CTkEntry(self.window)
        desc_entry.pack()

        error_label = customtkinter.CTkLabel(self.window, text="", text_color="red")
        error_label.pack(pady=5)

        def handle_submit():
            print(">>> Submit clicked!")

            # Validate patient ID
            try:
                patient_id = int(patient_id_entry.get())
            except ValueError:
                error_label.configure(text="Invalid patient ID")
                return

            # Ensure patient exists
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM Patients WHERE patient_id = ?", (patient_id,))
            patient = cur.fetchone()
            if not patient:
                error_label.configure(text="Patient not found")
                return

            # Collect form inputs
            full_name = selected_doctor.get()
            date = date_entry.get()
            start = start_entry.get()
            end = end_entry.get()
            desc = desc_entry.get()

            # Validate date
            if not validate_date_format(date):
                error_label.configure(text="Invalid date format (YYYY-MM-DD, year must be 2025)")
                return

            # Validate time format
            if not validate_time_format(start) or not validate_time_format(end):
                error_label.configure(text="Invalid time format (HH:MM)")
                return

            # Check if start time is before end time
            start_dt = datetime.strptime(start, "%H:%M")
            end_dt = datetime.strptime(end, "%H:%M")
            if start_dt >= end_dt:
                error_label.configure(text="Start time must be before end time")
                return

            try:
                # Find doctor ID
                parts = full_name.strip().split(" ")
                name = " ".join(parts[:-1])
                surname = parts[-1]
                doctor_id = self.doc_store.find_id_by_name(name, surname)

                if doctor_id is None:
                    error_label.configure(text="Doctor not found")
                    return

                # Create appointment object
                appointment = Appointments(
                    patient_id=patient_id,
                    doctor_id=doctor_id,
                    appointment_date=date,
                    start_time=start,
                    end_time=end,
                    description=desc
                )

                # Try to insert into DB
                success = self.appointment_store.create(appointment)

                if success:
                    print("Appointment successfully created")
                    self.window.destroy()
                else:
                    error_label.configure(text="Time conflict! Appointment not created.")

            except Exception as e:
                print(f">>> EXCEPTION in handle_submit: {e}")
                error_label.configure(text=f"Error: {e}")

        # Submit button
        customtkinter.CTkButton(self.window, text="Create Appointment", command=handle_submit).pack(pady=15)