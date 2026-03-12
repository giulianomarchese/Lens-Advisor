"""
Lens Advisor — 50 casi test GS v1.0.1
Target distribuzione: L2 20% · L3 40% · L4 30% · L5 10%
(L5 richiede video_centratore=True)
"""
from engine import calcola
from collections import Counter

Q_ZERO = {
    "q0p": 45,
    "q1": "principale",
    "q2": 1,
    "q3": False,
    "q4": 1,
    "q5": None,
    "q6": "nessuno",
    "q7": "da_anni",
    "q8": "protezione",
    "q9": "nessuna",
}

CASI = [
    (1, "L2 — miopia lieve OD",
     {"sph_od": -1.50, "sph_os": 0.00, "cyl_od": 0, "cyl_os": 0, "add": 0, "pd": 64},
     {}, False, 2),
    (2, "L2 — ipermetropia lieve",
     {"sph_od": 1.25, "sph_os": 1.00, "cyl_od": 0, "cyl_os": 0, "add": 0, "pd": 64},
     {}, False, 2),
    (3, "L2 — cilindro sotto soglia soft",
     {"sph_od": 0.00, "sph_os": 0.00, "cyl_od": 0.75, "cyl_os": 0.50, "add": 0, "pd": 64},
     {}, False, 2),
    (4, "L2 — prescrizione piatta, Q6 nessuno",
     {"sph_od": -0.75, "sph_os": -0.50, "cyl_od": 0, "cyl_os": 0, "add": 0, "pd": 64},
     {"q6": "nessuno", "q8": "protezione"}, False, 2),
    (5, "L2 — ipermetropia minima, add assente",
     {"sph_od": 0.50, "sph_os": 0.75, "cyl_od": 0, "cyl_os": 0, "add": 0, "pd": 66},
     {"q8": "protezione"}, False, 2),
    (6, "L2 — miopia lieve bilaterale",
     {"sph_od": -1.00, "sph_os": -1.25, "cyl_od": 0, "cyl_os": 0, "add": 0, "pd": 62},
     {"q8": "protezione"}, False, 2),
    (7, "L2 — secondo paio da sole, prescrizione minima",
     {"sph_od": -0.50, "sph_os": -0.75, "cyl_od": 0, "cyl_os": 0, "add": 0, "pd": 64},
     {"q1": "secondo_paio", "q8": "protezione"}, False, 2),
    (8, "L2 — soft trigger singolo (cilindro 1.00), q8 neutro",
     {"sph_od": 0.00, "sph_os": 0.00, "cyl_od": 1.00, "cyl_os": 0.00, "add": 0, "pd": 64},
     {"q8": "protezione"}, False, 2),
    (9, "L2 — anisometropia sotto soft",
     {"sph_od": -1.00, "sph_os": 0.00, "cyl_od": 0, "cyl_os": 0, "add": 0, "pd": 64},
     {"q8": "protezione"}, False, 2),
    (10, "L2 — prescrizione nulla pratica (solo lieve miopia)",
     {"sph_od": -0.25, "sph_os": -0.25, "cyl_od": 0, "cyl_os": 0, "add": 0, "pd": 64},
     {"q8": "protezione"}, False, 2),
    (11, "L3 — due soft trigger (miopia 3.00 + cilindro 1.00)",
     {"sph_od": -3.00, "sph_os": -1.00, "cyl_od": 1.00, "cyl_os": 0, "add": 0, "pd": 64},
     {"q8": "protezione"}, False, 3),
    (12, "L3 — ipermetropia soft + cilindro soft",
     {"sph_od": 2.00, "sph_os": 1.50, "cyl_od": 0, "cyl_os": 1.00, "add": 0, "pd": 64},
     {"q8": "protezione"}, False, 3),
    (13, "L2 — add soft singolo (2.00), nessun altro trigger",
     {"sph_od": 1.00, "sph_os": 1.00, "cyl_od": 0, "cyl_os": 0, "add": 2.00, "pd": 64},
     {"q8": "protezione"}, False, 2),
    (14, "L3 — hard trigger singolo (cilindro 1.50)",
     {"sph_od": 0.00, "sph_os": 0.00, "cyl_od": 1.50, "cyl_os": 0, "add": 0, "pd": 64},
     {"q8": "protezione"}, False, 3),
    (15, "L3 — miopia hard singola (4.50), aniso contenuta",
     {"sph_od": -4.50, "sph_os": -3.00, "cyl_od": 0, "cyl_os": 0, "add": 0, "pd": 64},
     {"q8": "protezione"}, False, 3),
    (16, "L2 — anisometropia soft singola (1.25)",
     {"sph_od": -2.00, "sph_os": -0.75, "cyl_od": 0, "cyl_os": 0, "add": 0, "pd": 64},
     {"q8": "protezione"}, False, 2),
    (17, "L3 — ipermetropia hard singola (3.50)",
     {"sph_od": 3.50, "sph_os": 2.50, "cyl_od": 0, "cyl_os": 0, "add": 0, "pd": 64},
     {"q8": "protezione"}, False, 3),
    (18, "L2 — add soft singola + miopia lieve",
     {"sph_od": -1.50, "sph_os": -1.50, "cyl_od": 0, "cyl_os": 0, "add": 2.00, "pd": 64},
     {"q8": "protezione"}, False, 2),
    (19, "L3 — due soft (miopia 3.00 + aniso 1.25)",
     {"sph_od": -3.00, "sph_os": -1.75, "cyl_od": 0, "cyl_os": 0, "add": 0, "pd": 64},
     {"q8": "protezione"}, False, 3),
    (20, "L3 — cilindro hard singolo (1.50) + Q6 nessuno",
     {"sph_od": 0.00, "sph_os": 0.00, "cyl_od": 1.50, "cyl_os": 0, "add": 0, "pd": 64},
     {"q6": "nessuno", "q8": "protezione"}, False, 3),
    (21, "L2 — add soft 2.25 singola, ipermetropia lieve",
     {"sph_od": 1.50, "sph_os": 1.25, "cyl_od": 0, "cyl_os": 0, "add": 2.25, "pd": 64},
     {"q8": "protezione"}, False, 2),
    (22, "L3 — miopia soft (3.00) + Q7 prima volta senza trigger hard",
     {"sph_od": -3.00, "sph_os": -2.00, "cyl_od": 0, "cyl_os": 0, "add": 0, "pd": 64},
     {"q7": "prima_volta", "q8": "protezione"}, False, 3),
    (23, "L3 — due soft (ipermetropia 2.00 + add 2.00)",
     {"sph_od": 2.00, "sph_os": 1.75, "cyl_od": 0, "cyl_os": 0, "add": 2.00, "pd": 64},
     {"q8": "protezione"}, False, 3),
    (24, "L3 — cilindro soft (1.00) + miopia soft (3.00)",
     {"sph_od": -3.00, "sph_os": -1.00, "cyl_od": 1.00, "cyl_os": 0, "add": 0, "pd": 64},
     {"q8": "protezione"}, False, 3),
    (25, "L3 — aniso soft + ipermetropia lieve",
     {"sph_od": 2.50, "sph_os": 1.25, "cyl_od": 0, "cyl_os": 0, "add": 0, "pd": 64},
     {"q8": "protezione"}, False, 3),
    (26, "L3 — hard singolo (add 3.00), Q8 neutro",
     {"sph_od": 1.00, "sph_os": 1.00, "cyl_od": 0, "cyl_os": 0, "add": 3.00, "pd": 64},
     {"q8": "protezione"}, False, 3),
    (27, "L3 — miopia hard singola + Q1 secondo paio",
     {"sph_od": -4.50, "sph_os": -3.50, "cyl_od": 0, "cyl_os": 0, "add": 0, "pd": 64},
     {"q1": "secondo_paio", "q8": "protezione"}, False, 3),
    (28, "L3 — cilindro hard + Q7 da anni",
     {"sph_od": 0.00, "sph_os": 0.00, "cyl_od": 1.50, "cyl_os": 0, "add": 0, "pd": 64},
     {"q7": "da_anni", "q8": "protezione"}, False, 3),
    (29, "L3 — soft trigger singolo + Q6 signal (+1) → L3",
     {"sph_od": -1.50, "sph_os": -1.50, "cyl_od": 0, "cyl_os": 0, "add": 0, "pd": 64},
     {"q6": "signal", "q8": "protezione"}, False, 3),
    (30, "L3 — due soft (miopia + cilindro), Q8 neutro",
     {"sph_od": -3.00, "sph_os": -2.00, "cyl_od": 1.00, "cyl_os": 0, "add": 0, "pd": 64},
     {"q8": "protezione"}, False, 3),
    (31, "L4 — due hard trigger (miopia + cilindro)",
     {"sph_od": -4.50, "sph_os": -2.00, "cyl_od": 1.50, "cyl_os": 0, "add": 0, "pd": 64},
     {"q8": "protezione"}, False, 4),
    (32, "L4 — hard + 3 soft",
     {"sph_od": -4.50, "sph_os": -3.00, "cyl_od": 1.00, "cyl_os": 0, "add": 2.00, "pd": 64},
     {"q8": "protezione"}, False, 4),
    (33, "L4 — tre hard (miopia + cilindro + add)",
     {"sph_od": -4.50, "sph_os": -2.00, "cyl_od": 1.50, "cyl_os": 0, "add": 3.00, "pd": 64},
     {"q8": "protezione"}, False, 4),
    (34, "L4 — PD anomalo basso (55) + hard miopia",
     {"sph_od": -4.50, "sph_os": -2.00, "cyl_od": 0, "cyl_os": 0, "add": 0, "pd": 55},
     {"q8": "protezione"}, False, 4),
    (35, "L4 — ipermetropia hard + cilindro hard",
     {"sph_od": 3.50, "sph_os": 2.00, "cyl_od": 1.50, "cyl_os": 0, "add": 0, "pd": 64},
     {"q8": "protezione"}, False, 4),
    (36, "L3 — add hard + aniso soft + cilindro soft (1H+2S)",
     {"sph_od": -2.00, "sph_os": -0.75, "cyl_od": 1.00, "cyl_os": 0, "add": 3.00, "pd": 64},
     {"q8": "protezione"}, False, 3),
    (37, "L3 — miopia alta bilaterale (5.50/5.00) → 1 hard",
     {"sph_od": -5.50, "sph_os": -5.00, "cyl_od": 0, "cyl_os": 0, "add": 0, "pd": 64},
     {"q8": "protezione"}, False, 3),
    (38, "L4 — PD anomalo alto (72) + cilindro hard",
     {"sph_od": 0.00, "sph_os": 0.00, "cyl_od": 1.50, "cyl_os": 0, "add": 0, "pd": 72},
     {"q8": "protezione"}, False, 4),
    (39, "L4 — hard singolo + Q6 combined (+2) → L4",
     {"sph_od": -4.50, "sph_os": -1.00, "cyl_od": 0, "cyl_os": 0, "add": 0, "pd": 64},
     {"q6": "combined", "q8": "protezione"}, False, 4),
    (40, "L3 — aniso hard (2.00) + miopia soft (1H+1S)",
     {"sph_od": -3.00, "sph_os": -1.00, "cyl_od": 0, "cyl_os": 0, "add": 0, "pd": 64},
     {"q8": "protezione"}, False, 3),
    (41, "L4 — tre soft (miopia + cilindro + add) → 3S bypass L4",
     {"sph_od": -3.00, "sph_os": -2.00, "cyl_od": 1.00, "cyl_os": 0, "add": 2.00, "pd": 64},
     {"q8": "protezione"}, False, 4),
    (42, "L4 — ipermetropia hard + add hard",
     {"sph_od": 3.50, "sph_os": 2.00, "cyl_od": 0, "cyl_os": 0, "add": 3.00, "pd": 64},
     {"q8": "protezione"}, False, 4),
    (43, "L3 — miopia hard bilaterale + aniso soft (1H+1S)",
     {"sph_od": -4.50, "sph_os": -3.25, "cyl_od": 0, "cyl_os": 0, "add": 0, "pd": 64},
     {"q8": "protezione"}, False, 3),
    (44, "L4 — hard miopia + Q7 prima volta con hard_rx>=1",
     {"sph_od": -4.50, "sph_os": -2.00, "cyl_od": 0, "cyl_os": 0, "add": 0, "pd": 64},
     {"q7": "prima_volta", "q8": "protezione"}, False, 4),
    (45, "L4 — cilindro hard + add hard + miopia lieve",
     {"sph_od": -1.50, "sph_os": -1.50, "cyl_od": 1.50, "cyl_os": 0, "add": 3.00, "pd": 64},
     {"q8": "protezione"}, False, 4),
    (46, "L5 — prescrizione molto complessa, video centratore",
     {"sph_od": -6.00, "sph_os": -5.00, "cyl_od": 1.50, "cyl_os": 1.00, "add": 3.00, "pd": 64},
     {"q6": "combined", "q8": "protezione"}, True, 5),
    (47, "L5 — miopia altissima + cilindro hard + Q6 combined",
     {"sph_od": -7.00, "sph_os": -4.50, "cyl_od": 2.00, "cyl_os": 0, "add": 0, "pd": 64},
     {"q6": "combined", "q8": "protezione"}, True, 5),
    (48, "L5 — ipermetropia estrema + add hard",
     {"sph_od": 5.00, "sph_os": 4.50, "cyl_od": 0, "cyl_os": 0, "add": 3.50, "pd": 64},
     {"q6": "signal", "q8": "comfort"}, True, 5),
    (49, "L5 — PD anomalo + miopia hard + cilindro hard + add hard + Q6 combined",
     {"sph_od": -5.00, "sph_os": -4.50, "cyl_od": 1.50, "cyl_os": 0, "add": 3.00, "pd": 55},
     {"q6": "combined", "q8": "protezione"}, True, 5),
    (50, "L5 — aniso hard + miopia hard + Q6 combined",
     {"sph_od": -4.50, "sph_os": -2.50, "cyl_od": 0, "cyl_os": 0, "add": 0, "pd": 64},
     {"q6": "combined", "q7": "prima_volta", "q8": "comfort"}, True, 5),
]

def build_q(override: dict) -> dict:
    q = dict(Q_ZERO)
    q.update(override)
    return q

def run_tests():
    print(f"{'ID':>3}  {'Descrizione':<55}  {'Atteso':>6}  {'Ottenuto':>8}  {'Base':>5}  {'Delta':>5}  {'Esito'}")
    print("-" * 110)
    risultati = []
    contatore_livelli = Counter()
    falliti = []
    for caso in CASI:
        id_, descr, rx, q_override, video_c, atteso = caso
        q = build_q(q_override)
        out = calcola(rx, q, video_centratore=video_c)
        ottenuto = out["livello_consigliato"]
        base = out["livello_base_trigger"]
        delta = out["delta_questionario"]
        ok = ottenuto == atteso
        esito = "✓" if ok else "✗ FAIL"
        print(f"{id_:>3}  {descr:<55}  L{atteso}      L{ottenuto}       {base}     {delta:+}    {esito}")
        contatore_livelli[ottenuto] += 1
        risultati.append(ok)
        if not ok:
            falliti.append((id_, descr, atteso, ottenuto, base, delta))
    totale = len(CASI)
    passati = sum(risultati)
    print("\n" + "=" * 110)
    print(f"RISULTATO: {passati}/{totale} casi passati")
    print("\nDistribuzione livelli (ottenuti vs target):")
    target = {2: 20, 3: 40, 4: 30, 5: 10}
    for lv in [2, 3, 4, 5]:
        n = contatore_livelli.get(lv, 0)
        pct = n / totale * 100
        tgt = target.get(lv, 0)
        delta_d = pct - tgt
        marker = "✓" if abs(delta_d) <= 5 else "⚠"
        print(f"  L{lv}: {n:>2} casi ({pct:>5.1f}%)  target {tgt}%  delta {delta_d:+.1f}%  {marker}")
    if falliti:
        print("\nCASI FALLITI:")
        for f in falliti:
            id_, descr, att, ott, base, delta = f
            print(f"  #{id_} {descr}")
            print(f"     Atteso L{att} | Ottenuto L{ott} | Base trigger L{base} | Delta Q {delta:+}")
    else:
        print("\nTutti i casi superati. ENGINE GS v1.0.1 validato.")

if __name__ == "__main__":
    run_tests()
