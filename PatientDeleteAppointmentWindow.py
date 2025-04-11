import customtkinter
from AppointmentStore import AppointmentStore

class PatientDeleteAppointmentWindow:
    def __init__(self, conn):
        self.conn = conn
        self.appointment_store = AppointmentStore(self.conn)
        self.window = None

    def show(self):
        self.window = customtkinter.CTkToplevel()
        self.window.title("Delete Appointment")
        self.window.geometry("400x300")

        customtkinter.CTkLabel(self.window, text="Enter Patient ID to delete appointments:").pack(pady=10)

        self.patient_id_entry = customtkinter.CTkEntry(self.window)
        self.patient_id_entry.pack(pady=10)

        self.status_label = customtkinter.CTkLabel(self.window, text="")
        self.status_label.pack(pady=5)

        delete_btn = customtkinter.CTkButton(self.window, text="Delete", command=self.delete_appointments_by_patient_id)
        delete_btn.pack(pady=20)

    def delete_appointments_by_patient_id(self):
        try:
            patient_id = int(self.patient_id_entry.get())
        except ValueError:
            self.status_label.configure(text="Invalid ID", text_color="red")
            return

        success = self.appointment_store.delete_by_patient_id(patient_id)
        if success:
            self.status_label.configure(text="Deleted successfully.", text_color="green")
        else:
            self.status_label.configure(text="No appointment found.", text_color="orange")
