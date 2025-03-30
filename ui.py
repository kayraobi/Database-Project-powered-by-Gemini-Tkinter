import customtkinter
import sqlite3
from AppointmentStore import *
from AppointmentWindow import *
from SetAppointmentWindow import *
from SetAppointmentWindow import *

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect("hospital3.db")
        self.appointment_store = AppointmentStore(self.conn)
       

        self.title("Hospital Appointment System")
        self.geometry("1100x580")

        # Set Appointment Button
        self.set_appointment_btn = customtkinter.CTkButton(
            self, text="Set an Appointment", command=self.set_appointment)
        self.set_appointment_btn.grid(row=1, column=0, padx=20, pady=10)
        


        # Get Appointments Button
        self.get_appointments_btn = customtkinter.CTkButton(
            self, text="Appointments", command=self.get_appointments)
        self.get_appointments_btn.grid(row=2, column=0, padx=20, pady=10)

        # Create Patient Button
        self.id_create = customtkinter.CTkButton(
            self, text="Create your patient id", command=self.set_patience
        )
        self.id_create.grid(row=3, column=0, padx=20, pady=10)

    def set_patience(self):
        print("patient creation opening")
        # set_patience_window = PatientStore(self.conn)
        # set_patience_window.show()

    def set_appointment(self):
        print("Opening SetAppointmentWindow")
        set_appointment_window = SetAppointmentWindow(self.conn)
        set_appointment_window.show()

    def get_appointments(self):
        print("Opening AppointmentWindow")
        appointment_window = AppointmentWindow(self.conn)
        appointment_window.show()

if __name__ == "__main__":
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")
    app = App()
    app.mainloop()