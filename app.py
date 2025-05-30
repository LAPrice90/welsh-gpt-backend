# app.py  – FastAPI micro-service
import pandas as pd
from fastapi import FastAPI, HTTPException

df = pd.read_excel("data/welsh_vocab.xlsx", engine="openpyxl")
CORE_SET = {"dw", "i", "yn", "y", "a", "ond"}      # always-allowed tokens

app = FastAPI(title="Welsh Vocab API")

@app.get("/allowed")
def get_allowed(section: int, unit: int):
    try:
        unlocked = df[
            (df.section < section) |
            ((df.section == section) & (df.unit <= unit))
        ]["welsh"].str.strip().tolist()
        tokens = sorted(set(unlocked) | CORE_SET)
        return {"allowed": tokens}
    except Exception as e:
        raise HTTPException(400, str(e))
