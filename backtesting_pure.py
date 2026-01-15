# backtesting_pure.py
# Backtesting PD (pur Python, sans dépendances)
# - Génère un portefeuille synthétique
# - Calcule PD vs Default Rate par déciles (approx) + Brier score
# - Donne une lecture "entretien-ready"

import math
import random
from collections import defaultdict

random.seed(0)

def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))

def mean(x):
    return sum(x) / len(x) if x else 0.0

def brier_score(p_list, y_list):
    return mean([(p - y) ** 2 for p, y in zip(p_list, y_list)])

def deciles_by_pd(rows, n_bins=10):
    """
    Découpage en quantiles approximatifs : on trie par PD,
    puis on coupe en n_bins groupes de taille (presque) égale.
    """
    rows_sorted = sorted(rows, key=lambda r: r["pd"])
    n = len(rows_sorted)
    bins = []
    for i in range(n_bins):
        a = (i * n) // n_bins
        b = ((i + 1) * n) // n_bins
        if a < b:
            bins.append(rows_sorted[a:b])
    return bins

def main():
    # 1) Dataset synthétique
    n = 40000
    rows = []

    # rating 1..10 ; PD modèle = logistic(-4 + 0.35*rating)
    # défaut observé ~ Bernoulli(PD "vraie"), ici on utilise PD modèle pour simplifier
    for _ in range(n):
        rating = random.randint(1, 10)
        pd_model = sigmoid(-4.0 + 0.35 * rating)

        # défaut réalisé (0/1)
        y = 1 if random.random() < pd_model else 0

        rows.append({
            "rating": rating,
            "pd": pd_model,
            "default": y,
        })

    p_list = [r["pd"] for r in rows]
    y_list = [r["default"] for r in rows]

    # 2) Brier (qualité globale)
    brier = brier_score(p_list, y_list)

    # 3) Calibration par déciles (PD vs DR)
    bins = deciles_by_pd(rows, n_bins=10)

    print("\n=== MINI BACKTEST PD (PURE PYTHON) ===")
    print(f"Observations: {n}")
    print(f"Brier score : {brier:.5f}\n")

    print("Déciles (triés par PD croissante) : PD_moyenne vs DR_observé")
    print("decile | n     | avg_PD  | DR (default rate) | DR - PD")
    print("-" * 60)

    for i, b in enumerate(bins, start=1):
        avg_pd = mean([r["pd"] for r in b])
        dr = mean([r["default"] for r in b])
        diff = dr - avg_pd
        print(f"{i:>6} | {len(b):<5} | {avg_pd:>6.4f} | {dr:>15.4f} | {diff:>7.4f}")

    # 4) Sanity check par rating
    by_rating = defaultdict(list)
    for r in rows:
        by_rating[r["rating"]].append(r)

    print("\n--- Sanity check par rating ---")
    print("rating | n     | avg_PD  | DR")
    print("-" * 34)
    for rating in sorted(by_rating.keys()):
        g = by_rating[rating]
        avg_pd = mean([x["pd"] for x in g])
        dr = mean([x["default"] for x in g])
        print(f"{rating:>6} | {len(g):<5} | {avg_pd:>6.4f} | {dr:>6.4f}")

    print("\nInterprétation (entretien):")
    print("- On valide la calibration si, par décile, DR est proche de la PD moyenne.")
    print("- Si DR > PD de façon systématique, le modèle sous-estime le risque.")
    print("- Si DR < PD de façon systématique, le modèle est conservateur.")

if __name__ == "__main__":
    main()
