import sqlite3
import customtkinter
from PatientStore import PatientStore, Patient

class PatientCreateWindow:
    def __init__(self, conn):
        self.conn = conn
        self.patient_store = PatientStore(self.conn)

    def show(self):
        # Yeni pencere oluştur
        window = customtkinter.CTkToplevel()
        window.title("Randevu Ekle")
        window.geometry("400x550")

        # Form elemanları yeni pencereye (window) ekleniyor
        form_frame = customtkinter.CTkFrame(window)
        form_frame.pack(padx=20, pady=20)

        self.name_entry = customtkinter.CTkEntry(form_frame, placeholder_text="Name")
        self.name_entry.pack(pady=5)

        self.surname_entry = customtkinter.CTkEntry(form_frame, placeholder_text="Surname")
        self.surname_entry.pack(pady=5)

        self.phone_entry = customtkinter.CTkEntry(form_frame, placeholder_text="Phone Number")
        self.phone_entry.pack(pady=5)


        submit_btn = customtkinter.CTkButton(form_frame, text="Submit", command=self.submit_patient)
        submit_btn.pack(pady=10)

        self.result_label = customtkinter.CTkLabel(form_frame, text="")
        self.result_label.pack()

    def submit_patient(self):
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        phone = self.phone_entry.get()


        if not (name and surname and phone ):
            self.result_label.configure(text="Please fill all fields", text_color="red")
            return

        patient = Patient(name, surname, phone)
        patient_id = self.patient_store.create(patient)

        self.result_label.configure(
            text=f"Patient added successfully! ID: {patient_id}",
            text_color="green"
        )
        self.clear_form()

    def clear_form(self):
        self.name_entry.delete(0, 'end')
        self.surname_entry.delete(0, 'end')
        self.phone_entry.delete(0, 'end')
