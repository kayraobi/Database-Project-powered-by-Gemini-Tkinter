import sqlite3


# db = ...
# doc_s = DoctorStore(db)
# doc_s.create(...)
# doc_s.read_all()
# doc_s.read_by_id(1)
# doc_s.update(...)
# doc_s.delete(1)
#

class Doctor:
    def __init__(self, name, surname, speciality, phone):
         self.name=name
         self.surname=surname
         self.speciality=speciality
         self.phone=phone
    
    
class DoctorStore:
    def __init__(self, db):
        self.db = db
       
    def create(self, doc_s):
        cur = self.db.cursor()
        cur.execute("""
            INSERT INTO Doctors (name, surname, specialty, phone_number)
            VALUES (?, ?, ?, ?)
            """, (doc_s.name, doc_s.surname, doc_s.speciality, doc_s.phone))
        self.db.commit()

    def read_all(self):
        cur = self.db.cursor()
        res = cur.execute("SELECT * FROM Doctors")
        doctors = res.fetchall()
        return doctors

    def read_by_id(self, id):
        cur = self.db.cursor()
        res = cur.execute("SELECT * FROM Doctors WHERE id = ?", (id))
        doctor = res.fetchone()
        return doctor
    
    def find_id_by_name(self, name):
     cur = self.db.cursor()
     res = cur.execute("SELECT * FROM Doctors WHERE name = ?", (name))
     doctor = res.fetchone()
     return doctor
        
         

    def update(self, id, name, surname, phone, speciality):
        cur = self.db.cursor()
        cur.execute("""
            UPDATE Doctors
            SET name = ?, surname = ?, specialty = ?, phone_number = ?
            WHERE id = ?
            """, (name, surname, phone, speciality, id))
        cur.commit()
    
    def delete(self, id):
        cur = self.db.cursor()
        cur.execute("DELETE FROM Doctors WHERE id = ?", (id))
        cur.commit()
        
        