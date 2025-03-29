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
    
        

        self.title("Create Patient Id")
        self.geometry("600x600")

        # Form frame
        form_frame = ttk.Frame(self)
        form_frame.pack(padx=20, pady=20, fill="x")