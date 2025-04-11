import customtkinter
from tkinter import StringVar
from DoctorStore import *
from AppointmentStore import Appointments, AppointmentStore

class DoctorLoginWindow:
    def __init__(self, conn):
        self.conn = conn
        self.appointment_store = AppointmentStore(self.conn)
        self.doc_store = DoctorStore(self.conn)

    def show(self):
        window = customtkinter.CTkToplevel()
        window.title("Doctor Login")
        window.geometry("400x450")

        def only_numbers(input_str):
            return input_str.isdigit() or input_str == ""

        vcmd_numbers = (window.register(only_numbers), '%P')

        # Giriş başlığı
        label = customtkinter.CTkLabel(window, text="Enter Doctor ID:")
        label.pack(pady=10)

        # ID giriş kutusu
        self.doc_id_var = StringVar()
        self.doc_id_entry = customtkinter.CTkEntry(
            window,
            textvariable=self.doc_id_var,
            validate="key",
            validatecommand=vcmd_numbers
        )
        self.doc_id_entry.pack(pady=5)

        
        submit_btn = customtkinter.CTkButton(window, text="Get Appointments", command=self.load_appointments)
        submit_btn.pack(pady=10)


        self.result_box = customtkinter.CTkTextbox(window, width=350, height=300)
        self.result_box.pack(pady=10)

    def load_appointments(self):
        doc_id = self.doc_id_var.get()

        if not doc_id:
            self.result_box.delete("0.0", "end")
            self.result_box.insert("0.0", "Please enter a doctor ID.\n")
            return

        try:
          
            appointments = self.appointment_store.read_by_doctor_id(int(doc_id))
            self.result_box.delete("0.0", "end")

            if not appointments:
                self.result_box.insert("0.0", f"No appointments found for Doctor ID: {doc_id}")
            else:
                for app in appointments:
                    self.result_box.insert("end",
                        f"Appointment ID: {app[0]}\n"
                        f"Patient: {app[1]}\n"
                        f"Date: {app[2]} | {app[3]} - {app[4]}\n"
                        f"Description: {app[5]}\n\n"
                    )

        except Exception as e:
            self.result_box.insert("0.0", f"Error: {str(e)}\n")