"""
Lens Advisor — ENGINE Gold Standard v1.0.1
Specifica frozen. Nessuna modalità senza prescrizione.
"""
GS_VERSION = "1.0.1"
# ---------------------------------------------------------------------------
# SOGLIE
# ---------------------------------------------------------------------------
SOGLIE = {
    "addizione":      {"soft": 2.00, "hard": 3.00},
    "cilindro":       {"soft": 1.00, "hard": 1.50},
    "miopia":         {"soft": 3.00, "hard": 4.50},   # valore assoluto
    "ipermetropia":   {"soft": 2.00, "hard": 3.50},
    "anisometropia":  {"soft": 1.25, "hard": 2.00},
    "pd_basso":       {"hard": 58},
    "pd_alto":        {"hard": 70},
}
# ---------------------------------------------------------------------------
# INDICE SUGGERITO
# ---------------------------------------------------------------------------
def indice_suggerito(rx: dict, fotocromatico: bool = False) -> float:
    """Restituisce l'indice minimo suggerito in base alla prescrizione."""
    sph_od = abs(rx.get("sph_od", 0) or 0)
    sph_os = abs(rx.get("sph_os", 0) or 0)
    cyl_od = abs(rx.get("cyl_od", 0) or 0)
    cyl_os = abs(rx.get("cyl_os", 0) or 0)
    val = max(sph_od, sph_os, cyl_od, cyl_os)
    if val >= 7.00:
        idx = 1.74
    elif val >= 5.00:
        idx = 1.67
    elif val >= 3.00:
        idx = 1.60
    else:
        idx = 1.50
    # Fotocromatico esclude 1.74
    if fotocromatico and idx == 1.74:
        idx = 1.67
    return idx
# ---------------------------------------------------------------------------
# TRIGGER RX
# ---------------------------------------------------------------------------
def calcola_trigger(rx: dict) -> dict:
    """
    Analizza la prescrizione e restituisce trigger hard/soft e livello minimo tecnico.
    Restituisce anche flag per PD anomalo.
    """
    sph_od = rx.get("sph_od", 0) or 0
    sph_os = rx.get("sph_os", 0) or 0
    cyl_od = abs(rx.get("cyl_od", 0) or 0)
    cyl_os = abs(rx.get("cyl_os", 0) or 0)
    add    = rx.get("add", 0) or 0
    pd     = rx.get("pd", None)
    # Anisometropia sferica
    aniso = abs(sph_od - sph_os)
    hard_triggers = 0
    soft_triggers = 0
    def check(val, param):
        nonlocal hard_triggers, soft_triggers
        s = SOGLIE[param]
        if val >= s["hard"]:
            hard_triggers += 1
        elif val >= s["soft"]:
            soft_triggers += 1
    # Addizione
    check(add, "addizione")
    # Cilindro (peggiore occhio)
    check(max(cyl_od, cyl_os), "cilindro")
    # Miopia (valore assoluto, solo sfere negative)
    miopia = max(
        abs(sph_od) if sph_od < 0 else 0,
        abs(sph_os) if sph_os < 0 else 0
    )
    check(miopia, "miopia")
    # Ipermetropia (sfere positive)
    ipermetropia = max(
        sph_od if sph_od > 0 else 0,
        sph_os if sph_os > 0 else 0
    )
    check(ipermetropia, "ipermetropia")
    # Anisometropia
    check(aniso, "anisometropia")
    # PD anomalo — hard trigger diretto
    pd_anomalo = False
    if pd is not None:
        if pd <= SOGLIE["pd_basso"]["hard"] or pd >= SOGLIE["pd_alto"]["hard"]:
            hard_triggers += 1
            pd_anomalo = True
    # Livello minimo tecnico post-trigger
    if hard_triggers >= 3:
        livello_minimo = 4
    elif hard_triggers >= 2:
        livello_minimo = 4
    elif hard_triggers >= 1 and soft_triggers >= 3:
        livello_minimo = 4
    elif soft_triggers >= 3:
        livello_minimo = 4
    elif hard_triggers >= 1:
        livello_minimo = 3
    elif soft_triggers >= 2:
        livello_minimo = 3
    elif soft_triggers >= 1:
        livello_minimo = 2
    else:
        livello_minimo = 2  # L1 mai consigliato dal motore
    return {
        "hard_triggers": hard_triggers,
        "soft_triggers": soft_triggers,
        "livello_minimo": livello_minimo,
        "pd_anomalo": pd_anomalo,
        "miopia": miopia,
        "ipermetropia": ipermetropia,
        "aniso": aniso,
        "add": add,
        "cil_max": max(cyl_od, cyl_os),
    }
# ---------------------------------------------------------------------------
# NEAR DEMAND
# ---------------------------------------------------------------------------
def calcola_near_demand(q2: int, q4: int) -> int:
    """NearDemand = max(Q2, Q4) — mai doppio conteggio."""
    return max(q2 or 0, q4 or 0)
# ---------------------------------------------------------------------------
# QUESTIONARIO → DELTA LIVELLO
# ---------------------------------------------------------------------------
def applica_questionario(livello_base: int, rx_data: dict, q: dict, video_centratore: bool) -> dict:
    livello = livello_base
    delta = 0
    trattamenti = set()
    trt_note = []
    domande_saltate = sum(1 for v in q.values() if v is None)
    hard_rx = rx_data["hard_triggers"]
    soft_rx = rx_data["soft_triggers"]
    # Q1 — Tipo occhiale
    q1 = q.get("q1")
    if q1 == "secondo_paio":
        delta -= 1
    elif q1 == "sole":
        pass
    # Q2 — Vita digitale
    q2 = q.get("q2", 0) or 0
    q4 = q.get("q4", 0) or 0
    near_demand = calcola_near_demand(q2, q4)
    # Q5 — Flag office
    q5 = q.get("q5")
    # Q6 — Fastidi visivi
    q6 = q.get("q6", "nessuno")
    if q6 == "combined":
        delta += 2
    elif q6 == "signal" or q6 == "luci_fari":
        delta += 1
        if q6 == "luci_fari":
            trattamenti.add("antiriflesso_premium")
            trt_note.append("Q6 luci/fari → antiriflesso premium pre-selezionato")
    elif q6 == "negativo":
        delta -= 1
    # Q7 — Esperienza progressive
    q7 = q.get("q7")
    if q7 == "prima_volta":
        if hard_rx >= 1 or soft_rx >= 1:
            delta += 1
    kpi_q7 = q7
    # Q8 — Caratteristica più importante
    q8 = q.get("q8")
    if q8 == "comfort":
        delta += 1
    elif q8 == "protezione":
        trattamenti.add("trt_protezione")
    elif q8 == "riflessi":
        trattamenti.add("antiriflesso_premium")
    # Q9 — Protezione UV / tipo lente
    q9 = q.get("q9")
    if q9 == "fotocromatico":
        trattamenti.add("fotocromatico")
        trattamenti.discard("luce_blu")
        trt_note.append("Q9 fotocromatico → luce blu rimossa")
    elif q9 == "luce_blu" or (q2 >= 2 and q9 != "fotocromatico"):
        trattamenti.add("luce_blu")
        trt_note.append("Q2 alto o Q9 luce blu → luce blu pre-selezionata")
    # Applica delta al livello
    livello = livello_base + delta
    livello = max(livello, livello_base)
    livello = min(livello, 5)
    if not video_centratore and livello == 5:
        livello = 4
    livello = max(livello, 2)
    flag_office = q5
    return {
        "livello_consigliato": livello,
        "livello_base_trigger": livello_base,
        "delta_questionario": delta,
        "trattamenti_preselezionati": list(trattamenti),
        "flag_office": flag_office,
        "near_demand": near_demand,
        "kpi_q7": kpi_q7,
        "domande_saltate": domande_saltate,
        "trt_note": trt_note,
    }
# ---------------------------------------------------------------------------
# TRATTAMENTI STEP 8 — PROMOZIONI
# ---------------------------------------------------------------------------
def suggerimento_step8(flag_office: str | None, q9: str) -> dict:
    sole = (q9 == "sole")
    if flag_office == "attivo":
        if not sole:
            primo = "lente_office"
            secondo = "secondo_paio_sole"
        else:
            primo = "lente_office"
            secondo = "promemoria_generico"
    elif flag_office == "non_attivo" or flag_office is None:
        if not sole:
            primo = None
            secondo = "secondo_paio_sole_graduato"
        else:
            primo = None
            secondo = "promemoria_generico"
    else:
        primo = None
        secondo = "promemoria_generico"
    return {"primo": primo, "secondo": secondo}
# ---------------------------------------------------------------------------
# ENTRY POINT PRINCIPALE
# ---------------------------------------------------------------------------
def calcola(rx: dict, q: dict, video_centratore: bool = False) -> dict:
    rx_data = calcola_trigger(rx)
    livello_base = rx_data["livello_minimo"]
    risultato_q = applica_questionario(livello_base, rx_data, q, video_centratore)
    livello_finale = risultato_q["livello_consigliato"]
    fotocromatico = "fotocromatico" in risultato_q["trattamenti_preselezionati"]
    idx = indice_suggerito(rx, fotocromatico=fotocromatico)
    promo = suggerimento_step8(risultato_q["flag_office"], q.get("q9", "nessuna"))
    return {
        "gs_version": GS_VERSION,
        "livello_consigliato": livello_finale,
        "livello_base_trigger": livello_base,
        "delta_questionario": risultato_q["delta_questionario"],
        "hard_triggers": rx_data["hard_triggers"],
        "soft_triggers": rx_data["soft_triggers"],
        "trattamenti_preselezionati": risultato_q["trattamenti_preselezionati"],
        "indice_suggerito": idx,
        "flag_office": risultato_q["flag_office"],
        "near_demand": risultato_q["near_demand"],
        "promozioni": promo,
        "kpi": {
            "q7": risultato_q["kpi_q7"],
            "domande_saltate": risultato_q["domande_saltate"],
        },
        "pd_anomalo": rx_data["pd_anomalo"],
        "trt_note": risultato_q["trt_note"],
    }
