import tkinter
import customtkinter
from tkinter import ttk
from AppointmentStore import *
from tkinter import *

class SetAppointmentWindow(customtkinter.CTk):  
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.appointment_store = AppointmentStore(self.conn)

        self.title("Set Appointment")
        self.geometry("600x600")

        # Form frame
        form_frame = ttk.Frame(self)
        form_frame.pack(padx=20, pady=20, fill="x")

        # Validasyon fonksiyonları
        def only_letters(input_str):
            return input_str.isalpha() or input_str == ""

        def only_numbers(input_str):
            return input_str.isdigit() or input_str == ""

        def validate_date_format(date_str):
            import re
            pattern = r"^\d{4}-\d{2}-\d{2}$"
            return re.match(pattern, date_str) is not None

        def valid_date_input(new_value):
            import re
            return re.match(r"^[0-9\-]*$", new_value) is not None

        def valid_time_input(new_value):
            import re
            return re.match(r"^[0-9:]*$", new_value) is not None

        # Validasyon bağlamaları
        vcmd_letters = (self.register(only_letters), '%P')
        vcmd_numbers = (self.register(only_numbers), '%P')
        vcmd_date = (self.register(valid_date_input), '%P')
        vcmd_time = (self.register(valid_time_input), '%P')

        # ID
        ttk.Label(form_frame, text="Patient ID:").pack(anchor="w")
        self.id_entry = ttk.Entry(form_frame, validate="key", validatecommand=vcmd_numbers)
        self.id_entry.pack(fill="x", pady=5)

        # Date
        ttk.Label(form_frame, text="Date (YYYY-MM-DD):").pack(anchor="w")
        self.date_entry = ttk.Entry(form_frame, validate="key", validatecommand=vcmd_date)
        self.date_entry.pack(fill="x", pady=5)

        self.date_error_label = ttk.Label(form_frame, text="", foreground="red")
        self.date_error_label.pack(anchor="w")

        # Start Time
        ttk.Label(form_frame, text="Start Time (HH:MM):").pack(anchor="w")
        self.start_entry = ttk.Entry(form_frame, validate="key", validatecommand=vcmd_time)
        self.start_entry.pack(fill="x", pady=5)

        # End Time
        ttk.Label(form_frame, text="End Time (HH:MM):").pack(anchor="w")
        self.end_entry = ttk.Entry(form_frame, validate="key", validatecommand=vcmd_time)
        self.end_entry.pack(fill="x", pady=5)

        # Doctor Dropdown
        ttk.Label(form_frame, text="Doctor:").pack(anchor="w")
        cursor = self.conn.cursor()
        cursor.execute("SELECT doctor_id, name FROM Doctors")
        self.doctor_dict = {name: doc_id for doc_id, name in cursor}
        doctor_names = list(self.doctor_dict.keys())

        if not doctor_names:
         doctor_names = ["No doctors found"]
         self.doctor_dict = {"No doctors found": -1}

        self.doctor_var = StringVar()
        self.doctor_var.set(doctor_names[0])
        
        self.doctor_combo = ttk.Combobox(form_frame, textvariable=self.doctor_var, values=doctor_names)
        self.doctor_combo.pack(fill="x", pady=5)
  
  
  




        # Problem Description
        ttk.Label(form_frame, text="Describe the Problem:").pack(anchor="w")
        self.problem_text = tkinter.Text(form_frame, height=4)
        self.problem_text.pack(fill="x", pady=5)

        # Submit Button
        self.submit_btn = customtkinter.CTkButton(
            self,
            text="Submit Appointment",
            command=self.submit_appointment
        )
        self.submit_btn.pack(pady=20)

    def submit_appointment(self):
        try:
            patient_id = int(self.id_entry.get())
        except ValueError:
            print("Invalid patient ID.")
            return
        doctor_name = self.doctor_var.get()  # önce isim alınır
        doctor_id = self.doctor_dict.get(doctor_name, -1)  # sonra ID alınır
        date = self.date_entry.get()
        start = self.start_entry.get()
        end = self.end_entry.get()
        doctor_name = self.doctor_var.get()
        problem = self.problem_text.get("1.0", "end").strip()

        def validate_date_format(date_str):
            import re
            pattern = r"^\d{4}-\d{2}-\d{2}$"
            return re.match(pattern, date_str) is not None

        if not validate_date_format(date):
            self.date_error_label.config(text="Date must be in YYYY-MM-DD format")
            return
        else:
            self.date_error_label.config(text="")

        print("Appointment submitted:")
        print(f"Patient ID: {patient_id}")
        print(f"Date: {date}, Time: {start} - {end}")
        print(f"Doctor: {doctor_id}")
        print(f"Problem: {problem}")


        appointment = Appointments(
            patient_id=patient_id,
            doctor_id=doctor_id,
            appointment_date=date,
            start_time=start,
            end_time=end,
            description=problem
        )

        self.appointment_store.create(appointment)
        print("Appointment saved to database.")

    def show(self):
        self.lift()
        self.deiconify()