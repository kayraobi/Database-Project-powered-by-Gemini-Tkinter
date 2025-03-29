import sqlite3



class Appointments:
    def __init__(self, patient_id, doctor_id, appointment_date, start_time, end_time, description):
         self.patient_id = patient_id
         self.doctor_id = doctor_id
         self.appointment_date = appointment_date
         self.start_time = start_time
         self.end_time = end_time
         self.description = description

    
# db = ...
# doc_s = DoctorStore(db)
# doc_s.create(...)
# doc_s.read_all()
# doc_s.read_by_id(1)
# doc_s.update(...)
# doc_s.delete(1)
class AppointmentStore:
    def __init__(self, db):
        self.db = db

    def create(self, appointment):  # <-- DİKKAT: bu def artık sınıfın İÇİNDE ✅
        cur = self.db.cursor()

        # Çakışan randevu var mı kontrol et
        cur.execute("""
            SELECT * FROM Appointments
            WHERE doctor_id = ?
            AND appointment_date = ?
            AND (
                (? < end_time AND ? > start_time)
                OR
                (? < end_time AND ? > start_time)
                OR
                (? <= start_time AND ? >= end_time)
            )
        """, (
            appointment.doctor_id,
            appointment.appointment_date,
            appointment.start_time, appointment.start_time,
            appointment.end_time, appointment.end_time,
            appointment.start_time, appointment.end_time
        ))

        conflict = cur.fetchone()
        if conflict:
            print("Randevu çakışması: Bu saat aralığında zaten bir randevu var.")
            return False

        cur.execute("""
            INSERT INTO Appointments (patient_id, doctor_id, appointment_date, start_time, end_time, description)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            appointment.patient_id,
            appointment.doctor_id,
            appointment.appointment_date,
            appointment.start_time,
            appointment.end_time,
            appointment.description
        ))

        self.db.commit()
        print("Randevu başarıyla eklendi.")
        return True

    def read_all(self):
        cur = self.db.cursor()
        res = cur.execute("SELECT * FROM Appointments")
        Appointments = res.fetchall()
        return Appointments

    def read_by_id(self, id):
        cur = self.db.cursor()
        res = cur.execute("SELECT * FROM Appointments WHERE id = ?", (id))
        doctor = res.fetchone()
        return doctor
    
    def delete(self, id):
        cur = self.db.cursor()
        cur.execute("DELETE FROM Appointments WHERE id = ?", (id))
        cur.commit()
        
        