from credit_scoring_project.models.Model import BankModel
import psycopg2
from typing import List

class BankAction:

    def __init__(self, db_connection_string):
        self.db_connection_string = db_connection_string

    def is_valid_person_id(self, cursor, person_id):
        cursor.execute("SELECT COUNT(*) FROM public.credit_candidate WHERE person_id = %s", (person_id,))
        count = cursor.fetchone()[0]
        return count > 0

    def add_bank_entry(self, new_entry) -> bool:
        try:
            conn = psycopg2.connect(self.db_connection_string)
            cursor = conn.cursor()

            if not self.is_valid_person_id(cursor, new_entry.person_id):
                conn.close()
                print("Error: person_id tidak ditemukan di tabel credit_candidate.")
                return False

            # cursor.execute(f"SELECT COUNT(*) FROM public.bank")
            # count = cursor.fetchone()[0]
            # new_person_id = count + 1

            cursor.execute(
                "INSERT INTO public.bank "
                "(person_id, loan_status) "
                "VALUES (%s, %s)",
                (
                    new_entry.person_id,
                    new_entry.loan_status
                )
            )

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Error: {str(e)}")
            return False

    def get_all_bank_entries(self, order_by) -> List[BankModel]:
        bank_entries = []
        try:
            conn = psycopg2.connect(self.db_connection_string)
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM public.bank ORDER BY {order_by}")
            rows = cursor.fetchall()
            for row in rows:
                entry = BankModel()
                entry.person_id = row[0]
                entry.loan_status = row[1]
                bank_entries.append(entry)
            conn.close()
                
        except Exception as e:
            print(f"Error: {str(e)}")
            return None
        return bank_entries

    def get_by_person_id(self, person_id) -> BankModel:
        try:
            conn = psycopg2.connect(self.db_connection_string)
            cursor = conn.cursor()

            if not self.is_valid_person_id(cursor, person_id):
                conn.close()
                print("Error: person_id tidak ditemukan di tabel credit_candidate.")
                return False

            cursor.execute("SELECT * FROM public.bank WHERE person_id = %s", (person_id,))
            row = cursor.fetchone()
            if row:
                entry = BankModel()
                entry.person_id = row[0]
                entry.loan_status = row[1]
                conn.close()
                return entry
            else:
                conn.close()
                return None
                
        except Exception as e:
            print(f"Error: {str(e)}")
            return None

    def update_bank_entry(self, person_id, new_data) -> bool:
        try:
            conn = psycopg2.connect(self.db_connection_string)
            cursor = conn.cursor()

            if not self.is_valid_person_id(cursor, person_id):
                conn.close()
                print("Error: person_id tidak ditemukan di tabel credit_candidate.")
                return False

            cursor.execute(
                "UPDATE public.bank SET "
                "loan_status=%s WHERE person_id=%s;",
                (
                    new_data.loan_status,
                    person_id # bukan error, tetapi saat mencoba ganti ID tidak bisa berubah
                )
            )

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Error: {str(e)}")
            return False

    def delete_bank_entry(self, person_id) -> bool:
        try:
            conn = psycopg2.connect(self.db_connection_string)
            cursor = conn.cursor()

            if not self.is_valid_person_id(cursor, person_id):
                conn.close()
                print("Error: person_id tidak ditemukan di tabel credit_candidate.")
                return False

            cursor.execute("DELETE FROM public.bank WHERE person_id=%s", (person_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error: {str(e)}")
            return False