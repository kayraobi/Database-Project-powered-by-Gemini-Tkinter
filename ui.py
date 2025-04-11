import customtkinter
import sqlite3
from AppointmentStore import *
from AppointmentWindow import *
from SetAppointmentWindow import *
from DoctorLoginWindow import *
from PatientCreateWindow import *
from ChatbotWindow import *
from PatientDeleteAppointmentWindow import *  # Yeni eklenen pencere

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect("hospital3.db")
        self.appointment_store = AppointmentStore(self.conn)

        self.title("Hospital Appointment System")
        self.geometry("1100x580")

        self.set_appointment_btn = customtkinter.CTkButton(
            self, text="Set an Appointment", command=self.set_appointment)
        self.set_appointment_btn.grid(row=1, column=0, padx=20, pady=10)

        self.doctor_login_btn = customtkinter.CTkButton(
            self, text="Doctor Login", command=self.get_appointments_by_doc_id)
        self.doctor_login_btn.grid(row=2, column=0, padx=20, pady=10)

        self.chatbot_btn = customtkinter.CTkButton(
            self, text="Hospital Chatbot", command=self.open_chatbot)
        self.chatbot_btn.grid(row=3, column=0, padx=20, pady=10)

        self.get_appointments_btn = customtkinter.CTkButton(
            self, text="Appointments", command=self.get_appointments)
        self.get_appointments_btn.grid(row=4, column=0, padx=20, pady=10)

        self.id_create = customtkinter.CTkButton(
            self, text="Create your patient ID", command=self.set_patience)
        self.id_create.grid(row=5, column=0, padx=20, pady=10)

        self.delete_appointment_btn = customtkinter.CTkButton(
            self, text="Delete Appointment", command=self.open_delete_appointment)
        self.delete_appointment_btn.grid(row=6, column=0, padx=20, pady=10)

    def set_patience(self):
        print("Patient creation opening")
        self.patient_window = PatientCreateWindow(self.conn)
        self.patient_window.show()

    def set_appointment(self):
        print("Opening SetAppointmentWindow")
        set_appointment_window = SetAppointmentWindow(self.conn)
        set_appointment_window.show()

    def get_appointments(self):
        print("Opening AppointmentWindow")
        appointment_window = AppointmentWindow(self.conn)
        appointment_window.show()

    def get_appointments_by_doc_id(self):
        print("Opening DoctorLoginWindow")
        doc_appointment_window = DoctorLoginWindow(self.conn)
        doc_appointment_window.show()

    def open_chatbot(self):
        print("Opening ChatbotWindow")
        chatbot_window = ChatbotWindow()
        chatbot_window.show()

    def open_delete_appointment(self):
        print("Opening PatientDeleteAppointmentWindow")
        delete_window = PatientDeleteAppointmentWindow(self.conn)
        delete_window.show()

if __name__ == "__main__":
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")
    app = App()
    app.mainloop()
