class Doctor:
    def __init__(self, name, surname, speciality, phone):
        self.name = name
        self.surname = surname
        self.speciality = speciality
        self.phone = phone

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
        res = cur.execute("SELECT * FROM Doctors WHERE id = ?", (id,))
        doctor = res.fetchone()
        return doctor

    def find_id_by_name(self, name, surname):
     cur = self.db.cursor()
     res = cur.execute("SELECT doctor_id FROM Doctors WHERE name = ? AND surname = ?", (name, surname))
     doctor = res.fetchone()
     return doctor[0] if doctor else None

    def update(self, id, name, surname, phone, speciality):
        cur = self.db.cursor()
        cur.execute("""
            UPDATE Doctors
            SET name = ?, surname = ?, specialty = ?, phone_number = ?
            WHERE id = ?
        """, (name, surname, phone, speciality, id))
        self.db.commit()

    def delete(self, id):
        cur = self.db.cursor()
        cur.execute("DELETE FROM Doctors WHERE id = ?", (id,))
        self.db.commit()