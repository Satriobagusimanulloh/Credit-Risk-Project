import os
from fastapi import FastAPI, HTTPException
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

from credit_scoring_project.models.ModelAPI import CreditCandidateModel, BankModel
from credit_scoring_project.services.BankService import BankAction
from credit_scoring_project.services.CreditCandidateService import CreditCandidateAction
from credit_scoring_project.machinelearning.MachineLearningProduce import Algorithm, MachineLearningProduce

app = FastAPI()
model_path_hardcoded = "/Users/satrio/Documents/Credit_Scoring_Project/credit-scoring-project/upload/model/model_credit_risk.pkl"
ml_model = joblib.load(model_path_hardcoded)

db_connection_string = "dbname=db_creditscoring user=postgres password=password host=localhost port=5438"
table_credit_candidate = "credit_candidate"
credit_candidate_db = CreditCandidateAction(db_connection_string)
db_connection_string = "dbname=db_creditscoring user=postgres password=password host=localhost port=5438"
table_bank = "bank"
bank_db = BankAction(db_connection_string)

@app.get("/")
def read_root():
    return {"message": "Selamat datang di API Credit Scoring!"}

@app.post("/credit_candidates")
async def add_credit_candidate(new_candidate : CreditCandidateModel):
    try:
        new_credit_candidate = credit_candidate_db.add_credit_candidate(new_candidate)
        if new_credit_candidate:
            return {"message": "Kandidat kredit berhasil ditambahkan"}
        else:
            raise HTTPException(status_code=400, detail="Gagal menambahkan kandidat kredit")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Gagal menambahkan data kandidat kredit: {str(e)}")

@app.get("/credit_candidates")
async def get_all_credit_candidates():
    candidates = credit_candidate_db.get_all_credit_candidates("person_id")
    return candidates

@app.get("/credit_candidates/{person_id}")
async def get_by_id(person_id : int):
    retrieved_candidate = credit_candidate_db.get_by_id(person_id)
    if retrieved_candidate:
        return retrieved_candidate
    else:
        raise HTTPException(status_code=404, detail="Kandidat kredit tidak ditemukan")
    
@app.put("/credit_candidates/{person_id}")
async def update_credit_candidate(person_id : int, new_candidate : CreditCandidateModel):
    try:
        updated_credit_candidate = credit_candidate_db.update_credit_candidate(person_id, new_candidate)
        if updated_credit_candidate:
            return {"message": "Kandidat kredit berhasil diperbarui!"}
        else:
            raise HTTPException(status_code=400, detail="Gagal memperbarui kandidat kredit!")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Gagal memperbarui kandidat kredit: {str(e)}")
    
@app.delete("/credit_candidates/{person_id}")
async def delete_credit_candidate(person_id : int):
    try:
        deleted_credit_candidate = credit_candidate_db.delete_credit_candidate(person_id)
        if deleted_credit_candidate:
            return {"message": f"Data person ID {person_id} berhasil dihapus!"}
        else:
            raise HTTPException(status_code=400, detail=f"Gagal menghapus data person ID {person_id}!")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Gagal menghapus data person ID {person_id}: {str(e)}")

 
"""
API untuk CRUD BANK
"""


    
@app.post("/bank_entries")
async def add_bank_entry(new_entry: BankModel):
    try:
        added_entry = bank_db.add_bank_entry(new_entry)
        if added_entry:
            return {"message": "Data bank berhasil ditambahkan"}
        else:
            raise HTTPException(status_code=400, detail="Gagal menambahkan data bank")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Gagal menambahkan data bank: {str(e)}")

@app.get("/bank_entries")
async def get_all_bank_entries():
    banks = bank_db.get_all_bank_entries("person_id")
    return banks

@app.get("/bank_entries/{person_id}")
async def get_by_person_id(person_id: int):
    entry = bank_db.get_by_person_id(person_id)
    if entry:
        return entry
    else:
        raise HTTPException(status_code=404, detail="Data bank tidak ditemukan")

@app.put("/bank_entries/{person_id}")
async def update_bank_entry(person_id: int, new_entry: BankModel):
    try:
        updated_entry = bank_db.update_bank_entry(person_id, new_entry)
        if updated_entry:
            return {"message": "Data bank berhasil diperbarui!"}
        else:
            raise HTTPException(status_code=400, detail="Gagal memperbarui data bank!")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Gagal memperbarui data bank: {str(e)}")

@app.delete("/bank_entries/{person_id}")
async def delete_bank_entry(person_id: int):
    try:
        deleted_entry = bank_db.delete_bank_entry(person_id)
        if deleted_entry:
            return {"message": f"Data bank dengan person ID {person_id} berhasil dihapus!"}
        else:
            raise HTTPException(status_code=400, detail=f"Gagal menghapus data bank dengan person ID {person_id}!")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Gagal menghapus data bank dengan person ID {person_id}: {str(e)}")
    

"""
API untuk membuat prediksi
"""


@app.post("/credit_candidates_and_predict")
async def add_credit_candidate_and_predict(new_candidate: CreditCandidateModel):
    try:
        new_credit_candidate = credit_candidate_db.add_credit_candidate(new_candidate)
        if not new_credit_candidate:
            raise HTTPException(status_code=400, detail="Failed to add credit candidate")

        input_data = pd.DataFrame([new_candidate.dict()]).drop(columns=["person_id"])

        preprocessor = MachineLearningProduce(algorithm=Algorithm.RANDOM_FOREST, model=None)
        input_data_processed = preprocessor.data_cleaning_preprocessing(
            input_data, log_features=['person_age', 'person_emp_length'], categorical_features=['person_home_ownership', 'loan_intent', 'loan_grade', 'cb_person_default_on_file']
        )

        predictions = preprocessor.make_predict(ml_model, input_data_processed)

        result = bank_db.add_bank_entry(BankModel(person_id=new_candidate.person_id, loan_status=int(predictions[0])))
        if result:
            return {"message": "Credit candidate added and prediction saved to the bank table"}
        else:
            raise HTTPException(status_code=400, detail="Failed to save prediction to the bank table")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process credit candidate and make prediction: {str(e)}")
