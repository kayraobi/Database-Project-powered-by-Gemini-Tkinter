import sqlite3

class Patient:
    def __init__(self, name, surname, phonenumber):
        self.name = name
        self.surname = surname
        self.phonenumber = phonenumber

class PatientStore:
    def __init__(self, db):
        self.db = db

    def create(self, patient):  
        cur = self.db.cursor()
        cur.execute("""
            INSERT INTO Patients (name, surname, phonenumber)
            VALUES (?, ?, ?)
        """, (patient.name, patient.surname, patient.phonenumber))
        self.db.commit()
        return cur.lastrowid  

    def read_all(self):
        cur = self.db.cursor()
        res = cur.execute("SELECT * FROM Appointments")
        Appointments = res.fetchall()
        return Appointments

    def read_by_id(self, id):
        cur = self.db.cursor()
        res = cur.execute("SELECT * FROM Appointments WHERE id = ?", (id,))
        doctor = res.fetchone()
        return doctor

    def delete(self, id):
        cur = self.db.cursor()
        cur.execute("DELETE FROM Appointments WHERE id = ?", (id,))
        self.db.commit()