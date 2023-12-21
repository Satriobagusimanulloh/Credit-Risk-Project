from credit_scoring_project.models.Model import CreditCandidateModel
import psycopg2
from typing import List

class CreditCandidateAction:

    def __init__(self, db_connection_string):
        self.db_connection_string = db_connection_string

    def is_valid_credit_candidate_id(self, cursor, person_id):
        cursor.execute("SELECT COUNT(*) FROM public.credit_candidate WHERE person_id = %s", (person_id,))
        count = cursor.fetchone()[0]
        return count > 0
    
    def add_credit_candidate(self, new_candidate) -> bool:
        try:
            conn = psycopg2.connect(self.db_connection_string)
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM public.credit_candidate")
            count = cursor.fetchone()[0]

            cursor.execute("SELECT person_id FROM public.credit_candidate ORDER BY person_id DESC LIMIT 1")
            last_id = cursor.fetchone()
            new_person_id = last_id[0] + 1 if last_id else 1
            
            cursor.execute(
                "INSERT INTO public.credit_candidate "
                "(person_id, person_age, person_income, person_home_ownership, person_emp_length, "
                "loan_intent, loan_grade, loan_amnt, loan_int_rate, loan_percent_income, "
                "cb_person_default_on_file, cb_person_cred_hist_length) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    new_person_id,
                    new_candidate.person_age,
                    new_candidate.person_income,
                    new_candidate.person_home_ownership,
                    new_candidate.person_emp_length,
                    new_candidate.loan_intent,
                    new_candidate.loan_grade,
                    new_candidate.loan_amnt,
                    new_candidate.loan_int_rate,
                    new_candidate.loan_percent_income,
                    new_candidate.cb_person_default_on_file,
                    new_candidate.cb_person_cred_hist_length
                )
            )

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Error: {str(e)}")
            return False

    def get_all_credit_candidates(self, order_by) -> List[CreditCandidateModel]:
        credit_candidates = []
        try:
            conn = psycopg2.connect(self.db_connection_string)
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM public.credit_candidate ORDER BY {order_by}")
            rows = cursor.fetchall()
            for row in rows:
                candidate = CreditCandidateModel()
                candidate.person_id = row[0]
                candidate.person_age = row[1]
                candidate.person_income = row[2]
                candidate.person_home_ownership = row[3]
                candidate.person_emp_length = row[4]
                candidate.loan_intent = row[5]
                candidate.loan_grade = row[6]
                candidate.loan_amnt = row[7]
                candidate.loan_int_rate = row[8]
                candidate.loan_percent_income = row[9]
                candidate.cb_person_default_on_file = row[10]
                candidate.cb_person_cred_hist_length = row[11]
                credit_candidates.append(candidate)
            conn.close()
                
        except Exception as e:
            print(f"Error: {str(e)}")
            return None
        return credit_candidates

    def get_by_id(self, person_id) -> CreditCandidateModel:
        try:
            conn = psycopg2.connect(self.db_connection_string)
            cursor = conn.cursor()

            if not self.is_valid_credit_candidate_id(cursor, person_id):
                conn.close()
                print("Error: person_id tidak ditemukan di tabel credit_candidate.")
                return False

            cursor.execute("SELECT * FROM public.credit_candidate WHERE person_id = %s", (person_id,))
            row = cursor.fetchone()
            if row:
                candidate = CreditCandidateModel()
                candidate.person_id = row[0]
                candidate.person_age = row[1]
                candidate.person_income = row[2]
                candidate.person_home_ownership = row[3]
                candidate.person_emp_length = row[4]
                candidate.loan_intent = row[5]
                candidate.loan_grade = row[6]
                candidate.loan_amnt = row[7]
                candidate.loan_int_rate = row[8]
                candidate.loan_percent_income = row[9]
                candidate.cb_person_default_on_file = row[10]
                candidate.cb_person_cred_hist_length = row[11]
                conn.close()
                return candidate
            else:
                conn.close()
                return None
                
        except Exception as e:
            print(f"Error: {str(e)}")
            return None

    def update_credit_candidate(self, person_id, new_data) -> bool:
        try:
            conn = psycopg2.connect(self.db_connection_string)
            cursor = conn.cursor()

            if not self.is_valid_credit_candidate_id(cursor, person_id):
                conn.close()
                print("Error: person_id tidak ditemukan di tabel credit_candidate.")
                return False

            cursor.execute(
                "UPDATE public.credit_candidate SET "
                "person_age=%s, person_income=%s, person_home_ownership=%s, person_emp_length=%s, "
                "loan_intent=%s, loan_grade=%s, loan_amnt=%s, loan_int_rate=%s, loan_percent_income=%s, "
                "cb_person_default_on_file=%s, cb_person_cred_hist_length=%s WHERE person_id=%s;",
                (
                    new_data.person_age,
                    new_data.person_income,
                    new_data.person_home_ownership,
                    new_data.person_emp_length,
                    new_data.loan_intent,
                    new_data.loan_grade,
                    new_data.loan_amnt,
                    new_data.loan_int_rate,
                    new_data.loan_percent_income,
                    new_data.cb_person_default_on_file,
                    new_data.cb_person_cred_hist_length,
                    person_id
                )
            )

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Error: {str(e)}")
            return False

    def delete_credit_candidate(self, person_id) -> bool:
        try:
            conn = psycopg2.connect(self.db_connection_string)
            cursor = conn.cursor()

            if not self.is_valid_credit_candidate_id(cursor, person_id):
                conn.close()
                print("Error: person_id tidak ditemukan di tabel credit_candidate.")
                return False

            cursor.execute("DELETE FROM public.credit_candidate WHERE person_id=%s", (person_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error: {str(e)}")
            return False