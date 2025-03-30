import customtkinter
from tkinter import StringVar
from DoctorStore import *
from AppointmentStore import Appointments, AppointmentStore
import re
from datetime import datetime

class SetAppointmentWindow:
    def __init__(self, conn):
        self.conn = conn
        self.appointment_store = AppointmentStore(self.conn)
        self.doc_store = DoctorStore(self.conn)

    def show(self):
        window = customtkinter.CTkToplevel()
        window.title("Randevu Ekle")
        window.geometry("400x550")

        def only_letters(input_str):
            return input_str.isalpha() or input_str == ""

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
                hour, minute = dt.hour, dt.minute
                return 0 <= hour <= 23 and 0 <= minute <= 59
            except ValueError:
                return False

        vcmd_letters = (window.register(only_letters), '%P')
        vcmd_numbers = (window.register(only_numbers), '%P')
        vcmd_date = (window.register(valid_date_input), '%P')
        vcmd_time = (window.register(valid_time_input), '%P')

        # Doktorları çek
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, surname FROM Doctors")
        rows = cursor.fetchall()
        doctor_list = [f"{row[0]} {row[1]}" for row in rows]
        if not doctor_list:
            doctor_list = ["No doctors found"]

        selected_doctor = StringVar(value=doctor_list[0])

        # UI bileşenleri
        customtkinter.CTkLabel(window, text="Select Doctor", font=("Arial", 14)).pack(pady=10)
        dropdown = customtkinter.CTkOptionMenu(window, variable=selected_doctor, values=doctor_list)
        dropdown.pack(pady=5)

        customtkinter.CTkLabel(window, text="Tarih (YYYY-MM-DD)").pack(pady=5)
        date_entry = customtkinter.CTkEntry(window, validate="key", validatecommand=vcmd_date)
        date_entry.pack()

        customtkinter.CTkLabel(window, text="Beginning time (HH:MM)").pack(pady=5)
        start_entry = customtkinter.CTkEntry(window, validate="key", validatecommand=vcmd_time)
        start_entry.pack()

        customtkinter.CTkLabel(window, text="Ending time (HH:MM)").pack(pady=5)
        end_entry = customtkinter.CTkEntry(window, validate="key", validatecommand=vcmd_time)
        end_entry.pack()

        customtkinter.CTkLabel(window, text="Description").pack(pady=5)
        desc_entry = customtkinter.CTkEntry(window)
        desc_entry.pack()

        error_label = customtkinter.CTkLabel(window, text="", text_color="red")
        error_label.pack(pady=5)

        def handle_submit():
            full_name = selected_doctor.get()
            date = date_entry.get()
            start = start_entry.get()
            end = end_entry.get()
            desc = desc_entry.get()

            if not doctor_list:
              error_label.configure(text="Doktor bulunamadı.")
              return

            if not validate_date_format(date):
                error_label.configure(text="Invalid time")
                return

            if not validate_time_format(start) or not validate_time_format(end):
                error_label.configure(text="Time format is invalid")
                return

            try:
                name, surname = full_name.split(" ", 1)
                doctor_id = self.doc_store.find_id_by_name(name, surname)

                if doctor_id is None:
                    error_label.configure(text="No doctors found")
                    return

                appointment = Appointments(
                    patient_id=123,
                    doctor_id=doctor_id,
                    appointment_date=date,
                    start_time=start,
                    end_time=end,
                    description=desc
                )

                self.appointment_store.create(appointment)
                print("Appointment created successfully")
                window.destroy()

            except Exception as e:
                error_label.configure(text=f"Hata: {e}")

        submit_btn = customtkinter.CTkButton(window, text="Create Appointment", command=handle_submit)
        submit_btn.pack(pady=15)