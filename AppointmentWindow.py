import tkinter
import tkinter.messagebox
import customtkinter
from AppointmentStore import *
from tkinter import ttk  

class AppointmentWindow(customtkinter.CTk):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.appointment_store = AppointmentStore(self.conn)
        self.appointments = self.appointment_store.read_all()
        import tkinter


class AppointmentWindow(customtkinter.CTk):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.appointment_store = AppointmentStore(self.conn)
        self.appointments = self.appointment_store.read_all()
        
        self.title("Appointments")
        self.geometry("1100x580")

        # Treeview (tablo)
        self.tree = ttk.Treeview(self, columns=("ID", "Patient ID", "Doctor ID", "Date", "Start", "End", "Description"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Patient ID", text="Patient ID")
        self.tree.heading("Doctor ID", text="Doctor ID")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Start", text="Start Time")
        self.tree.heading("End", text="End Time")
        self.tree.heading("Description", text="Description")

        self.tree.grid(row=0, column=0, padx=20, pady=20)

        # Rescan button
        self.set_appointment_btn = customtkinter.CTkButton(self, text="Rescan", command=self.rescan_appointment)
        self.set_appointment_btn.grid(row=1, column=0, padx=20, pady=10)

        # İlk yükleme
        self.populate_table()

    def populate_table(self):
        # Önce tüm eski verileri temizle
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Yeniden yükle
        for appointment in self.appointments:
            self.tree.insert("", "end", values=appointment)

    def rescan_appointment(self):
        print("rescan_appointment called.")
        self.appointments = self.appointment_store.read_all()
        self.populate_table()
        
      
        # configure window
        self.title("Appointments")
        self.geometry(f"{1100}x{580}")
        self.table=tkinter.Frame(self,background = "#420000")

        self.set_appointment_btn = customtkinter.CTkButton(self, text="Rescan", command = self.rescan_appointment)
        self.set_appointment_btn.grid(row=1, column=0, padx=20, pady=10)

    def rescan_appointment(self):
        print("rescan_appointment called.")
        self.appointments = self.appointment_store.read_all()
      
    def show(self):
     self.lift()
     self.deiconify()   