class Appointments:
    def __init__(self, patient_id, doctor_id, appointment_date, start_time, end_time, description):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.appointment_date = appointment_date
        self.start_time = start_time
        self.end_time = end_time
        self.description = description


class AppointmentStore:
    def __init__(self, db):
        self.db = db

    def create(self, appointment):
        cur = self.db.cursor()
        try:
            if appointment.start_time >= appointment.end_time:
                print(">>> Warning: Beginning hours cant be ahead from Ending hours")
                return False

            print(f">>> Checking for conflicts on {appointment.appointment_date} "
                  f"from {appointment.start_time} to {appointment.end_time} for doctor {appointment.doctor_id}")

            cur.execute("""
                SELECT * FROM Appointments
                WHERE doctor_id = ?
                AND appointment_date = ?
                AND (
                    start_time < ? AND end_time > ?
                )
            """, (
                appointment.doctor_id,
                appointment.appointment_date,
                appointment.end_time,
                appointment.start_time
            ))

            conflict = cur.fetchone()
            print(">>> SQL conflict result:", conflict)

            if conflict:
                print(">>> Appointment Clash Detected!")
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
            print(">>> Randevu başarıyla eklendi.")
            return True

        except Exception as db_error:
            print(">>> DB INSERT ERROR:", db_error)
            return False

    def read_all(self):
        cur = self.db.cursor()
        res = cur.execute("""
            SELECT 
                a.appointment_id,
                COALESCE(p.name || ' ' || p.surname, a.patient_id) AS patient_name,
                a.doctor_id,
                a.appointment_date,
                a.start_time,
                a.end_time,
                a.description
            FROM Appointments a
            LEFT JOIN Patients p ON a.patient_id = p.patient_id
        """)
        return res.fetchall()

    def read_by_doctor_id(self, doctor_id):
        cur = self.db.cursor()
        res = cur.execute("""
            SELECT 
                a.appointment_id,
                COALESCE(p.name || ' ' || p.surname, a.patient_id) AS patient_name,
                a.appointment_date,
                a.start_time,
                a.end_time,
                a.description
            FROM Appointments a
            LEFT JOIN Patients p ON a.patient_id = p.patient_id
            WHERE a.doctor_id = ?
        """, (doctor_id,))
        return res.fetchall()
