from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import json
import os
from engine import calcola

app = FastAPI(title="Lens Advisor API", version="1.0.0")

DIST_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carica layer commerciale
LENTI_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "lenti.json")
with open(LENTI_PATH, "r", encoding="utf-8") as f:
    LENTI_DATA = json.load(f)


class Prescrizione(BaseModel):
    sph_od: float = 0
    sph_os: float = 0
    cyl_od: float = 0
    cyl_os: float = 0
    ax_od: Optional[int] = None
    ax_os: Optional[int] = None
    add: float = 0
    pd: Optional[float] = None


class Questionario(BaseModel):
    q0p: int = 45
    q1: str = "principale"
    q2: int = 0
    q3: bool = False
    q4: int = 0
    q5: Optional[str] = None
    q6: str = "nessuno"
    q7: str = "da_anni"
    q8: str = "comfort"
    q9: str = "nessuna"


class CalcolaRequest(BaseModel):
    rx: Prescrizione
    questionario: Questionario
    video_centratore: bool = False


@app.post("/api/calcola")
def api_calcola(req: CalcolaRequest):
    rx_dict = {
        "sph_od": req.rx.sph_od,
        "sph_os": req.rx.sph_os,
        "cyl_od": req.rx.cyl_od,
        "cyl_os": req.rx.cyl_os,
        "add": req.rx.add,
        "pd": req.rx.pd,
    }
    q_dict = req.questionario.model_dump()
    risultato = calcola(rx_dict, q_dict, video_centratore=req.video_centratore)

    # Arricchisci con nomi commerciali
    livello = risultato["livello_consigliato"]
    lente_info = LENTI_DATA["livelli"].get(str(livello), {})
    risultato["nome_commerciale"] = lente_info.get("nome", f"Livello {livello}")
    risultato["descrizione_commerciale"] = lente_info.get("descrizione", "")
    risultato["vantaggi"] = lente_info.get("vantaggi", [])

    # Alternative adiacenti
    alternative = []
    for alt_lv in [livello - 1, livello + 1]:
        if alt_lv < 1 or alt_lv > 5:
            continue
        if alt_lv == 5 and not req.video_centratore:
            continue
        alt_info = LENTI_DATA["livelli"].get(str(alt_lv), {})
        alternative.append({
            "livello": alt_lv,
            "nome": alt_info.get("nome", f"Livello {alt_lv}"),
            "descrizione": alt_info.get("descrizione", ""),
            "tipo": "economica" if alt_lv < livello else "premium",
            "is_l1": alt_lv == 1,
        })
    # L1 sempre visibile come opzione economica separata in step 5
    if livello > 2:
        l1_info = LENTI_DATA["livelli"].get("1", {})
        if not any(a["livello"] == 1 for a in alternative):
            alternative.append({
                "livello": 1,
                "nome": l1_info.get("nome", "Livello 1"),
                "descrizione": l1_info.get("descrizione", ""),
                "tipo": "economica",
                "is_l1": True,
            })

    risultato["alternative"] = alternative
    risultato["trattamenti_info"] = LENTI_DATA.get("trattamenti", {})

    return risultato


@app.get("/api/lenti")
def api_lenti():
    return LENTI_DATA


@app.get("/api/health")
def health():
    return {"status": "ok", "engine_version": "1.0.1"}


# Serve frontend build
if os.path.isdir(DIST_DIR):
    app.mount("/assets", StaticFiles(directory=os.path.join(DIST_DIR, "assets")), name="static")

    @app.get("/{full_path:path}")
    def serve_frontend(full_path: str):
        file_path = os.path.join(DIST_DIR, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(DIST_DIR, "index.html"))
