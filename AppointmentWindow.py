import customtkinter
from tkinter import ttk
from AppointmentStore import AppointmentStore

class AppointmentWindow(customtkinter.CTk):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.appointment_store = AppointmentStore(self.conn)
        self.appointments = []

        self.title("Appointments")
        self.geometry("1100x580")

        self.tree = ttk.Treeview(
            self, 
            columns=("ID", "Patient Name", "Doctor ID", "Date", "Start", "End", "Description"), 
            show="headings"
        )
        for col in ("ID", "Patient Name", "Doctor ID", "Date", "Start", "End", "Description"):
            self.tree.heading(col, text=col)

        self.tree.grid(row=0, column=0, padx=20, pady=20)

        self.set_appointment_btn = customtkinter.CTkButton(self, text="Rescan", command=self.rescan_appointment)
        self.set_appointment_btn.grid(row=1, column=0, padx=20, pady=10)

        self.rescan_appointment()

    def populate_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for appointment in self.appointments:
            self.tree.insert("", "end", values=appointment)

    def rescan_appointment(self):
        self.appointments = self.appointment_store.read_all()
        self.populate_table()

    def show(self):
        self.lift()
        self.deiconify()
