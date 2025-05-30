# app.py – FastAPI micro-service
import os
import pandas as pd
from fastapi import FastAPI, HTTPException
import uvicorn
from fastapi.staticfiles import StaticFiles

df = pd.read_excel("data/welsh_vocab.xlsx", engine="openpyxl")
CORE_SET = {"dw", "i", "yn", "y", "a", "ond"}  # always-allowed tokens

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

# This block is required for Render to bind to the correct port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)

from fastapi.staticfiles import StaticFiles
app.mount("/.well-known", StaticFiles(directory=os.path.join(os.path.dirname(__file__), ".well-known")), name="static")
